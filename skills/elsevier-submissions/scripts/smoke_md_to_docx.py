#!/usr/bin/env python3
"""Convert the bundled Markdown fixture and verify a DOCX is written."""
from __future__ import annotations

import sys
import tempfile
import zipfile
from pathlib import Path

from md_to_docx import markdown_to_docx


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    """Run the Markdown-to-DOCX smoke against the bundled fixture."""
    source = ROOT / "tests" / "fixtures" / "highlights.md"
    with tempfile.TemporaryDirectory(prefix="elsevier-docx-smoke-") as tmp:
        target = Path(tmp) / "highlights.docx"
        markdown_to_docx(source, target)
        if not target.is_file() or not zipfile.is_zipfile(target):
            print("Markdown-to-DOCX smoke failed: output is missing or invalid")
            return 1
        with zipfile.ZipFile(target) as archive:
            if "word/document.xml" not in archive.namelist():
                print("Markdown-to-DOCX smoke failed: document XML is missing")
                return 1
    print("Markdown-to-DOCX smoke passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
