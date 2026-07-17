#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED = {
    "question": str,
    "evaluation_intent": str,
    "verdict": str,
    "directness": (str, bool),
    "supported_claims": list,
    "unsupported_claims": list,
    "missing_reasoning": list,
    "followups": list,
    "better_answer_shape": (str, list),
    "clarification_requests": list,
}
TEXT_SUFFIXES = {".txt", ".md", ".json", ".html", ".yaml", ".yml"}


def normalize(value: str) -> str:
    return re.sub(r"\s+", "", value).casefold()


def is_candidate_profile(path: Path) -> bool:
    if path.name == "candidate-profile.json":
        return True
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return False
    return (
        isinstance(value, dict)
        and value.get("schema_version") == 1
        and value.get("visibility") == "main_only"
        and set(value.get("slots", {})) == {"recognition", "character", "trajectory"}
    )


def packet_text(path: Path, excluded: Path) -> str:
    files = [path] if path.is_file() else sorted(path.rglob("*"))
    parts: list[str] = []
    for file in files:
        if file.is_file() and is_candidate_profile(file):
            raise ValueError("candidate-profile.json is main-only and cannot enter an Interviewer packet")
        if (
            file.is_file()
            and file.resolve() != excluded.resolve()
            and file.suffix.lower() in TEXT_SUFFIXES
        ):
            parts.append(file.read_text(encoding="utf-8", errors="ignore"))
    return normalize("\n".join(parts))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--packet", type=Path, required=True)
    args = parser.parse_args()

    report = json.loads(args.report.read_text(encoding="utf-8"))
    errors: list[str] = []
    try:
        source = packet_text(args.packet, args.report)
    except ValueError as error:
        source = ""
        errors.append(str(error))
    if not source:
        errors.append("packet contains no readable text")

    for key, expected in REQUIRED.items():
        if key not in report:
            errors.append(f"missing key: {key}")
        elif not isinstance(report[key], expected):
            errors.append(f"{key} has the wrong type")
    if report.get("verdict") not in {"strong", "mixed", "weak"}:
        errors.append("verdict must be strong, mixed, or weak")

    question = report.get("question")
    if not isinstance(question, str) or not question.strip():
        errors.append("question must be non-empty")
    elif normalize(question) not in source:
        errors.append("question is not present in the frozen packet")

    claims = report.get("supported_claims", [])
    if isinstance(claims, list):
        for index, item in enumerate(claims):
            if not isinstance(item, dict):
                errors.append(f"supported_claims[{index}] must be an object")
                continue
            for key in ("claim", "packet_quote", "source"):
                if not isinstance(item.get(key), str) or not item[key].strip():
                    errors.append(f"supported_claims[{index}].{key} must be non-empty")
            quote = item.get("packet_quote")
            if isinstance(quote, str) and quote.strip() and normalize(quote) not in source:
                errors.append(f"supported_claims[{index}].packet_quote is not in the packet")

    if errors:
        raise SystemExit("interview report validation failed:\n- " + "\n- ".join(errors))
    print("interview report valid")


if __name__ == "__main__":
    main()
