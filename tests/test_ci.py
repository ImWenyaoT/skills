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

    def test_python_files_skips_the_virtualenv(self) -> None:
        """uv builds .venv inside the repo; compiling its thousands of files is not a check."""
        self.assertFalse([f for f in ci.python_files() if f.startswith(".venv")])
        self.assertFalse([f for f in ci.python_files() if f.split("/")[0].startswith(".")])

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


class DependencyDeclarationTests(unittest.TestCase):
    """Given the project declares its dependencies, then it does so in one place."""

    def test_dev_dependencies_live_in_pyproject(self) -> None:
        import tomllib

        pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        group = pyproject["dependency-groups"]["dev"]
        joined = " ".join(group)
        for package in ("coverage", "matplotlib", "pillow", "ruff", "ty"):
            self.assertIn(package, joined.lower())

    def test_requirements_txt_is_gone(self) -> None:
        """uv reads pyproject; a second dependency file is a second thing to drift."""
        self.assertFalse((ROOT / "requirements-ci.txt").exists())


class LintAndTypeTests(unittest.TestCase):
    """Given ruff and ty are the chosen tools, then ci.py must actually run them."""

    def test_the_plan_lints_formats_and_type_checks(self) -> None:
        plan = ci.checks(with_coverage=False)
        flat = [" ".join(cmd) for _, cmd in plan]
        self.assertTrue(any("ruff check" in cmd for cmd in flat))
        self.assertTrue(any("ruff format" in cmd and "--check" in cmd for cmd in flat))
        self.assertTrue(any("ty check" in cmd for cmd in flat))

    def test_format_check_does_not_rewrite_files(self) -> None:
        """A check that edits the tree turns a red build green without telling you."""
        plan = dict(ci.checks(with_coverage=False))
        fmt = [cmd for name, cmd in plan.items() if "format" in name.lower()][0]
        self.assertIn("--check", fmt)


class InterpreterTests(unittest.TestCase):
    def setUp(self) -> None:
        self._which = ci.shutil.which
        self.addCleanup(setattr, ci.shutil, "which", self._which)

    def test_uv_supplies_the_dependencies_and_pins_the_interpreter(self) -> None:
        ci.shutil.which = lambda name: "/usr/bin/uv" if name == "uv" else None
        argv = ci.interpreter()
        self.assertEqual(argv[:2], ["uv", "run"])
        self.assertIn("--group", argv)
        self.assertIn("dev", argv)
        # Without --python, a CI matrix over several versions would test one.
        self.assertIn("--python", argv)
        self.assertIn(sys.executable, argv)

    def test_without_uv_it_falls_back_to_this_interpreter(self) -> None:
        ci.shutil.which = lambda name: None
        self.assertEqual(ci.interpreter(), [sys.executable])

    def test_stdlib_only_checks_do_not_go_through_uv(self) -> None:
        ci.shutil.which = lambda name: "/usr/bin/uv" if name == "uv" else None
        plan = dict(ci.checks(with_coverage=False))
        self.assertEqual(plan["Skill frontmatter and structure"][0], sys.executable)
        tests = [cmd for name, cmd in ci.checks(False) if name.startswith("Tests:")][0]
        self.assertEqual(tests[0], "uv")


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
        self.assertEqual(discovery.expected_count(), len(list(ROOT.glob("skills/*/SKILL.md"))))

    def test_ansi_is_stripped_before_matching(self) -> None:
        self.assertEqual(discovery.ANSI.sub("", "\x1b[32mFound 4 skills\x1b[0m"), "Found 4 skills")


if __name__ == "__main__":
    unittest.main()


class EntryPointDocTests(unittest.TestCase):
    """AGENTS.md was silently emptied of 172 of its 173 lines by a tool whose commit
    message said it was adding conventions. Every check stayed green: the only one
    that reads the file compares it to CLAUDE.md, and a symlink to an empty file is
    still identical to itself."""

    def test_agents_md_does_not_import_itself(self) -> None:
        """`@AGENTS.md` is how CLAUDE.md includes it; inside AGENTS.md it is a loop."""
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertNotIn("@AGENTS.md", text)

    def test_agents_md_points_at_the_conventions(self) -> None:
        """Short is a choice; losing the rules is not. The pointer has to resolve."""
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("docs/development.md", text)
        self.assertTrue((ROOT / "docs" / "development.md").is_file())

    def test_the_conventions_still_carry_the_load_bearing_rules(self) -> None:
        """A file that exists but was gutted passes a file-exists check."""
        text = (ROOT / "docs" / "development.md").read_text(encoding="utf-8")
        for rule in ("黄金法则", "触发测试", "VALIDATION_FLOOR", "TIE_RATIO", "先写会失败的测试"):
            self.assertIn(rule, text, f"development.md no longer mentions {rule}")
