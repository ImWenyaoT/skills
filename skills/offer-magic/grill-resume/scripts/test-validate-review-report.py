#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate-review-report.py")
SPEC = importlib.util.spec_from_file_location("validate_review_report", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

RESUME = "28 届电子信息硕士。二作发表 HGD-Net。构建 Agent Harness 并用 14 个场景验证。"
JD = "负责 Agent Harness 的任务编排、工具调用和评测。"
NO_JD = "[No target JD provided; perform a general resume review.]\n"


def valid_report() -> dict:
    return {
        "schema_version": 2,
        "five_second_profile": {
            "status": "clear",
            "text": "28 届电子信息硕士，二作发表 HGD-Net。用可评测 Agent Harness 对齐岗位任务编排。",
            "resume_quotes": ["28 届电子信息硕士", "二作发表 HGD-Net"],
            "jd_quotes": ["负责 Agent Harness 的任务编排、工具调用和评测"],
        },
        "recommendation": "advance",
        "confidence": 0.86,
        "material_findings": [],
        "clarification_requests": [],
    }


def assert_valid(report: dict, jd: str = JD) -> None:
    errors = MODULE.validate_report(report, RESUME, jd)
    assert not errors, errors


def assert_invalid(report: dict, expected: str, jd: str = JD) -> None:
    errors = MODULE.validate_report(report, RESUME, jd)
    assert any(expected in error for error in errors), errors


def main() -> None:
    assert_valid(valid_report())

    report = valid_report()
    report["schema_version"] = 1
    assert_invalid(report, "schema_version must be 2")

    report = valid_report()
    report["five_second_profile"]["status"] = "excellent"
    assert_invalid(report, "status is invalid")

    report = valid_report()
    report["five_second_profile"]["text"] = "甲。乙。丙。"
    assert_invalid(report, "at most two sentences")

    report = valid_report()
    report["five_second_profile"]["text"] = "候" * 101
    assert_invalid(report, "exceeds 100")

    report = valid_report()
    report["five_second_profile"]["resume_quotes"] = ["二作发表 HGD-Net"]
    assert_invalid(report, "at least two resume quotes")

    report = valid_report()
    report["five_second_profile"]["resume_quotes"][0] = "不存在的候选人信息"
    assert_invalid(report, "not in its frozen source")

    report = valid_report()
    report["five_second_profile"]["status"] = "unclear"
    report["five_second_profile"]["text"] = "这是一位方向清晰且证据充分的候选人。"
    assert_invalid(report, "must state that the resume is unclear")

    report = valid_report()
    report["five_second_profile"]["jd_quotes"] = []
    assert_invalid(report, "needs at least one JD quote")

    report = valid_report()
    report["five_second_profile"]["jd_quotes"] = []
    assert_valid(report, NO_JD)

    report = valid_report()
    report["material_findings"] = [
        {
            "category": "selection",
            "finding": "常规工作重复。",
            "why_it_matters": "挤占区分度。",
            "resume_quote": "构建 Agent Harness 并用 14 个场景验证",
        }
    ]
    assert_valid(report)

    print("validate-review-report tests passed: 11")


if __name__ == "__main__":
    main()
