#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


LIST_KEYS = {
    "hard_requirements",
    "core_work",
    "preferences",
    "environment_signals",
    "unknowns",
    "likely_followups",
}
QUOTED_KEYS = {"hard_requirements", "core_work", "preferences", "environment_signals"}


def normalize(value: str) -> str:
    return re.sub(r"\s+", "", value).casefold()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--jd", type=Path, required=True)
    args = parser.parse_args()

    report = json.loads(args.report.read_text(encoding="utf-8"))
    jd = normalize(args.jd.read_text(encoding="utf-8"))
    errors: list[str] = []

    if not isinstance(report.get("role_summary"), str) or not report["role_summary"].strip():
        errors.append("role_summary must be a non-empty string")

    for key in LIST_KEYS:
        if not isinstance(report.get(key), list):
            errors.append(f"{key} must be a list")

    for key in QUOTED_KEYS:
        values = report.get(key, [])
        if not isinstance(values, list):
            continue
        for index, item in enumerate(values):
            if not isinstance(item, dict):
                errors.append(f"{key}[{index}] must be an object")
                continue
            quote = item.get("jd_quote")
            if not isinstance(quote, str) or not quote.strip():
                errors.append(f"{key}[{index}].jd_quote must be non-empty")
            elif normalize(quote) not in jd:
                errors.append(f"{key}[{index}].jd_quote is not present in the frozen JD")
            if not isinstance(item.get("signal"), str) or not item["signal"].strip():
                errors.append(f"{key}[{index}].signal must be non-empty")
            if key != "environment_signals":
                if not isinstance(item.get("reason"), str) or not item["reason"].strip():
                    errors.append(f"{key}[{index}].reason must be non-empty")
            else:
                if not isinstance(item.get("inference"), str) or not item["inference"].strip():
                    errors.append(f"{key}[{index}].inference must be non-empty")
                confidence = item.get("confidence")
                if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
                    errors.append(f"{key}[{index}].confidence must be numeric")
                elif not 0 <= confidence <= 1:
                    errors.append(f"{key}[{index}].confidence must be between 0 and 1")

    if errors:
        raise SystemExit("role report validation failed:\n- " + "\n- ".join(errors))
    print("role report valid")


if __name__ == "__main__":
    main()
