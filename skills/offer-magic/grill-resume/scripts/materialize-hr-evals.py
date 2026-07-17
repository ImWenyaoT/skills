#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    cases = json.loads(args.cases.read_text(encoding="utf-8"))
    if args.out.exists() and any(args.out.iterdir()):
        raise SystemExit("eval output directory must be empty")
    for case in cases:
        content = args.out / case["id"] / "content"
        content.mkdir(parents=True, exist_ok=True)
        (content / "resume-semantic.txt").write_text(
            case["resume"].strip() + "\n", encoding="utf-8"
        )
        (content / "jd.txt").write_text(case["jd"].strip() + "\n", encoding="utf-8")
        (content / "constraints.txt").write_text(
            "Language: Simplified Chinese\nReview stage: frozen synthetic behavior eval\n",
            encoding="utf-8",
        )
    print(args.out.resolve())


if __name__ == "__main__":
    main()
