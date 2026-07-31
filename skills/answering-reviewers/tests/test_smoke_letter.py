"""Tests for the response-letter template smoke.

The point of the smoke is that a partial TeX install fails loudly and
distinguishably, so these tests pin the diagnosis, not the compile.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT / "scripts"))

import smoke_letter  # noqa: E402


class DoctorTests(unittest.TestCase):
    def test_missing_pdflatex_names_the_binary(self) -> None:
        """No LaTeX at all must name pdflatex rather than fail during compile."""
        with mock.patch.object(smoke_letter.shutil, "which", return_value=None):
            strategy, problems = smoke_letter.doctor()
        self.assertIsNone(strategy)
        self.assertIn("pdflatex", "".join(problems))

    def test_missing_package_names_the_package(self) -> None:
        """A partial TeX install must point at the package, not at a LaTeX error."""
        with mock.patch.object(smoke_letter.shutil, "which", side_effect=lambda name: f"/bin/{name}"), \
             mock.patch.object(smoke_letter, "_style_found", return_value=False):
            strategy, problems = smoke_letter.doctor()
        self.assertIsNone(strategy)
        self.assertIn("tcolorbox.sty", "".join(problems))

    def test_runtime_problem_exits_two_not_zero(self) -> None:
        """An unusable runtime must not read as a pass."""
        with mock.patch.object(smoke_letter, "doctor", return_value=(None, ["broken"])):
            self.assertEqual(smoke_letter.main([]), 2)

    def test_missing_template_exits_one(self) -> None:
        """A template directory without main.tex is a broken template, not a runtime gap."""
        self.assertEqual(smoke_letter.main(["--template", str(ROOT / "assets")]), 1)


if __name__ == "__main__":
    unittest.main()
