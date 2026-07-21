"""Tests for the response-letter generator."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_letter.py"

sys.path.insert(0, str(ROOT / "scripts"))

from render_letter import escape_latex, main  # noqa: E402


PAGE = """<!doctype html>
<html lang="zh"><body>
<article class="comment-card" data-comment-id="E-1" data-status="doing">
  <div class="verbatim">Please distinguish the method from prior work &amp; resolve the gap.</div>
  <div class="translation">请把方法与既有工作区分开。</div>
  <div class="response-draft">We have clarified the distinction in Sec. 1.</div>
</article>
<article class="comment-card" data-comment-id="R1-1" data-status="done" data-choice="B">
  <div class="verbatim">The reported PSNR is 23.5 while the original paper reports 28.2.</div>
  <div class="response-draft">We reproduced the baseline with official weights.</div>
  <div class="manuscript-change">Table 2 now reports 28.1 dB under the corrected protocol.</div>
  <div class="location">Sec. 4.2, Table 2</div>
</article>
<article class="comment-card" data-comment-id="R1-2" data-status="todo">
  <div class="verbatim">Only <strong>concrete</strong> evidence at 95% coverage will convince.</div>
</article>
</body></html>
"""


class EscapeLatexTests(unittest.TestCase):
    def test_escapes_every_special_character(self) -> None:
        """Each LaTeX special must survive as literal text."""
        self.assertEqual(escape_latex("95% & $x$ #1 a_b {c} ~ ^"),
                         r"95\% \& \$x\$ \#1 a\_b \{c\} \textasciitilde{} \textasciicircum{}")

    def test_backslash_does_not_double_escape(self) -> None:
        """A backslash becomes a command that later replacements leave alone."""
        self.assertEqual(escape_latex("a\\b"), r"a\textbackslash{}b")

    def test_plain_text_is_unchanged(self) -> None:
        """Text without specials passes through untouched."""
        self.assertEqual(escape_latex("The PSNR is 23.5 dB."), "The PSNR is 23.5 dB.")


class RenderLetterTests(unittest.TestCase):
    def render(self, page: str) -> tuple[int, Path]:
        """Run the generator over one page and return the exit code and out dir."""
        directory = Path(tempfile.mkdtemp())
        page_path = directory / "revision.html"
        page_path.write_text(page, encoding="utf-8")
        out = directory / "letter"
        code = main([str(page_path), "--out", str(out)])
        return code, out

    def test_groups_cards_by_reviewer(self) -> None:
        """The editor and each reviewer get their own file."""
        code, out = self.render(PAGE)
        self.assertEqual(code, 0)
        self.assertTrue((out / "Reviewers" / "Editor.tex").is_file())
        self.assertTrue((out / "Reviewers" / "R1.tex").is_file())

    def test_editor_uses_editor_environments(self) -> None:
        """Editor cards must not emit reviewer environments."""
        _, out = self.render(PAGE)
        text = (out / "Reviewers" / "Editor.tex").read_text(encoding="utf-8")
        self.assertIn(r"\begin{editorcomment}", text)
        self.assertIn(r"\begin{editorresponse}", text)
        self.assertNotIn(r"\startReviewerSection", text)

    def test_reviewer_file_opens_a_section(self) -> None:
        """A reviewer file opens its section so the counter resets."""
        _, out = self.render(PAGE)
        text = (out / "Reviewers" / "R1.tex").read_text(encoding="utf-8")
        self.assertIn(r"\startReviewerSection{Reviewer \#1}", text)

    def test_preserves_document_order(self) -> None:
        """Card order sets the printed numbering, so it must not be sorted."""
        _, out = self.render(PAGE)
        text = (out / "Reviewers" / "R1.tex").read_text(encoding="utf-8")
        self.assertLess(text.index("R1-1"), text.index("R1-2"))

    def test_escapes_verbatim_specials(self) -> None:
        """A percent sign in the reviewer's words must not comment out the line."""
        _, out = self.render(PAGE)
        text = (out / "Reviewers" / "R1.tex").read_text(encoding="utf-8")
        self.assertIn(r"95\% coverage", text)

    def test_html_entity_becomes_plain_text(self) -> None:
        """An HTML entity is decoded, then escaped for LaTeX."""
        _, out = self.render(PAGE)
        text = (out / "Reviewers" / "Editor.tex").read_text(encoding="utf-8")
        self.assertIn(r"prior work \& resolve", text)

    def test_bold_markup_inside_verbatim_is_flattened(self) -> None:
        """A bolded forceful word survives as text, not as markup."""
        _, out = self.render(PAGE)
        text = (out / "Reviewers" / "R1.tex").read_text(encoding="utf-8")
        self.assertIn("Only concrete evidence", text)

    def test_manuscript_change_becomes_changes_block(self) -> None:
        """A revised-text field nests inside the response."""
        _, out = self.render(PAGE)
        text = (out / "Reviewers" / "R1.tex").read_text(encoding="utf-8")
        self.assertIn(r"\begin{changes}", text)
        self.assertIn("Table 2 now reports 28.1 dB", text)

    def test_missing_draft_leaves_a_visible_placeholder(self) -> None:
        """An undrafted response must be obvious in the output."""
        _, out = self.render(PAGE)
        text = (out / "Reviewers" / "R1.tex").read_text(encoding="utf-8")
        self.assertIn("{{RESPONSE-TO-R1-2}}", text)

    def test_empty_verbatim_is_refused(self) -> None:
        """A comment block that quotes nothing must stop the run."""
        page = (
            '<article class="comment-card" data-comment-id="R2-1">'
            '<div class="verbatim"></div></article>'
        )
        with self.assertRaises(SystemExit) as caught:
            self.render(page)
        self.assertIn("verbatim field is empty", str(caught.exception))

    def test_card_without_id_is_refused(self) -> None:
        """A card with no id cannot be placed in the letter."""
        page = '<article class="comment-card"><div class="verbatim">x</div></article>'
        with self.assertRaises(SystemExit) as caught:
            self.render(page)
        self.assertIn("data-comment-id", str(caught.exception))

    def test_page_without_cards_exits_nonzero(self) -> None:
        """An unrecognized page fails loudly instead of writing nothing."""
        code, _ = self.render("<html><body><p>no cards here</p></body></html>")
        self.assertEqual(code, 1)


class CliTests(unittest.TestCase):
    def test_runs_as_a_script(self) -> None:
        """The documented command line works end to end."""
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            page = directory / "revision.html"
            page.write_text(PAGE, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(page), "--out", str(directory / "letter")],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("2/3 comments carry a response draft", result.stdout)


if __name__ == "__main__":
    unittest.main()
