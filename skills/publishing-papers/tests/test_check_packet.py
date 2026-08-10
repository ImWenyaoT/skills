from __future__ import annotations

import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_packet.py"
TODAY = dt.date.today().isoformat()


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
            '<Default Extension="rels" '
            'ContentType="application/vnd.openxmlformats-package.relationships+xml" />'
            '<Default Extension="xml" ContentType="application/xml" />'
            '<Override PartName="/word/document.xml" '
            'ContentType="'
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml" />'
            "</Types>",
        )
        archive.writestr(
            "_rels/.rels",
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" '
            'Type="'
            'http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
            'Target="word/document.xml" />'
            "</Relationships>",
        )
        archive.writestr("word/document.xml", document)


def write_pdf(path: Path, pages: int) -> None:
    """Write a minimal uncompressed PDF with an exact page count."""
    objects = ["<< /Type /Catalog /Pages 2 0 R >>"]
    kids = " ".join(f"{index + 3} 0 R" for index in range(pages))
    objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {pages} >>")
    objects.extend("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>" for _ in range(pages))
    body = b"%PDF-1.4\n"
    offsets = []
    for number, obj in enumerate(objects, start=1):
        offsets.append(len(body))
        body += f"{number} 0 obj\n{obj}\nendobj\n".encode("ascii")
    xref_start = len(body)
    xref = f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode("ascii")
    xref += b"".join(f"{offset:010d} 00000 n \n".encode("ascii") for offset in offsets)
    trailer = (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF\n"
    ).encode("ascii")
    path.write_bytes(body + xref + trailer)


def write_elsevier_manuscript(path: Path) -> None:
    """Write structural Elsevier backmatter in the required order."""
    path.write_text(
        "\\begin{abstract}A concise abstract for packet verification.\\end{abstract}\n"
        "\\section*{CRediT authorship contribution statement}\n"
        "\\section*{Declaration of competing interest}\n"
        "\\section*{Acknowledgements and Funding}\n"
        "\\section*{Data availability}\n",
        encoding="utf-8",
    )


def write_ieee_manuscript(path: Path, abstract_words: int) -> None:
    """Write an IEEE manuscript whose abstract has an exact word count."""
    words = " ".join(f"word{index}" for index in range(abstract_words))
    path.write_text(
        "\\documentclass[journal]{IEEEtran}\n\\begin{document}\n"
        f"\\begin{{abstract}}\n{words}\n\\end{{abstract}}\n\\end{{document}}\n",
        encoding="utf-8",
    )


def elsevier_manifest() -> dict[str, Any]:
    """Return a complete PDF-only Elsevier manifest for focused test overrides."""
    return {
        "publisher": "elsevier",
        "submission_step": "initial PDF and side-material upload",
        "submission_step_checked_on": TODAY,
        "journal_guide_url": "https://example.com/guide-for-authors",
        "journal_limits_checked_on": TODAY,
        "journal_limits": {
            "abstract_max_words": 250,
            "highlights_min_items": 3,
            "highlights_max_items": 5,
            "highlight_max_characters": 85,
        },
        "manuscript": "main.tex",
        "source_required": False,
        "side_materials": ["highlights.docx"],
        "submission_stage": "initial",
    }


def ieee_manifest() -> dict[str, Any]:
    """Return a complete initial IEEE manifest for focused test overrides."""
    return {
        "publisher": "ieee",
        "submission_step": "initial submission",
        "submission_step_checked_on": TODAY,
        "journal_guide_url": "https://signalprocessingsociety.org/publications-resources/information-authors",
        "journal_limits_checked_on": TODAY,
        "journal_limits": {
            "abstract_min_words": 150,
            "abstract_max_words": 250,
            "max_pages": 10,
        },
        "manuscript": "main.tex",
        "manuscript_pdf": "manuscript.pdf",
        "edics": ["MMSP-ANAL"],
        "side_materials": [],
        "submission_stage": "initial",
        "source_required": False,
    }


class PacketCheckTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory(prefix="journal-packet-test-")
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name)

    def run_check(
        self, manifest: object, env: dict | None = None
    ) -> subprocess.CompletedProcess[str]:
        """Invoke the public packet-check CLI."""
        manifest_path = self.base / "packet.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(manifest_path)],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )


class PublisherSelectionTests(PacketCheckTestCase):
    def test_missing_publisher_fails(self) -> None:
        manifest = elsevier_manifest()
        del manifest["publisher"]
        result = self.run_check(manifest)
        self.assertEqual(result.returncode, 1)
        self.assertIn("publisher must be one of", result.stdout)

    def test_other_publishers_key_is_rejected(self) -> None:
        """The per-publisher key set is closed: an IEEE key is invalid for Elsevier."""
        write_elsevier_manuscript(self.base / "main.tex")
        manifest = elsevier_manifest()
        manifest["edics"] = ["MMSP-ANAL"]
        result = self.run_check(manifest)
        self.assertEqual(result.returncode, 1)
        self.assertIn("unknown manifest key(s) for elsevier: edics", result.stdout)

    def test_other_publishers_limit_key_is_rejected(self) -> None:
        write_ieee_manuscript(self.base / "main.tex", abstract_words=200)
        write_pdf(self.base / "manuscript.pdf", pages=10)
        manifest = ieee_manifest()
        manifest["journal_limits"]["highlight_max_characters"] = 85
        result = self.run_check(manifest)
        self.assertEqual(result.returncode, 1)
        self.assertIn("unknown journal_limits key(s) for ieee", result.stdout)


class ElsevierPacketTests(PacketCheckTestCase):
    def setUp(self) -> None:
        super().setUp()
        write_elsevier_manuscript(self.base / "main.tex")
        write_minimal_docx(
            self.base / "highlights.docx",
            ["Highlights", "First result", "Second result", "Third result"],
        )

    def test_complete_pdf_only_packet_passes(self) -> None:
        result = self.run_check(elsevier_manifest())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("packet check passed", result.stdout.lower())

    def test_revision_packet_rejects_missing_response_to_reviewers(self) -> None:
        manifest = elsevier_manifest()
        manifest.update(
            submission_step="revision upload",
            submission_stage="revision",
            response_to_reviewers="response.docx",
        )
        result = self.run_check(manifest)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("response_to_reviewers is missing", result.stdout.lower())

    def test_revision_packet_rejects_missing_marked_manuscript(self) -> None:
        """A declared marked manuscript must exist and differ from the clean one."""
        write_minimal_docx(self.base / "response.docx", ["Response to reviewers"])
        manifest = elsevier_manifest()
        manifest.update(
            submission_step="revision upload",
            submission_stage="revision",
            response_to_reviewers="response.docx",
            marked_manuscript="marked.pdf",
        )
        result = self.run_check(manifest)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("marked_manuscript is missing", result.stdout.lower())

    def test_complete_revision_packet_passes(self) -> None:
        write_minimal_docx(self.base / "response.docx", ["Response to reviewers"])
        (self.base / "marked.pdf").write_bytes(b"%PDF-1.4 marked")
        manifest = elsevier_manifest()
        manifest.update(
            submission_step="revision upload",
            submission_stage="revision",
            response_to_reviewers="response.docx",
            marked_manuscript="marked.pdf",
        )
        result = self.run_check(manifest)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("packet check passed", result.stdout.lower())

    def test_unknown_manifest_key_is_rejected(self) -> None:
        """A misspelled key must fail loudly instead of silently disabling a check."""
        manifest = elsevier_manifest()
        manifest.update(submission_stage="revision", response_to_reviewer="response.docx")
        result = self.run_check(manifest)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("unknown manifest key(s) for elsevier: response_to_reviewer", result.stdout)

    def test_required_source_zip_cannot_be_omitted(self) -> None:
        manifest = elsevier_manifest()
        manifest.update(
            submission_step="revision source upload", source_required=True, source_zip="source.zip"
        )
        result = self.run_check(manifest)
        self.assertEqual(result.returncode, 1)
        self.assertIn("source zip does not exist", result.stdout.lower())

    def test_required_source_zip_must_be_flat(self) -> None:
        with zipfile.ZipFile(self.base / "source.zip", "w") as archive:
            archive.writestr("main.tex", "\\documentclass{elsarticle}")
            archive.writestr("figures/plot.png", b"not-an-image")
        manifest = elsevier_manifest()
        manifest.update(
            submission_step="revision source upload",
            source_required=True,
            source_zip="source.zip",
            source_entrypoint="main.tex",
        )
        result = self.run_check(manifest)
        self.assertEqual(result.returncode, 1)
        self.assertIn("source zip is not flat", result.stdout.lower())

    def test_source_step_cannot_disable_source(self) -> None:
        manifest = elsevier_manifest()
        manifest["submission_step"] = "revision source upload"
        result = self.run_check(manifest)
        self.assertEqual(result.returncode, 1)
        self.assertIn("cannot set source_required to false", result.stdout)

    def test_manifest_rejects_a_string_side_material_list(self) -> None:
        manifest = elsevier_manifest()
        manifest["side_materials"] = "highlights.docx"
        result = self.run_check(manifest)
        self.assertEqual(result.returncode, 1)
        self.assertIn("side_materials must be a json array", result.stdout.lower())

    def test_comments_cannot_satisfy_statement_headings(self) -> None:
        (self.base / "main.tex").write_text(
            "\\begin{abstract}Short abstract.\\end{abstract}\n"
            "% \\section*{CRediT authorship contribution statement}\n"
            "\\section*{Declaration of competing interest}\n"
            "\\section*{Acknowledgements and Funding}\n"
            "\\section*{Data availability}\n",
            encoding="utf-8",
        )
        result = self.run_check(elsevier_manifest())
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing required statement heading: credit", result.stdout.lower())

    def test_statement_order_is_enforced(self) -> None:
        (self.base / "main.tex").write_text(
            "\\begin{abstract}Short abstract.\\end{abstract}\n"
            "\\section*{Data availability}\n"
            "\\section*{CRediT authorship contribution statement}\n"
            "\\section*{Declaration of competing interest}\n"
            "\\section*{Acknowledgements and Funding}\n",
            encoding="utf-8",
        )
        result = self.run_check(elsevier_manifest())
        self.assertEqual(result.returncode, 1)
        self.assertIn("not in the required order", result.stdout.lower())

    def test_highlight_character_limit_is_enforced(self) -> None:
        write_minimal_docx(
            self.base / "highlights.docx",
            ["Highlights", "x" * 86, "Second result", "Third result"],
        )
        result = self.run_check(elsevier_manifest())
        self.assertEqual(result.returncode, 1)
        self.assertIn("maximum is 85", result.stdout.lower())

    def test_invalid_docx_container_is_rejected(self) -> None:
        with zipfile.ZipFile(self.base / "highlights.docx", "w") as archive:
            archive.writestr("[Content_Types].xml", "<Types />")
            archive.writestr("_rels/.rels", "<Relationships />")
            archive.writestr("word/document.xml", "<document />")
        result = self.run_check(elsevier_manifest())
        self.assertEqual(result.returncode, 1)
        self.assertIn("lacks a valid word document", result.stdout.lower())

    def test_stale_evidence_date_fails(self) -> None:
        manifest = elsevier_manifest()
        manifest["journal_limits_checked_on"] = "2020-01-01"
        result = self.run_check(manifest)
        self.assertEqual(result.returncode, 1)
        self.assertIn("journal_limits_checked_on is", result.stdout)


class IeeePacketTests(PacketCheckTestCase):
    def setUp(self) -> None:
        super().setUp()
        write_ieee_manuscript(self.base / "main.tex", abstract_words=200)
        write_pdf(self.base / "manuscript.pdf", pages=10)

    @unittest.skipUnless(shutil.which("pdfinfo"), "pdfinfo unavailable")
    def test_valid_initial_packet_passes(self) -> None:
        result = self.run_check(ieee_manifest())
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("ieee packet check passed", result.stdout)

    def test_unknown_manifest_key_fails(self) -> None:
        manifest = ieee_manifest()
        manifest["responseto_reviewers"] = "response.pdf"
        result = self.run_check(manifest)
        self.assertEqual(result.returncode, 1)
        self.assertIn("unknown manifest key(s) for ieee: responseto_reviewers", result.stdout)

    def test_missing_edics_fails(self) -> None:
        manifest = ieee_manifest()
        manifest["edics"] = []
        result = self.run_check(manifest)
        self.assertEqual(result.returncode, 1)
        self.assertIn("edics must be a non-empty JSON array", result.stdout)

    @unittest.skipUnless(shutil.which("pdfinfo"), "pdfinfo unavailable")
    def test_abstract_below_range_fails(self) -> None:
        write_ieee_manuscript(self.base / "main.tex", abstract_words=120)
        result = self.run_check(ieee_manifest())
        self.assertEqual(result.returncode, 1)
        self.assertIn("abstract has 120 words; live journal range is 150-250", result.stdout)

    @unittest.skipUnless(shutil.which("pdfinfo"), "pdfinfo unavailable")
    def test_overlength_manuscript_pdf_fails(self) -> None:
        write_pdf(self.base / "manuscript.pdf", pages=11)
        result = self.run_check(ieee_manifest())
        self.assertEqual(result.returncode, 1)
        self.assertIn("manuscript PDF has 11 pages; live journal maximum is 10", result.stdout)

    @unittest.skipUnless(shutil.which("pdfinfo"), "pdfinfo unavailable")
    def test_supplemental_pdf_over_limit_fails(self) -> None:
        write_pdf(self.base / "supplemental.pdf", pages=5)
        manifest = ieee_manifest()
        manifest["supplemental_pdf"] = "supplemental.pdf"
        manifest["journal_limits"]["supplemental_max_pages"] = 4
        result = self.run_check(manifest)
        self.assertEqual(result.returncode, 1)
        self.assertIn("supplemental PDF has 5 pages; live journal maximum is 4", result.stdout)

    def test_supplemental_pdf_requires_recorded_limit(self) -> None:
        write_pdf(self.base / "supplemental.pdf", pages=2)
        manifest = ieee_manifest()
        manifest["supplemental_pdf"] = "supplemental.pdf"
        result = self.run_check(manifest)
        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "journal_limits.supplemental_max_pages must be a positive integer", result.stdout
        )

    def test_revision_without_response_fails(self) -> None:
        manifest = ieee_manifest()
        manifest["submission_stage"] = "revision"
        result = self.run_check(manifest)
        self.assertEqual(result.returncode, 1)
        self.assertIn("response_to_reviewers must be a non-empty path", result.stdout)

    def test_missing_difference_statement_fails(self) -> None:
        manifest = ieee_manifest()
        manifest["difference_statement"] = "diff.pdf"
        result = self.run_check(manifest)
        self.assertEqual(result.returncode, 1)
        self.assertIn("difference_statement is missing", result.stdout)

    def test_final_step_cannot_disable_source(self) -> None:
        manifest = ieee_manifest()
        manifest["submission_step"] = "final files source upload"
        result = self.run_check(manifest)
        self.assertEqual(result.returncode, 1)
        self.assertIn("cannot set source_required to false", result.stdout)

    def test_missing_pdfinfo_blocks_instead_of_passing(self) -> None:
        env = os.environ.copy()
        env["PATH"] = "/nonexistent"
        result = self.run_check(ieee_manifest(), env=env)
        self.assertEqual(result.returncode, 2)
        self.assertIn("page-count check is blocked", result.stdout)
        self.assertIn("pdfinfo", result.stdout)


if __name__ == "__main__":
    unittest.main()
