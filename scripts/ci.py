#!/usr/bin/env python3
"""Run every check CI runs, in the same order, and report which ones failed.

This is the single source of truth for "is the repository green". Nothing else —
not the workflow, not AGENTS.md — should list the checks again; they call this.

  python3 scripts/ci.py              # every check
  python3 scripts/ci.py --coverage   # also enforce branch coverage on scripts/

Coverage is separate because it needs the `coverage` package, which the local
machine may not have; CI runs it on one interpreter only.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COVERAGE_FLOOR = 70
REQUIREMENTS = "requirements-ci.txt"


def interpreter() -> list[str]:
    """The command that runs Python with this repository's test dependencies.

    Several checks need matplotlib, Pillow, or coverage, and a machine that has
    none of them should not have to install them globally to run the suite. When
    uv is on PATH it supplies them per-run from requirements-ci.txt; otherwise
    fall back to this interpreter and let the import error say what is missing.
    """
    if shutil.which("uv"):
        # --python pins uv to the interpreter already running, so a CI matrix over
        # several Python versions still tests each one.
        return ["uv", "run", "--python", sys.executable,
                "--with-requirements", REQUIREMENTS, "--quiet", "python"]
    return [sys.executable]


def run(name: str, argv: list[str]) -> bool:
    """Run one check, stream its output, and report whether it passed."""
    print(f"\n=== {name}\n{' '.join(argv)}", flush=True)
    completed = subprocess.run(argv, cwd=ROOT)
    if completed.returncode != 0:
        print(f"--- FAILED: {name} (exit {completed.returncode})", flush=True)
        return False
    return True


def python_files() -> list[str]:
    """Every Python file in the repository, excluding caches and the git dir."""
    skip = {".git", "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache"}
    return [
        str(path.relative_to(ROOT))
        for path in sorted(ROOT.rglob("*.py"))
        if not skip & set(path.parts)
    ]


def test_suites() -> list[Path]:
    """The repository suite plus every skill that ships its own tests.

    Discovered rather than listed: naming the directories by hand meant a new
    skill's tests stayed silently unexecuted until somebody noticed.
    """
    suites = [ROOT / "tests"]
    suites += sorted(path for path in ROOT.glob("skills/*/tests") if path.is_dir())
    return [path for path in suites if path.is_dir()]


def checks(with_coverage: bool) -> list[tuple[str, list[str]]]:
    """Build the ordered list of (name, argv) checks to run."""
    py = [sys.executable]           # stdlib-only checks need nothing extra
    dep = interpreter()             # checks that need the test dependencies
    planned: list[tuple[str, list[str]]] = [
        ("Skill frontmatter and structure", [*py, "scripts/validate_skills.py"]),
        ("Trigger contract, anti-scope, smoke", [*py, "scripts/evaluate_skill_triggers.py"]),
    ]
    for suite in test_suites():
        planned.append((
            f"Tests: {suite.relative_to(ROOT)}",
            [*dep, "-W", "error::ResourceWarning", "-m", "unittest", "discover",
             "-s", str(suite.relative_to(ROOT)), "-p", "test_*.py"],
        ))
    planned += [
        ("Every Python file compiles", [*py, "-m", "py_compile", *python_files()]),
        # CLAUDE.md is a symlink to AGENTS.md. On a checkout that cannot make
        # symlinks it degrades into a plain file, and the two silently diverge.
        ("CLAUDE.md is still a symlink to AGENTS.md", ["diff", "AGENTS.md", "CLAUDE.md"]),
        ("No whitespace errors in the diff", ["git", "diff", "--check"]),
    ]
    if with_coverage:
        planned += [
            ("Branch coverage: erase", [*dep, "-m", "coverage", "erase"]),
            ("Branch coverage: run", [*dep, "-m", "coverage", "run", "--branch",
                                      "--source=scripts", "-m", "unittest",
                                      "discover", "-s", "tests"]),
            ("Branch coverage: report", [*dep, "-m", "coverage", "report",
                                         "--show-missing",
                                         f"--fail-under={COVERAGE_FLOOR}"]),
        ]
    return planned


def main(argv: list[str] | None = None) -> int:
    """Run the checks and summarise the failures at the end."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--coverage",
        action="store_true",
        help=f"also enforce {COVERAGE_FLOOR}%% branch coverage on scripts/",
    )
    args = parser.parse_args(argv)

    failed = [name for name, cmd in checks(args.coverage) if not run(name, cmd)]

    print()
    if failed:
        print(f"{len(failed)} check(s) failed:")
        for name in failed:
            print(f"  - {name}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
