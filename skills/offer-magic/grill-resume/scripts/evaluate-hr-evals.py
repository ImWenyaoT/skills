#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


VALIDATOR = Path(__file__).with_name("validate-review-report.py")
SPEC = importlib.util.spec_from_file_location("validate_review_report", VALIDATOR)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--packets", type=Path, required=True)
    parser.add_argument("--reports", type=Path, required=True)
    args = parser.parse_args()

    failures: list[str] = []
    cases = json.loads(args.cases.read_text(encoding="utf-8"))
    for case in cases:
        case_id = case["id"]
        report_path = args.reports / f"{case_id}.json"
        if not report_path.is_file():
            failures.append(f"{case_id}: missing report")
            continue
        report = json.loads(report_path.read_text(encoding="utf-8"))
        content = args.packets / case_id / "content"
        resume = (content / "resume-semantic.txt").read_text(encoding="utf-8")
        jd = (content / "jd.txt").read_text(encoding="utf-8")
        errors = MODULE.validate_report(report, resume, jd)
        failures.extend(f"{case_id}: {error}" for error in errors)

        expected = case.get("expect", {})
        text = report.get("five_second_profile", {}).get("text", "")
        for term in expected.get("profile_terms", []):
            if term.casefold() not in text.casefold():
                failures.append(f"{case_id}: profile missing term {term!r}")
        categories = {
            finding.get("category")
            for finding in report.get("material_findings", [])
            if isinstance(finding, dict)
        }
        for category in expected.get("required_categories", []):
            if category not in categories:
                failures.append(f"{case_id}: missing category {category}")
        for category in expected.get("forbidden_categories", []):
            if category in categories:
                failures.append(f"{case_id}: unexpected category {category}")
        allowed = expected.get("allowed_recommendations")
        if allowed and report.get("recommendation") not in allowed:
            failures.append(
                f"{case_id}: recommendation {report.get('recommendation')!r} not in {allowed}"
            )

    if failures:
        raise SystemExit("HR behavior evals failed:\n- " + "\n- ".join(failures))
    print(f"HR behavior evals passed: {len(cases)}")


if __name__ == "__main__":
    main()
