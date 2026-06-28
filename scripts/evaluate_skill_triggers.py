#!/usr/bin/env python3
"""Evaluate skill trigger health from golden prompts and optional trace predictions.

The default mode is an offline contract check: it verifies that every local skill
has positive and negative coverage in evals/trigger_cases.json, then runs a small
metadata-similarity smoke test to catch obviously overlapping descriptions.

For real trigger metrics, pass --predictions JSONL with records like:
  {"id": "case-id", "actual_skills": ["reviewing-academic-papers"]}
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals" / "trigger_cases.json"
SKIP = {"scripts", ".git", ".github", "evals"}
STOPWORDS = {
    "about",
    "after",
    "agent",
    "also",
    "and",
    "any",
    "are",
    "before",
    "build",
    "code",
    "during",
    "from",
    "help",
    "into",
    "need",
    "needs",
    "not",
    "the",
    "this",
    "turn",
    "use",
    "used",
    "user",
    "when",
    "with",
    "work",
    "workflow",
}


@dataclass(frozen=True)
class Skill:
    """Store the trigger metadata that is visible before a skill is loaded."""

    name: str
    path: Path
    description: str


@dataclass(frozen=True)
class Case:
    """Store one golden trigger case."""

    id: str
    prompt: str
    expected_skills: tuple[str, ...]
    forbidden_skills: tuple[str, ...]
    notes: str


def parse_frontmatter(text: str) -> dict[str, str]:
    """Parse scalar SKILL.md frontmatter without requiring PyYAML."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out: dict[str, str] = {}
    for line in text[3:end].splitlines():
        match = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.group(1), match.group(2).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        out[key] = value
    return out


def load_skills() -> dict[str, Skill]:
    """Load all local skill names and descriptions from first-level folders."""
    skills: dict[str, Skill] = {}
    for child in sorted(ROOT.iterdir()):
        if not child.is_dir() or child.name in SKIP or child.name.startswith("."):
            continue
        skill_md = child / "SKILL.md"
        if not skill_md.is_file():
            continue
        metadata = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        name = metadata.get("name", "")
        description = metadata.get("description", "")
        if name:
            skills[name] = Skill(name=name, path=skill_md, description=description)
    return skills


def load_cases(path: Path = EVALS) -> list[Case]:
    """Load golden trigger cases from JSON."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    cases: list[Case] = []
    for item in raw.get("cases", []):
        cases.append(
            Case(
                id=item["id"],
                prompt=item["prompt"],
                expected_skills=tuple(item.get("expected_skills", [])),
                forbidden_skills=tuple(item.get("forbidden_skills", [])),
                notes=item.get("notes", ""),
            )
        )
    return cases


def tokenize(text: str) -> set[str]:
    """Tokenize English words, skill-name fragments, and short CJK n-grams."""
    lowered = text.lower().replace("-", " ")
    words = {
        token
        for token in re.findall(r"[a-z0-9][a-z0-9_]{2,}", lowered)
        if token not in STOPWORDS
    }
    cjk_chars = re.findall(r"[\u4e00-\u9fff]", text)
    cjk_grams = {"".join(cjk_chars[i : i + 2]) for i in range(max(0, len(cjk_chars) - 1))}
    return words | cjk_grams


def metadata_tokens(skill: Skill) -> set[str]:
    """Return the pre-load tokens a router can infer from name and description."""
    positive_description = re.split(
        r"\bDo not\b|\bDon't\b|不要|不应|不负责",
        skill.description,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]
    return tokenize(f"{skill.name.replace('-', ' ')} {positive_description}")


def similarity(prompt: str, skill: Skill) -> float:
    """Score how strongly one prompt resembles a skill's visible metadata."""
    if is_path_scoped_without_signal(prompt, skill):
        return 0.0
    prompt_tokens = tokenize(prompt)
    skill_tokens = metadata_tokens(skill)
    if not prompt_tokens or not skill_tokens:
        return 0.0
    overlap = len(prompt_tokens & skill_tokens)
    return overlap / math.sqrt(len(prompt_tokens) * len(skill_tokens))


def is_path_scoped_without_signal(prompt: str, skill: Skill) -> bool:
    """Return true when an absolute-path skill lacks any matching prompt signal."""
    if "/Users/" not in skill.description:
        return False
    prompt_lower = prompt.lower()
    description_lower = skill.description.lower()
    path_signals = re.findall(r"/users/[^\s,;:)]+", description_lower)
    repo_signals = re.findall(r"\b[a-z0-9_.-]+/[a-z0-9_.-]+\b", description_lower)
    phrase_signals = [
        "intern/docs/notes",
        "imwenyaot/notes",
        "that site's github pages",
        "personal notes site",
    ]
    return not any(signal in prompt_lower for signal in path_signals + repo_signals + phrase_signals)


def rank_skills(prompt: str, skills: dict[str, Skill]) -> list[tuple[str, float]]:
    """Rank skills by deterministic metadata similarity for smoke testing."""
    scored = [(name, similarity(prompt, skill)) for name, skill in skills.items()]
    return sorted(scored, key=lambda item: (-item[1], item[0]))


def validate_case_contract(cases: list[Case], skills: dict[str, Skill]) -> list[str]:
    """Validate that eval labels reference real skills and cover each skill both ways."""
    failures: list[str] = []
    skill_names = set(skills)
    ids = [case.id for case in cases]
    duplicate_ids = [case_id for case_id, count in Counter(ids).items() if count > 1]
    for case_id in duplicate_ids:
        failures.append(f"duplicate case id: {case_id}")

    positive_counts: Counter[str] = Counter()
    negative_counts: Counter[str] = Counter()
    for case in cases:
        referenced = set(case.expected_skills) | set(case.forbidden_skills)
        unknown = sorted(referenced - skill_names)
        if unknown:
            failures.append(f"{case.id}: unknown skills {unknown}")
        for skill in case.expected_skills:
            positive_counts[skill] += 1
        for skill in case.forbidden_skills:
            negative_counts[skill] += 1
        if set(case.expected_skills) & set(case.forbidden_skills):
            failures.append(f"{case.id}: skill appears in both expected and forbidden")

    for skill_name in sorted(skill_names):
        if positive_counts[skill_name] < 2:
            failures.append(f"{skill_name}: needs at least 2 positive trigger cases")
        if negative_counts[skill_name] < 2:
            failures.append(f"{skill_name}: needs at least 2 forbidden/negative cases")
    return failures


def smoke_test_metadata(cases: list[Case], skills: dict[str, Skill]) -> list[str]:
    """Run a cheap metadata-only overlap smoke test to flag broad descriptions."""
    failures: list[str] = []
    for case in cases:
        ranked = rank_skills(case.prompt, skills)
        top_name, top_score = ranked[0]
        expected = set(case.expected_skills)
        forbidden = set(case.forbidden_skills)

        if expected and top_name not in expected:
            expected_scores = {name: similarity(case.prompt, skills[name]) for name in expected}
            best_expected, best_score = max(expected_scores.items(), key=lambda item: item[1])
            failures.append(
                f"{case.id}: metadata top={top_name}({top_score:.3f}) "
                f"but expected {best_expected}({best_score:.3f})"
            )

        if top_name in forbidden and top_score >= 0.10:
            failures.append(f"{case.id}: forbidden skill {top_name} ranks first ({top_score:.3f})")

        if not expected and top_score >= 0.25:
            failures.append(f"{case.id}: no expected skill but metadata top={top_name}({top_score:.3f})")
    return failures


def load_predictions(path: Path) -> dict[str, tuple[str, ...]]:
    """Load JSONL predictions from a real agent run or sub-agent harness."""
    predictions: dict[str, tuple[str, ...]] = {}
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            item = json.loads(stripped)
            case_id = item.get("id")
            actual = item.get("actual_skills", [])
            if not isinstance(case_id, str) or not isinstance(actual, list):
                raise ValueError(f"{path}:{line_no}: expected id and actual_skills list")
            predictions[case_id] = tuple(str(skill) for skill in actual)
    return predictions


def score_predictions(cases: list[Case], predictions: dict[str, tuple[str, ...]]) -> tuple[list[str], dict[str, float]]:
    """Score real trigger predictions against the golden labels."""
    failures: list[str] = []
    true_positive = 0
    false_positive = 0
    false_negative = 0
    forbidden_hits = 0
    expected_total = 0
    actual_total = 0

    for case in cases:
        expected = set(case.expected_skills)
        forbidden = set(case.forbidden_skills)
        actual = set(predictions.get(case.id, ()))
        missing = expected - actual
        extra = actual - expected
        forbidden_actual = actual & forbidden
        true_positive += len(expected & actual)
        false_positive += len(extra)
        false_negative += len(missing)
        forbidden_hits += len(forbidden_actual)
        expected_total += len(expected)
        actual_total += len(actual)

        if missing or extra or forbidden_actual:
            failures.append(
                f"{case.id}: missing={sorted(missing)} extra={sorted(extra)} "
                f"forbidden_hits={sorted(forbidden_actual)} "
                f"actual={sorted(actual)}"
            )

    precision = true_positive / actual_total if actual_total else 1.0
    recall = true_positive / expected_total if expected_total else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    metrics = {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "false_positive": float(false_positive),
        "false_negative": float(false_negative),
        "forbidden_hits": float(forbidden_hits),
    }
    return failures, metrics


def print_summary(cases: list[Case], skills: dict[str, Skill]) -> None:
    """Print coverage counts so maintainers can see weak eval areas."""
    positive_counts: Counter[str] = Counter()
    negative_counts: Counter[str] = Counter()
    for case in cases:
        positive_counts.update(case.expected_skills)
        negative_counts.update(case.forbidden_skills)

    print(f"Loaded {len(skills)} skills and {len(cases)} trigger cases.")
    for skill_name in sorted(skills):
        print(
            f"- {skill_name}: positives={positive_counts[skill_name]} "
            f"forbidden={negative_counts[skill_name]}"
        )


def main(argv: Iterable[str] | None = None) -> int:
    """Run trigger-contract validation and optional prediction scoring."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=EVALS, help="Path to trigger cases JSON")
    parser.add_argument("--predictions", type=Path, help="Optional JSONL actual_skills predictions")
    parser.add_argument("--min-precision", type=float, default=0.90, help="Minimum precision for --predictions")
    parser.add_argument("--min-recall", type=float, default=0.90, help="Minimum recall for --predictions")
    parser.add_argument("--min-f1", type=float, default=0.90, help="Minimum F1 for --predictions")
    parser.add_argument(
        "--skip-smoke",
        action="store_true",
        help="Skip metadata-overlap smoke test and only validate labels/predictions",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    skills = load_skills()
    cases = load_cases(args.cases)
    print_summary(cases, skills)

    failures = validate_case_contract(cases, skills)
    if not args.skip_smoke:
        failures.extend(smoke_test_metadata(cases, skills))

    if args.predictions:
        prediction_failures, metrics = score_predictions(cases, load_predictions(args.predictions))
        failures.extend(prediction_failures)
        print(
            "Prediction metrics: "
            f"precision={metrics['precision']:.3f} recall={metrics['recall']:.3f} "
            f"f1={metrics['f1']:.3f} forbidden_hits={metrics['forbidden_hits']:.0f}"
        )
        if metrics["precision"] < args.min_precision:
            failures.append(
                f"prediction precision {metrics['precision']:.3f} below threshold {args.min_precision:.3f}"
            )
        if metrics["recall"] < args.min_recall:
            failures.append(f"prediction recall {metrics['recall']:.3f} below threshold {args.min_recall:.3f}")
        if metrics["f1"] < args.min_f1:
            failures.append(f"prediction f1 {metrics['f1']:.3f} below threshold {args.min_f1:.3f}")

    if failures:
        print("\nTrigger health failures:")
        for failure in failures:
            print(f"ERROR {failure}")
        return 1

    print("\nTrigger health checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
