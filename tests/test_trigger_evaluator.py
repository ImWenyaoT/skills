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

    def test_cjk_bigrams_stay_inside_one_run(self) -> None:
        tokens = evaluator.tokenize("写摘要, 写引言")
        self.assertIn("摘要", tokens)
        self.assertIn("写引", tokens)
        self.assertNotIn("要写", tokens)  # would span the comma

    def test_split_description_matches_both_boundary_phrasings(self) -> None:
        for description in (
            "Alpha routing. Do not use for beta work.",
            "Alpha routing. Does not apply to beta work.",
        ):
            positive, negative = evaluator.split_description(description)
            self.assertEqual(positive.strip(), "Alpha routing.")
            self.assertIn("beta", negative)
        self.assertEqual(evaluator.split_description("Alpha only"), ("Alpha only", ""))

    def test_split_ignores_a_mid_sentence_negation(self) -> None:
        """A symptom list says "the loss does not decrease" — that is not a boundary."""
        described = "Use when a run goes wrong: the loss does not decrease. Do not use for tables."
        positive, negative = evaluator.split_description(described)
        self.assertIn("decrease", positive)
        self.assertEqual(negative, "Do not use for tables.")

    def test_antiscope_tokens_drop_words_shared_with_the_positive_half(self) -> None:
        skill = self.skill("alpha-skill", "Alpha routing. Do not use for alpha invoices.")
        self.assertIn("invoices", evaluator.antiscope_tokens(skill))
        self.assertNotIn("alpha", evaluator.antiscope_tokens(skill))
        self.assertNotIn("for", evaluator.antiscope_tokens(skill))  # matches every prompt

    def test_antiscope_must_exist_and_be_exercised(self) -> None:
        skills = {"alpha-skill": self.skill("alpha-skill", "Alpha routing with no boundary")}
        case = evaluator.Case("one", "alpha", (), ("alpha-skill",), "")
        self.assertTrue(
            any("declares no anti-scope" in f for f in evaluator.validate_antiscope([case], skills))
        )

        skills = {"alpha-skill": self.skill("alpha-skill", "Alpha routing. Do not use for invoices.")}
        untested = evaluator.Case("one", "alpha routing please", (), ("alpha-skill",), "")
        self.assertTrue(
            any("no forbidden case exercises" in f
                for f in evaluator.validate_antiscope([untested], skills))
        )
        tested = evaluator.Case("two", "fix my invoices", (), ("alpha-skill",), "")
        self.assertEqual(evaluator.validate_antiscope([untested, tested], skills), [])

    def test_smoke_stays_silent_inside_the_tie_band(self) -> None:
        skills = {
            "alpha-skill": self.skill("alpha-skill", "shared routing alpha. Do not use for x."),
            "beta-skill": self.skill("beta-skill", "shared routing beta. Do not use for y."),
        }
        # "shared routing" hits both almost equally: a verdict here would read noise.
        tie = evaluator.Case("tie", "shared routing", ("beta-skill",), ("alpha-skill",), "")
        self.assertEqual(evaluator.smoke_test_metadata([tie], skills), [])
        # A prompt made only of alpha's own words is outside the band and must fail.
        clear = evaluator.Case("clear", "alpha alpha", ("beta-skill",), (), "")
        self.assertTrue(evaluator.smoke_test_metadata([clear], skills))

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
