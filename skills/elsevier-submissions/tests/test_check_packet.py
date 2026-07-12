from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def write_minimal_docx(path: Path, paragraphs: list[str]) -> None:
    """Write the minimum OOXML parts used by the packet check seam."""
    content = "".join(f"<w:p><w:r><w:t>{item}</w:t></w:r></w:p>" for item in paragraphs)
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{content}</w:body></w:document>"
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(
            "[Content_Types].xml",
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml" />'
            '<Default Extension="xml" ContentType="application/xml" />'
            '<Override PartName="/word/document.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml" />'
            "</Types>",
        )
        archive.writestr(
            "_rels/.rels",
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
            'Target="word/document.xml" />'
            "</Relationships>",
        )
        archive.writestr("word/document.xml", document)


def write_manuscript(path: Path) -> None:
    """Write structural Elsevier backmatter in the required order."""
    path.write_text(
        "\\begin{abstract}A concise abstract for packet verification.\\end{abstract}\n"
        "\\section*{CRediT authorship contribution statement}\n"
        "\\section*{Declaration of competing interest}\n"
        "\\section*{Acknowledgements and Funding}\n"
        "\\section*{Data availability}\n",
        encoding="utf-8",
    )


def base_manifest() -> dict[str, object]:
    """Return a complete PDF-only packet manifest for focused test overrides."""
    today = date.today().isoformat()
    return {
        "em_step": "initial PDF and side-material upload",
        "em_step_checked_on": today,
        "journal_guide_url": "https://example.com/guide-for-authors",
        "journal_limits_checked_on": today,
        "journal_limits": {
            "abstract_max_words": 250,
            "highlights_min_items": 3,
            "highlights_max_items": 5,
            "highlight_max_characters": 85,
        },
        "manuscript": "main.tex",
        "source_required": False,
        "side_materials": ["highlights.docx"],
    }


class PacketCheckTests(unittest.TestCase):
    def run_check(self, directory: Path, manifest: object) -> subprocess.CompletedProcess[str]:
        """Invoke the public packet-check CLI."""
        manifest_path = directory / "packet.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "check_packet.py"), str(manifest_path)],
            capture_output=True,
            text=True,
            check=False,
        )

    def prepare_packet(self, directory: Path) -> None:
        """Write the common manuscript and highlights outputs."""
        write_manuscript(directory / "main.tex")
        write_minimal_docx(
            directory / "highlights.docx",
            ["Highlights", "First result", "Second result", "Third result"],
        )

    def test_complete_pdf_only_packet_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.prepare_packet(directory)
            result = self.run_check(directory, base_manifest())

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("packet check passed", result.stdout.lower())

    def test_required_source_zip_cannot_be_omitted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.prepare_packet(directory)
            manifest = base_manifest()
            manifest.update(
                em_step="revision source upload", source_required=True, source_zip="source.zip"
            )
            result = self.run_check(directory, manifest)

        self.assertEqual(result.returncode, 1)
        self.assertIn("source zip does not exist", result.stdout.lower())

    def test_required_source_zip_must_be_flat(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.prepare_packet(directory)
            with zipfile.ZipFile(directory / "source.zip", "w") as archive:
                archive.writestr("main.tex", "\\documentclass{elsarticle}")
                archive.writestr("figures/plot.png", b"not-an-image")
            manifest = base_manifest()
            manifest.update(
                em_step="revision source upload",
                source_required=True,
                source_zip="source.zip",
                source_entrypoint="main.tex",
            )
            result = self.run_check(directory, manifest)

        self.assertEqual(result.returncode, 1)
        self.assertIn("source zip is not flat", result.stdout.lower())

    def test_manifest_rejects_a_string_side_material_list(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            manifest = base_manifest()
            manifest["side_materials"] = "highlights.docx"
            result = self.run_check(directory, manifest)

        self.assertEqual(result.returncode, 1)
        self.assertIn("side_materials must be a non-empty json array", result.stdout.lower())

    def test_comments_cannot_satisfy_statement_headings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.prepare_packet(directory)
            (directory / "main.tex").write_text(
                "\\begin{abstract}Short abstract.\\end{abstract}\n"
                "% \\section*{CRediT authorship contribution statement}\n"
                "\\section*{Declaration of competing interest}\n"
                "\\section*{Acknowledgements and Funding}\n"
                "\\section*{Data availability}\n",
                encoding="utf-8",
            )
            result = self.run_check(directory, base_manifest())

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing required statement heading: credit", result.stdout.lower())

    def test_highlight_character_limit_is_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            self.prepare_packet(directory)
            write_minimal_docx(
                directory / "highlights.docx",
                ["Highlights", "x" * 86, "Second result", "Third result"],
            )
            result = self.run_check(directory, base_manifest())

        self.assertEqual(result.returncode, 1)
        self.assertIn("maximum is 85", result.stdout.lower())

    def test_invalid_docx_container_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            write_manuscript(directory / "main.tex")
            with zipfile.ZipFile(directory / "highlights.docx", "w") as archive:
                archive.writestr("[Content_Types].xml", "<Types />")
                archive.writestr("_rels/.rels", "<Relationships />")
                archive.writestr("word/document.xml", "<document />")
            result = self.run_check(directory, base_manifest())

        self.assertEqual(result.returncode, 1)
        self.assertIn("lacks a valid word document", result.stdout.lower())


if __name__ == "__main__":
    unittest.main()
