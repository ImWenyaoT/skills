#!/usr/bin/env python3
"""Compile the bundled elsarticle fixture or report the missing runtime step."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = ROOT / "assets" / "minimal-article"


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run one LaTeX command and retain combined output for diagnostics."""
    return subprocess.run(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )


def doctor() -> tuple[str | None, list[str]]:
    """Return the available build strategy and actionable runtime problems."""
    latexmk = shutil.which("latexmk")
    pdflatex = shutil.which("pdflatex")
    bibtex = shutil.which("bibtex")
    missing_runtime = [
        name for name, path in (("pdflatex", pdflatex), ("bibtex", bibtex)) if not path
    ]
    if missing_runtime:
        return None, [
            f"LaTeX runtime unavailable or incomplete (missing {', '.join(missing_runtime)}): ",
            "install TeX Live/MacTeX or MiKTeX with pdflatex, BibTeX, latexmk, and the ",
            "elsarticle package; then rerun this smoke.",
        ]

    kpsewhich = shutil.which("kpsewhich")
    if not kpsewhich:
        return None, [
            "LaTeX package lookup unavailable: ensure kpsewhich is on PATH, then rerun.",
        ]
    missing = []
    for filename in ("elsarticle.cls", "elsarticle-num.bst"):
        result = subprocess.run(
            [kpsewhich, filename], capture_output=True, text=True, check=False
        )
        if result.returncode != 0 or not result.stdout.strip():
            missing.append(filename)
    if missing:
        return None, [
            f"Elsevier LaTeX package unavailable ({', '.join(missing)}): install or repair ",
            "the elsarticle package, refresh the TeX filename database, and rerun.",
        ]
    return ("latexmk" if latexmk else "manual"), []


def compile_template(template: Path, strategy: str) -> tuple[bool, str]:
    """Compile a copied fixture and return a short failure excerpt when needed."""
    with tempfile.TemporaryDirectory(prefix="elsevier-article-smoke-") as tmp:
        workdir = Path(tmp) / "article"
        shutil.copytree(template, workdir)
        if strategy == "latexmk":
            commands = [[
                "latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"
            ]]
        else:
            latex = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
            commands = [latex, ["bibtex", "main"], latex, latex]
        output = ""
        for command in commands:
            result = run(command, workdir)
            output += result.stdout
            if result.returncode != 0:
                return False, "\n".join(output.splitlines()[-30:])
        pdf = workdir / "main.pdf"
        log_path = workdir / "main.log"
        if not log_path.is_file():
            return False, "compile did not produce main.log"
        log = log_path.read_text(encoding="utf-8", errors="replace")
        unresolved = "undefined references" in log.lower() or "undefined citations" in log.lower()
        return pdf.is_file() and pdf.stat().st_size > 0 and not unresolved, "\n".join(
            output.splitlines()[-30:]
        )


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Smoke-test the bundled elsarticle template")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    args = parser.parse_args()
    if not (args.template / "main.tex").is_file():
        print(f"Template missing main.tex: {args.template}")
        return 1

    strategy, problems = doctor()
    if problems:
        print("".join(problems))
        return 2

    passed, details = compile_template(args.template, strategy or "manual")
    if not passed:
        print("elsarticle template smoke failed")
        print(details)
        return 1
    print(f"elsarticle template smoke passed with {strategy}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
