#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REQUIRED = {
    "schema_version": int,
    "five_second_profile": dict,
    "recommendation": str,
    "confidence": (int, float),
    "material_findings": list,
    "clarification_requests": list,
}
PROFILE_STATUSES = {"clear", "partial", "unclear"}
RECOMMENDATIONS = {"advance", "hold", "reject"}
CATEGORIES = {
    "hard_requirement",
    "strongest_evidence",
    "confusion",
    "overfit_risk",
    "layout",
    "claim_boundary",
    "interview_hook",
    "distinctiveness",
    "selection",
    "narrative_alignment",
}
NO_JD_PREFIX = "[No target JD provided;"
UNCLEAR_MARKERS = ("无法", "不能", "难以", "不清晰", "看不出", "未能")


def normalize(value: str) -> str:
    return re.sub(r"\s+", "", value).casefold()


def sentence_count(value: str) -> int:
    parts = [part for part in re.split(r"[。！？!?]+", value) if part.strip()]
    return len(parts)


def validate_quotes(
    *,
    values: Any,
    source: str,
    label: str,
    errors: list[str],
) -> None:
    if not isinstance(values, list):
        errors.append(f"{label} must be a list")
        return
    for index, quote in enumerate(values):
        if not isinstance(quote, str) or not quote.strip():
            errors.append(f"{label}[{index}] must be a non-empty string")
        elif normalize(quote) not in source:
            errors.append(f"{label}[{index}] is not in its frozen source")


def validate_report(report: Any, resume_text: str, jd_text: str) -> list[str]:
    resume = normalize(resume_text)
    jd = normalize(jd_text)
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["report must be an object"]

    for key, expected in REQUIRED.items():
        if key not in report:
            errors.append(f"missing key: {key}")
        elif not isinstance(report[key], expected):
            errors.append(f"invalid type for {key}")

    if report.get("schema_version") != 2:
        errors.append("schema_version must be 2")

    profile = report.get("five_second_profile")
    if isinstance(profile, dict):
        expected_profile_keys = {"status", "text", "resume_quotes", "jd_quotes"}
        missing = expected_profile_keys - profile.keys()
        if missing:
            errors.append(
                "five_second_profile missing: " + ", ".join(sorted(missing))
            )
        status = profile.get("status")
        text = profile.get("text")
        resume_quotes = profile.get("resume_quotes")
        jd_quotes = profile.get("jd_quotes")
        if status not in PROFILE_STATUSES:
            errors.append("five_second_profile.status is invalid")
        if not isinstance(text, str) or not text.strip():
            errors.append("five_second_profile.text must be non-empty")
        else:
            if len(normalize(text)) > 100:
                errors.append("five_second_profile.text exceeds 100 non-whitespace characters")
            if sentence_count(text) > 2:
                errors.append("five_second_profile.text must use at most two sentences")
            if status == "unclear" and not any(marker in text for marker in UNCLEAR_MARKERS):
                errors.append("an unclear profile must state that the resume is unclear")
        validate_quotes(
            values=resume_quotes,
            source=resume,
            label="five_second_profile.resume_quotes",
            errors=errors,
        )
        validate_quotes(
            values=jd_quotes,
            source=jd,
            label="five_second_profile.jd_quotes",
            errors=errors,
        )
        if status == "clear" and isinstance(resume_quotes, list) and len(resume_quotes) < 2:
            errors.append("a clear profile needs at least two resume quotes")
        has_target_jd = not jd_text.lstrip().startswith(NO_JD_PREFIX)
        if has_target_jd and isinstance(jd_quotes, list) and not jd_quotes:
            errors.append("a target-JD profile needs at least one JD quote")
        if not has_target_jd and isinstance(jd_quotes, list) and jd_quotes:
            errors.append("a no-JD profile must not invent JD quotes")

    if report.get("recommendation") not in RECOMMENDATIONS:
        errors.append("recommendation must be advance, hold, or reject")

    confidence = report.get("confidence")
    if (
        isinstance(confidence, bool)
        or not isinstance(confidence, (int, float))
        or not 0 <= confidence <= 1
    ):
        errors.append("confidence must be a number between 0 and 1")

    findings = report.get("material_findings", [])
    if isinstance(findings, list):
        for index, finding in enumerate(findings):
            if not isinstance(finding, dict):
                errors.append(f"material_findings[{index}] must be an object")
                continue
            for key in ("category", "finding", "why_it_matters"):
                if not isinstance(finding.get(key), str) or not finding[key].strip():
                    errors.append(f"material_findings[{index}].{key} must be non-empty")
            if finding.get("category") not in CATEGORIES:
                errors.append(f"material_findings[{index}].category is invalid")

            resume_quote = finding.get("resume_quote")
            jd_quote = finding.get("jd_quote")
            if resume_quote is not None and (
                not isinstance(resume_quote, str)
                or not resume_quote.strip()
                or normalize(resume_quote) not in resume
            ):
                errors.append(f"material_findings[{index}].resume_quote is not in the resume")
            if jd_quote is not None and (
                not isinstance(jd_quote, str)
                or not jd_quote.strip()
                or normalize(jd_quote) not in jd
            ):
                errors.append(f"material_findings[{index}].jd_quote is not in the JD")
            if resume_quote is None and jd_quote is None:
                errors.append(f"material_findings[{index}] needs a resume_quote or jd_quote")

    clarification_fields = {
        "blocked_judgment",
        "known_evidence",
        "unknown",
        "why_material",
        "candidate_question",
    }
    requests = report.get("clarification_requests", [])
    if isinstance(requests, list):
        for index, request in enumerate(requests):
            if not isinstance(request, dict):
                errors.append(f"clarification_requests[{index}] must be an object")
                continue
            missing = clarification_fields - request.keys()
            if missing:
                errors.append(
                    f"clarification_requests[{index}] missing: "
                    + ", ".join(sorted(missing))
                )
            for field in clarification_fields & request.keys():
                if not isinstance(request[field], str) or not request[field].strip():
                    errors.append(
                        f"clarification_requests[{index}].{field} must be a non-empty string"
                    )
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--resume-text", type=Path, required=True)
    parser.add_argument("--jd-text", type=Path, required=True)
    args = parser.parse_args()

    report = json.loads(args.report.read_text(encoding="utf-8"))
    errors = validate_report(
        report,
        args.resume_text.read_text(encoding="utf-8"),
        args.jd_text.read_text(encoding="utf-8"),
    )
    if errors:
        raise SystemExit("review report invalid:\n- " + "\n- ".join(errors))
    print("review report valid")


if __name__ == "__main__":
    main()
