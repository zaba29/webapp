from __future__ import annotations

import json
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QScrollArea,
    QSplitter,
    QStatusBar,
    QVBoxLayout,
    QWidget,
    QLineEdit,
)

from cmr_form import CMRData, FIELD_LABELS, MULTILINE_FIELDS, REQUIRED_FIELDS
from email_utils import open_file_location, send_with_default_mail_client
from pdf_generator import generate_cmr_pdf
from print_utils import print_pdf

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
DRAFTS_DIR = BASE_DIR / "saved_drafts"


class CMRWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("CMR Creator")
        self.resize(1300, 850)

        OUTPUT_DIR.mkdir(exist_ok=True)
        DRAFTS_DIR.mkdir(exist_ok=True)

        self.fields: dict[str, QLineEdit | QPlainTextEdit] = {}
        self.last_pdf: Path | None = None

        root = QWidget()
        root_layout = QVBoxLayout(root)

        root_layout.addLayout(self._build_toolbar())
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self._build_form_panel())
        splitter.addWidget(self._build_preview_panel())
        splitter.setSizes([850, 450])
        root_layout.addWidget(splitter)

        self.setCentralWidget(root)
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready")

        self._add_menu_actions()

    def _build_toolbar(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        buttons = [
            ("New", self.new_form),
            ("Save Draft", self.save_draft),
            ("Load Draft", self.load_draft),
            ("Export PDF", self.export_pdf),
            ("Print", self.print_document),
            ("Send", self.send_document),
        ]
        for title, callback in buttons:
            b = QPushButton(title)
            b.clicked.connect(callback)
            b.setMinimumHeight(36)
            layout.addWidget(b)
        layout.addStretch()
        return layout

    def _build_form_panel(self) -> QWidget:
        container = QWidget()
        form_layout = QFormLayout(container)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignTop)

        for key, label in FIELD_LABELS.items():
            if key in MULTILINE_FIELDS:
                widget = QPlainTextEdit()
                widget.setFixedHeight(70)
            else:
                widget = QLineEdit()
            self.fields[key] = widget
            form_layout.addRow(label, widget)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)
        return scroll

    def _build_preview_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        self.preview = QLabel(
            "Preview area\n\nGenerate PDF to see summary of entered content.\n"
            "(Optional PDF rendering can be added with PyMuPDF.)"
        )
        self.preview.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.preview.setWordWrap(True)
        self.preview.setStyleSheet("border:1px solid #bdbdbd; padding:12px; background:#fafafa;")
        layout.addWidget(self.preview)
        return panel

    def _add_menu_actions(self) -> None:
        file_menu = self.menuBar().addMenu("File")
        for text, handler in [
            ("New", self.new_form),
            ("Save Draft", self.save_draft),
            ("Load Draft", self.load_draft),
            ("Export PDF", self.export_pdf),
            ("Print", self.print_document),
        ]:
            action = QAction(text, self)
            action.triggered.connect(handler)
            file_menu.addAction(action)

    def _collect_data(self) -> CMRData:
        values: dict[str, str] = {}
        for key, widget in self.fields.items():
            if isinstance(widget, QPlainTextEdit):
                values[key] = widget.toPlainText().strip()
            else:
                values[key] = widget.text().strip()
        return CMRData.from_dict(values)

    def _set_data(self, data: CMRData) -> None:
        for key, value in data.to_dict().items():
            widget = self.fields[key]
            if isinstance(widget, QPlainTextEdit):
                widget.setPlainText(value)
            else:
                widget.setText(value)

    def _validate(self) -> list[str]:
        missing = []
        for key in REQUIRED_FIELDS:
            widget = self.fields[key]
            text = widget.toPlainText().strip() if isinstance(widget, QPlainTextEdit) else widget.text().strip()
            if not text:
                missing.append(FIELD_LABELS[key])
                widget.setStyleSheet("background-color: #fff2a8;")
            else:
                widget.setStyleSheet("")
        return missing

    def _refresh_preview(self, data: CMRData) -> None:
        lines = ["Current CMR draft summary:\n"]
        for key, label in FIELD_LABELS.items():
            value = data.to_dict().get(key, "")
            if value:
                lines.append(f"• {label}: {value[:100]}")
        self.preview.setText("\n".join(lines))

    def new_form(self) -> None:
        self._set_data(CMRData())
        self.preview.setText("New CMR started.")
        self.last_pdf = None
        self.statusBar().showMessage("Started a new CMR")

    def save_draft(self) -> None:
        data = self._collect_data().to_dict()
        path, _ = QFileDialog.getSaveFileName(self, "Save Draft", str(DRAFTS_DIR / "cmr_draft.json"), "JSON (*.json)")
        if not path:
            return
        Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        self.statusBar().showMessage(f"Draft saved: {path}")

    def load_draft(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Load Draft", str(DRAFTS_DIR), "JSON (*.json)")
        if not path:
            return
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        data = CMRData.from_dict(payload)
        self._set_data(data)
        self._refresh_preview(data)
        self.statusBar().showMessage(f"Draft loaded: {path}")

    def _generate_pdf(self, explicit_path: Path | None = None) -> Path:
        data = self._collect_data()
        missing = self._validate()
        if missing:
            QMessageBox.warning(self, "Important fields missing", "Some important fields are empty:\n- " + "\n- ".join(missing))
        output_path = explicit_path or OUTPUT_DIR / "cmr_document.pdf"
        generate_cmr_pdf(data.to_dict(), output_path)
        self._refresh_preview(data)
        self.last_pdf = output_path
        self.statusBar().showMessage(f"PDF generated: {output_path}")
        return output_path

    def export_pdf(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Export PDF", str(OUTPUT_DIR / "cmr_document.pdf"), "PDF (*.pdf)")
        if not path:
            return
        try:
            self._generate_pdf(Path(path))
        except Exception as exc:
            QMessageBox.critical(self, "Export error", str(exc))

    def print_document(self) -> None:
        try:
            pdf_path = self._generate_pdf()
            print_pdf(pdf_path)
        except Exception as exc:
            QMessageBox.critical(self, "Print error", str(exc))

    def send_document(self) -> None:
        try:
            pdf_path = self.last_pdf or self._generate_pdf()
            send_with_default_mail_client(pdf_path)
            open_file_location(pdf_path)
        except Exception as exc:
            QMessageBox.critical(self, "Send error", str(exc))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = CMRWindow()
    w.show()
    sys.exit(app.exec())
