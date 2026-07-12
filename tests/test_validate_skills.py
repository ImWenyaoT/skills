from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_skills.py"
SPEC = importlib.util.spec_from_file_location("validate_skills", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ValidateSkillsTests(unittest.TestCase):
    def run_validator(self, files: dict[str, str]) -> tuple[int, list[str], list[str]]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for relative, content in files.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            old_root = validator.ROOT
            validator.ROOT = str(root)
            validator.errors.clear()
            validator.warnings.clear()
            try:
                code = validator.main()
                return code, list(validator.errors), list(validator.warnings)
            finally:
                validator.ROOT = old_root
                validator.errors.clear()
                validator.warnings.clear()

    def test_accepts_valid_skill_with_quoted_colon(self) -> None:
        code, errors, warnings = self.run_validator(
            {"good-skill/SKILL.md": "---\nname: good-skill\ndescription: 'Review: safely.'\n---\n# Good\n"}
        )
        self.assertEqual((code, errors, warnings), (0, [], []))

    def test_rejects_unquoted_description_colon(self) -> None:
        code, errors, _ = self.run_validator(
            {"bad-skill/SKILL.md": "---\nname: bad-skill\ndescription: Review: safely.\n---\n# Bad\n"}
        )
        self.assertEqual(code, 1)
        self.assertTrue(any("YAML" in error for error in errors))

    def test_rejects_directory_name_mismatch_and_invalid_name(self) -> None:
        code, errors, _ = self.run_validator(
            {"folder-name/SKILL.md": "---\nname: Bad_Name\ndescription: bad\n---\n# Bad\n"}
        )
        self.assertEqual(code, 1)
        self.assertTrue(any("目录名不一致" in error for error in errors))
        self.assertTrue(any("非法字符" in error for error in errors))

    def test_warns_when_long_reference_has_no_contents(self) -> None:
        reference = "\n".join(f"line {index}" for index in range(101))
        code, errors, warnings = self.run_validator(
            {
                "good-skill/SKILL.md": "---\nname: good-skill\ndescription: good\n---\n# Good\n",
                "good-skill/references/long.md": reference,
            }
        )
        self.assertEqual((code, errors), (0, []))
        self.assertEqual(len(warnings), 1)


if __name__ == "__main__":
    unittest.main()
