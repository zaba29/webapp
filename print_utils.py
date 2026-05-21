from __future__ import annotations

import os
import platform
import subprocess
from pathlib import Path


def print_pdf(file_path: Path) -> None:
    if not file_path.exists():
        raise FileNotFoundError(f"Cannot print missing file: {file_path}")

    system = platform.system().lower()
    if "windows" in system:
        os.startfile(str(file_path), "print")  # type: ignore[attr-defined]
    else:
        # Fallback for development environments.
        subprocess.run(["xdg-open", str(file_path)], check=False)
