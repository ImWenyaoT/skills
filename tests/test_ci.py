from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(name: str):
    """Import a repository script by path, the way the other tests here do."""
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ci = _load("ci")
discovery = _load("check_cli_discovery")


class CheckPlanTests(unittest.TestCase):
    def test_test_suites_are_discovered_not_listed(self) -> None:
        """A new skill's tests must run without anyone editing this script."""
        suites = ci.test_suites()
        self.assertIn(ROOT / "tests", suites)
        for shipped in ROOT.glob("skills/*/tests"):
            self.assertIn(shipped, suites)

    def test_python_files_skips_caches(self) -> None:
        files = ci.python_files()
        self.assertTrue(files)
        self.assertFalse([f for f in files if "__pycache__" in f])
        self.assertIn("scripts/ci.py", files)

    def test_plan_covers_the_checks_ci_depends_on(self) -> None:
        names = [name for name, _ in ci.checks(with_coverage=False)]
        self.assertTrue(any("frontmatter" in n for n in names))
        self.assertTrue(any("Trigger" in n for n in names))
        self.assertTrue(any("symlink" in n for n in names))
        self.assertTrue(any("compiles" in n for n in names))
        self.assertFalse(any("coverage" in n.lower() for n in names))

    def test_coverage_is_opt_in(self) -> None:
        names = [name for name, _ in ci.checks(with_coverage=True)]
        self.assertTrue(any("coverage" in n.lower() for n in names))
        report = [cmd for name, cmd in ci.checks(True) if name.endswith("report")][0]
        self.assertIn(f"--fail-under={ci.COVERAGE_FLOOR}", report)
        # The XML export existed only to be uploaded as an artefact nobody read.
        self.assertFalse([c for _, c in ci.checks(True) if "xml" in c])


class ExitCodeTests(unittest.TestCase):
    def setUp(self) -> None:
        self._run = ci.run
        self.addCleanup(setattr, ci, "run", self._run)

    def main(self) -> int:
        """Call ci.main with its summary captured, so a passing suite stays quiet.

        Left uncaptured, the stubbed runs print a summary that reads exactly like a
        real failure report in the middle of the test output.
        """
        with contextlib.redirect_stdout(io.StringIO()):
            return ci.main([])

    def test_every_check_runs_even_after_one_fails(self) -> None:
        """A shell script with `set -e` stopped at the first failure; this must not."""
        seen: list[str] = []

        def fake(name: str, argv: list[str]) -> bool:
            seen.append(name)
            return "Trigger" not in name

        ci.run = fake
        self.assertEqual(self.main(), 1)
        self.assertEqual(len(seen), len(ci.checks(with_coverage=False)))

    def test_all_green_exits_zero(self) -> None:
        ci.run = lambda name, argv: True
        self.assertEqual(self.main(), 0)


class DiscoveryTests(unittest.TestCase):
    def test_expected_count_comes_from_the_filesystem(self) -> None:
        self.assertEqual(
            discovery.expected_count(), len(list(ROOT.glob("skills/*/SKILL.md")))
        )

    def test_ansi_is_stripped_before_matching(self) -> None:
        self.assertEqual(discovery.ANSI.sub("", "\x1b[32mFound 4 skills\x1b[0m"),
                         "Found 4 skills")


if __name__ == "__main__":
    unittest.main()
