from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "evaluate_skill_triggers.py"
SPEC = importlib.util.spec_from_file_location("trigger_evaluator", MODULE_PATH)
assert SPEC and SPEC.loader
evaluator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = evaluator
SPEC.loader.exec_module(evaluator)


class TriggerEvaluatorTests(unittest.TestCase):
    def skill(self, name: str, description: str, user_invoked: bool = False):
        return evaluator.Skill(name, Path(f"/{name}/SKILL.md"), description, user_invoked)

    def test_tokenize_supports_words_and_cjk_bigrams(self) -> None:
        tokens = evaluator.tokenize("Debug training 梯度异常")
        self.assertIn("debug", tokens)
        self.assertIn("梯度", tokens)
        self.assertIn("异常", tokens)

    def test_user_invoked_skill_only_ranks_when_named(self) -> None:
        skills = {
            "paper-workflow": self.skill("paper-workflow", "paper workflow", True),
            "writing-papers": self.skill("writing-papers", "polish academic papers"),
        }
        unnamed = [name for name, _ in evaluator.rank_skills("polish my paper", skills)]
        named = [name for name, _ in evaluator.rank_skills("run paper workflow", skills)]
        self.assertNotIn("paper-workflow", unnamed)
        self.assertIn("paper-workflow", named)

    def test_contract_requires_two_positive_and_negative_cases(self) -> None:
        skills = {"alpha-skill": self.skill("alpha-skill", "alpha")}
        case = evaluator.Case("one", "alpha", ("alpha-skill",), (), "")
        failures = evaluator.validate_case_contract([case], skills)
        self.assertIn("alpha-skill: needs at least 2 positive trigger cases", failures)
        self.assertIn("alpha-skill: needs at least 2 forbidden/negative cases", failures)

    def test_contract_rejects_unknown_and_conflicting_labels(self) -> None:
        skills = {"alpha-skill": self.skill("alpha-skill", "alpha")}
        case = evaluator.Case("bad", "alpha", ("alpha-skill", "missing"), ("alpha-skill",), "")
        failures = evaluator.validate_case_contract([case, case], skills)
        self.assertTrue(any("duplicate case id" in failure for failure in failures))
        self.assertTrue(any("unknown skills" in failure for failure in failures))
        self.assertTrue(any("both expected and forbidden" in failure for failure in failures))






    def test_load_cases_reads_optional_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cases.json"
            path.write_text(
                json.dumps(
                    {
                        "cases": [
                            {
                                "id": "one",
                                "prompt": "alpha",
                                "expected_skills": ["alpha-skill"],
                                "forbidden_skills": ["beta-skill"],
                                "notes": "edge",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            cases = evaluator.load_cases(path)
        self.assertEqual(cases[0].expected_skills, ("alpha-skill",))
        self.assertEqual(cases[0].forbidden_skills, ("beta-skill",))
        self.assertEqual(cases[0].notes, "edge")

    def test_parse_frontmatter_handles_quotes_and_missing_delimiter(self) -> None:
        parsed = evaluator.parse_frontmatter(
            "---\nname: alpha-skill\ndescription: 'Alpha skill'\n---\n# Alpha\n"
        )
        self.assertEqual(parsed["description"], "Alpha skill")
        self.assertEqual(evaluator.parse_frontmatter("# no frontmatter"), {})
        self.assertEqual(evaluator.parse_frontmatter("---\nname: broken"), {})

    def test_smoke_test_accepts_matching_metadata_and_skips_named_orchestrator(self) -> None:
        skills = {
            "alpha-skill": self.skill("alpha-skill", "alpha routing"),
            "paper-workflow": self.skill("paper-workflow", "paper workflow", True),
        }
        cases = [
            evaluator.Case("alpha", "alpha routing", ("alpha-skill",), (), ""),
            evaluator.Case("orchestrator", "run paper workflow", ("paper-workflow",), (), ""),
        ]
        self.assertEqual(evaluator.smoke_test_metadata(cases, skills), [])

    def test_main_rejects_case_file_with_incomplete_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cases.json"
            path.write_text(
                json.dumps({"cases": [{"id": "one", "prompt": "x", "expected_skills": ["writing-papers"]}]}),
                encoding="utf-8",
            )
            code = evaluator.main(["--cases", str(path), "--skip-smoke"])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
