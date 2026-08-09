#!/usr/bin/env python3
"""Compile the bundled response-letter template, or name the missing runtime step.

The template is written so that an unsubstituted `{{PLACEHOLDER}}` still
compiles, which makes the whole directory a valid smoke target on its own. The
failure this catches is a partial TeX install: `\\usepackage[most]{tcolorbox}`
and the `breakable` library are not in the small distributions, and the error
LaTeX prints for them is far from the cause.

Usage:
    python3 smoke_letter.py [--template assets/response-letter]

Exit codes: 0 compiled, 1 the template is broken, 2 the runtime is unusable.
Only the standard library is used, so the script runs wherever python3 does.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = ROOT / "assets" / "response-letter"

# Packages the template loads that a minimal TeX install omits.
REQUIRED_STYLES = ("tcolorbox.sty", "helvet.sty", "authblk.sty", "csquotes.sty")


def doctor() -> tuple[str | None, list[str]]:
    """Return the usable build strategy and the runtime problems that block it."""
    latexmk = shutil.which("latexmk")
    pdflatex = shutil.which("pdflatex")
    if not pdflatex:
        return None, [
            "LaTeX runtime unavailable (missing pdflatex): install a full TeX Live, MacTeX, ",
            "or MiKTeX, then rerun this smoke.",
        ]

    kpsewhich = shutil.which("kpsewhich")
    if not kpsewhich:
        return None, ["LaTeX package lookup unavailable: put kpsewhich on PATH, then rerun."]

    missing = [name for name in REQUIRED_STYLES if not _style_found(kpsewhich, name)]
    if missing:
        return None, [
            f"TeX packages unavailable ({', '.join(missing)}): the letter template needs a full ",
            "TeX Live — tcolorbox with the [most] option and the breakable library. Install the ",
            "missing packages, refresh the filename database, and rerun.",
        ]
    return ("latexmk" if latexmk else "manual"), []


def _style_found(kpsewhich: str, filename: str) -> bool:
    """Return whether kpsewhich resolves one style file."""
    result = subprocess.run([kpsewhich, filename], capture_output=True, text=True, check=False)
    return result.returncode == 0 and bool(result.stdout.strip())


def compile_template(template: Path, strategy: str) -> tuple[bool, str]:
    """Compile a copy of the template and return the tail of the log on failure."""
    with tempfile.TemporaryDirectory(prefix="response-letter-smoke-") as tmp:
        workdir = Path(tmp) / "letter"
        shutil.copytree(template, workdir)
        if strategy == "latexmk":
            commands = [["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
                         "main.tex"]]
        else:
            latex = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
            commands = [latex, latex]
        output = ""
        for command in commands:
            result = subprocess.run(command, cwd=workdir, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True, check=False)
            output += result.stdout
            if result.returncode != 0:
                return False, "\n".join(output.splitlines()[-30:])
        pdf = workdir / "main.pdf"
        return pdf.is_file() and pdf.stat().st_size > 0, "\n".join(output.splitlines()[-30:])


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    args = parser.parse_args(argv)
    if not (args.template / "main.tex").is_file():
        print(f"template missing main.tex: {args.template}", file=sys.stderr)
        return 1

    strategy, problems = doctor()
    if problems:
        print("".join(problems), file=sys.stderr)
        return 2

    passed, details = compile_template(args.template, strategy or "manual")
    if not passed:
        print("response-letter template smoke failed", file=sys.stderr)
        print(details, file=sys.stderr)
        return 1
    print(f"response-letter template smoke passed with {strategy}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
