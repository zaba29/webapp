from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

from cmr_form import FIELD_LABELS


# Coordinate map for easy layout adjustment.
# All coordinates are in millimeters from bottom-left.
FIELD_BOXES: Dict[str, Tuple[float, float, float, float]] = {
    "sender": (10, 250, 90, 35),
    "consignee": (105, 250, 95, 35),
    "delivery_address": (10, 220, 90, 30),
    "carrier": (105, 220, 95, 30),
    "place_date_taking_over": (10, 202, 90, 18),
    "successive_carriers": (105, 202, 95, 18),
    "place_designated_delivery": (10, 184, 190, 18),
    "marks_numbers": (10, 110, 35, 74),
    "number_kind_packages": (45, 110, 45, 74),
    "description_goods": (90, 110, 65, 74),
    "gross_weight": (155, 110, 22.5, 74),
    "volume": (177.5, 110, 22.5, 74),
    "carriage_charges": (10, 92, 60, 18),
    "customs_instructions": (70, 92, 130, 18),
    "t_form_instructions": (10, 74, 60, 18),
    "reservations": (70, 74, 130, 18),
    "documents_attached": (10, 56, 60, 18),
    "special_agreements": (70, 56, 130, 18),
    "goods_received": (10, 38, 63.3, 18),
    "goods_collected": (73.3, 38, 63.3, 18),
    "wh_job_reference": (136.6, 38, 63.4, 18),
    "place_date": (10, 20, 90, 18),
    "signatures_stamps": (100, 20, 100, 18),
    "company_completing_note": (10, 8, 190, 12),
}


def _draw_multiline_text(c: canvas.Canvas, text: str, x: float, y: float, w: float, h: float) -> None:
    pad = 2 * mm
    line_height = 9
    max_width = (w * mm) - 2 * pad
    cursor_y = (y * mm) + (h * mm) - pad - line_height

    for raw_line in text.splitlines() or [""]:
        words = raw_line.split(" ")
        line = ""
        for word in words:
            trial = word if not line else f"{line} {word}"
            if pdfmetrics.stringWidth(trial, "Helvetica", 8) <= max_width:
                line = trial
            else:
                c.drawString((x * mm) + pad, cursor_y, line)
                cursor_y -= line_height
                line = word
                if cursor_y < (y * mm) + pad:
                    return
        c.drawString((x * mm) + pad, cursor_y, line)
        cursor_y -= line_height
        if cursor_y < (y * mm) + pad:
            return


def generate_cmr_pdf(data: Dict[str, str], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4

    c.setTitle("CMR Creator - Transport Document")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(10 * mm, height - 12 * mm, "INTERNATIONAL CONSIGNMENT NOTE / LETTRE DE VOITURE CMR")

    c.setFont("Helvetica", 8)
    c.drawRightString(width - 10 * mm, height - 12 * mm, "CMR Creator")

    for key, (x, y, w, h) in FIELD_BOXES.items():
        c.rect(x * mm, y * mm, w * mm, h * mm)
        label = FIELD_LABELS.get(key, key)
        c.setFont("Helvetica", 7)
        c.drawString((x * mm) + 2 * mm, (y * mm) + (h * mm) - 3.5 * mm, label)

        value = data.get(key, "")
        c.setFont("Helvetica", 8)
        _draw_multiline_text(c, value, x, y, w, h - 4)

    c.setFont("Helvetica-Oblique", 6.5)
    c.drawString(10 * mm, 4 * mm, "Layout coordinates are editable in pdf_generator.py::FIELD_BOXES")

    c.showPage()
    c.save()
    return output_path
