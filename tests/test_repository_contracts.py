from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractTests(unittest.TestCase):
    def test_readme_language_switches_resolve(self) -> None:
        for name in ("README.md", "README.en.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("[简体中文](README.md) | [English](README.en.md)", text)

    def test_every_skill_has_trigger_coverage(self) -> None:
        completed = subprocess.run(
            [sys.executable, "scripts/evaluate_skill_triggers.py", "--skip-smoke"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("Loaded 19 skills", completed.stdout)

    def test_repository_skills_pass_structure_validation(self) -> None:
        completed = subprocess.run(
            [sys.executable, "scripts/validate_skills.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("19 个 skill", completed.stdout)


if __name__ == "__main__":
    unittest.main()
