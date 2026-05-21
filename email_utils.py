from __future__ import annotations

import subprocess
import urllib.parse
from pathlib import Path


def send_with_default_mail_client(pdf_path: Path, subject: str = "CMR Document") -> None:
    subject_q = urllib.parse.quote(subject)
    body_q = urllib.parse.quote(f"Please find the CMR document attached.\n\nFile: {pdf_path}")
    mailto = f"mailto:?subject={subject_q}&body={body_q}"
    subprocess.run(["cmd", "/c", "start", "", mailto], check=False)


def open_file_location(pdf_path: Path) -> None:
    subprocess.run(["explorer", "/select,", str(pdf_path)], check=False)
