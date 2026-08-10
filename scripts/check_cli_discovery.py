#!/usr/bin/env python3
"""Check that the official `skills` CLI discovers every skill in this repository.

The expected count is derived from the filesystem rather than written down. A
hard-coded number turns every new skill into a red build, and that is not a
regression — it is the repository doing its job.

Needs Node and network access, so it runs in its own CI job rather than as part
of scripts/ci.py.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANSI = re.compile(r"\x1B\[[0-9;?]*[ -/]*[@-~]")


def expected_count() -> int:
    """Count the installable skills: one first-level directory holding a SKILL.md."""
    return len(list(ROOT.glob("skills/*/SKILL.md")))


def main() -> int:
    """Run the CLI's listing and confirm it reports the expected number."""
    expected = expected_count()
    print(f"Expecting the CLI to discover {expected} skills.")

    completed = subprocess.run(
        ["npx", "--yes", "skills@latest", "add", ".", "--list"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    output = completed.stdout + completed.stderr
    print(output)
    if completed.returncode != 0:
        print(f"the CLI exited {completed.returncode}")
        return 1

    if f"Found {expected} skills" not in ANSI.sub("", output):
        print(f"the CLI did not report 'Found {expected} skills'")
        return 1

    print(f"The CLI discovered all {expected} skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
