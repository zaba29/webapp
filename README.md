# CMR Creator

Windows desktop application for creating CMR transport documents, exporting/printing PDF files, and saving JSON drafts.

## Features
- Editable CMR form with all requested fields.
- Professional A4 PDF generation (English/French labels, box-grid layout inspired by CMR template).
- Print action (default Windows print action).
- Export PDF with custom file name/location.
- Send action (opens default mail client via `mailto:` and opens file location).
- Save/Load local draft JSON files.
- Light validation with highlighted important fields.

## Project Structure
- `main.py` - PySide6 desktop UI and app workflow.
- `cmr_form.py` - CMR field data model, labels, required fields.
- `pdf_generator.py` - reportlab layout and PDF renderer.
- `print_utils.py` - print helper.
- `email_utils.py` - email/send helpers.
- `output/` - generated PDFs.
- `saved_drafts/` - draft JSON files.
- `templates/`, `assets/` - placeholders for template and resources.

## Setup (Development)
1. Install Python 3.12.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run app:
   ```bash
   python main.py
   ```

## Build Windows EXE (PyInstaller)
Run on Windows in project root:

```bash
pyinstaller --noconfirm --onefile --windowed --name "CMR Creator" main.py
```

Generated executable:
- `dist/CMR Creator.exe`

## Usage
1. Fill CMR form fields.
2. Use:
   - **New** to clear form.
   - **Save Draft** / **Load Draft** for JSON drafts.
   - **Export PDF** to create print-ready CMR PDF.
   - **Print** to print generated PDF.
   - **Send** to open email compose + file location.

## Notes
- PDF layout coordinates are centralized in `pdf_generator.py` as `FIELD_BOXES` for easy visual tuning.
- The current layout is a clean professional CMR structure inspired by typical CMR templates; you can refine coordinates to match a specific company template exactly.
