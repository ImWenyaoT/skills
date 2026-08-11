"""Contracts every script that ships inside a skill has to meet.

These scripts run on other people's machines — conda, a plain virtualenv, a
system Python, sometimes no uv at all. A bare ModuleNotFoundError traceback tells
that user nothing they can act on, and the repository already has a better
convention for it: name what is missing, name how to install it, and exit 2 to
mean "blocked", not "failed".
"""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Packages a shipped script may import that are not in the standard library. The
# list is explicit rather than inferred: a typo in an import should show up as an
# unguarded dependency, not be silently classed as stdlib.
THIRD_PARTY = {
    "matplotlib",
    "numpy",
    "PIL",
    "docx",
    "torch",
    "thop",
    "fitz",
    "pandas",
}


def shipped_scripts() -> list[Path]:
    """Every Python file that installs onto a user's machine with a skill."""
    return sorted(
        path
        for path in ROOT.glob("skills/*/scripts/**/*.py")
        if "__pycache__" not in path.parts and path.name != "__init__.py"
    )


def third_party_imports(tree: ast.Module) -> set[str]:
    """The top-level package name of every third-party import in the file."""
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [node.module or ""]
        else:
            continue
        for name in names:
            root = name.split(".")[0]
            if root in THIRD_PARTY:
                found.add(root)
    return found


class ShippedScriptContracts(unittest.TestCase):
    def test_there_are_shipped_scripts_to_check(self) -> None:
        """Guards against the glob silently matching nothing."""
        self.assertTrue(shipped_scripts())

    def test_every_third_party_import_is_guarded(self) -> None:
        """An unguarded import gives a user a traceback instead of an instruction."""
        offenders = []
        for path in shipped_scripts():
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source)
            if not third_party_imports(tree):
                continue
            guarded = any(
                isinstance(node, ast.Try)
                and any(
                    isinstance(handler.type, ast.Name)
                    and handler.type.id in {"ImportError", "ModuleNotFoundError"}
                    for handler in node.handlers
                )
                for node in ast.walk(tree)
            )
            if not guarded:
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [], "third-party imports with no guard")

    def test_the_guard_names_more_than_one_installer(self) -> None:
        """uv is not installed everywhere; conda and pip users get told what to run."""
        offenders = []
        for path in shipped_scripts():
            source = path.read_text(encoding="utf-8")
            if not third_party_imports(ast.parse(source)):
                continue
            lowered = source.lower()
            if not ("pip install" in lowered and "conda install" in lowered):
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [], "guards that name only one way to install")

    def test_a_missing_dependency_exits_two(self) -> None:
        """Exit 2 already means "blocked, not failed" for missing binaries here."""
        offenders = []
        for path in shipped_scripts():
            source = path.read_text(encoding="utf-8")
            if not third_party_imports(ast.parse(source)):
                continue
            if "SystemExit(2)" not in source and "sys.exit(2)" not in source:
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [], "guards that do not exit 2")


class GuardBehaviourTests(unittest.TestCase):
    """Run one guard for real. The structural tests above passed while the message
    printed a literal backslash-n and the word "None" where the package should be."""

    SCRIPT = ROOT / "skills" / "drawing-figures" / "scripts" / "stitch.py"

    def run_with_import_blocked(self, *blocked: str):
        import subprocess
        import sys

        program = (
            "import sys\n"
            "class Block:\n"
            "    def find_spec(self, name, path=None, target=None):\n"
            f"        if name.split('.')[0] in {blocked!r}:\n"
            "            raise ImportError(name)\n"
            "        return None\n"
            "sys.meta_path.insert(0, Block())\n"
            "import runpy\n"
            f"runpy.run_path({str(self.SCRIPT)!r}, run_name='__main__')\n"
        )
        return subprocess.run(
            [sys.executable, "-c", program], capture_output=True, text=True, cwd=ROOT
        )

    def test_a_blocked_import_exits_two_with_an_actionable_message(self) -> None:
        result = self.run_with_import_blocked("PIL")
        self.assertEqual(result.returncode, 2, result.stderr)
        message = result.stderr
        self.assertIn("pip install pillow", message)
        self.assertIn("conda install pillow", message)
        self.assertIn("uv run --with pillow", message)

    def test_the_message_has_no_literal_escapes_and_names_the_package(self) -> None:
        """Both of these shipped once: a literal backslash-n, and "None is needed"."""
        message = self.run_with_import_blocked("PIL").stderr
        self.assertNotIn("\\n", message)
        self.assertNotIn("None is needed", message)
        self.assertTrue(message.startswith("pillow is needed"), message[:80])


if __name__ == "__main__":
    unittest.main()
