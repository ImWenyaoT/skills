from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "smoke_template.py"
PUBLISHERS = ("elsevier", "ieee")


def run_smoke(publisher: str, env: dict) -> subprocess.CompletedProcess[str]:
    """Invoke the smoke CLI for one publisher with a controlled PATH."""
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--publisher", publisher],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


class TemplateSmokeTests(unittest.TestCase):
    def test_missing_runtime_reports_install_next_step(self) -> None:
        env = os.environ.copy()
        env["PATH"] = "/nonexistent"
        for publisher in PUBLISHERS:
            with self.subTest(publisher=publisher):
                result = run_smoke(publisher, env)
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
            for publisher in PUBLISHERS:
                with self.subTest(publisher=publisher):
                    result = run_smoke(publisher, env)
                    self.assertEqual(result.returncode, 2)
                    self.assertIn("pdflatex", result.stdout)
                    self.assertIn("bibtex", result.stdout)

    def test_missing_package_names_the_publisher_package(self) -> None:
        """A runtime without the class file must name that package, not pass silently."""
        with tempfile.TemporaryDirectory() as tmp:
            bindir = Path(tmp)
            for name in ("pdflatex", "bibtex", "kpsewhich"):
                stub = bindir / name
                stub.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
                stub.chmod(0o755)
            env = os.environ.copy()
            env["PATH"] = str(bindir)
            expected = {"elsevier": "elsarticle", "ieee": "IEEEtran"}
            for publisher in PUBLISHERS:
                with self.subTest(publisher=publisher):
                    result = run_smoke(publisher, env)
                    self.assertEqual(result.returncode, 2)
                    self.assertIn("LaTeX package unavailable", result.stdout)
                    self.assertIn(expected[publisher], result.stdout)

    def test_publisher_is_required(self) -> None:
        """Without a publisher there is no template to probe; refuse rather than guess."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--publisher", result.stderr)


if __name__ == "__main__":
    unittest.main()
