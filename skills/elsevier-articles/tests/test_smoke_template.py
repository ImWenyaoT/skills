from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TemplateSmokeTests(unittest.TestCase):
    def test_missing_runtime_reports_install_next_step(self) -> None:
        env = os.environ.copy()
        env["PATH"] = "/nonexistent"
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "smoke_template.py")],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("LaTeX runtime unavailable", result.stdout)
        self.assertIn("install", result.stdout.lower())

    def test_partial_runtime_reports_missing_engine_and_bibtex(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bindir = Path(tmp)
            latexmk = bindir / "latexmk"
            latexmk.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            latexmk.chmod(0o755)
            env = os.environ.copy()
            env["PATH"] = str(bindir)
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "smoke_template.py")],
                capture_output=True,
                text=True,
                env=env,
                check=False,
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("pdflatex", result.stdout)
        self.assertIn("bibtex", result.stdout)


if __name__ == "__main__":
    unittest.main()
