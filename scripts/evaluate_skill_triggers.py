#!/usr/bin/env python3
"""Check that every skill's trigger boundary is declared and non-overlapping.

The cases are split 60/40 into train and validation. Revise descriptions against
train failures only; the validation half exists to answer a different question —
did the revision generalise, or was it fitted to the cases in front of you? That
is why a validation failure is reported as a count and never as a case: knowing
which one failed is exactly what lets you patch for it, and a patch aimed at one
held-out prompt destroys the only estimate you have.

Three offline checks, no model and no network:
  1. Contract  — every skill has >=2 positive and >=2 forbidden cases in
                 evals/trigger_cases.json, and every label names a real skill.
  2. Anti-scope — every declared boundary ("Do not use for ...", "Does not apply
                 to ...") is exercised by a forbidden case that overlaps it.
  3. Smoke     — a bag-of-words overlap between each prompt and the attracting
                 half of the metadata a router sees before loading SKILL.md.
                 It catches descriptions that obviously collide; it is NOT a
                 model, and a passing smoke does not mean a real router would
                 route the same way.

This used to also score `--predictions` from a model-in-the-loop router with
precision/recall/F1, a confusion matrix, and pass@k / pass^k. That half was
deleted: it required an external API call that was never approved, so in the
repository's whole history it never produced a single measurement.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
EVALS = ROOT / "evals" / "trigger_cases.json"
SKIP = {"scripts", ".git", ".github", "evals"}
NONE_LABEL = "<none>"  # explicit abstain class so "fire nothing" is first-class
SPLITS = ("train", "validation")
# The validation half is a rate, not a checklist. Requiring every held-out case to
# pass would force you to read which one failed, and reading it is what turns the
# held-out half into more training data. A floor catches a description that stopped
# generalising without ever telling you which prompt to patch.
VALIDATION_FLOOR = 0.85
# "Does not apply to ..." is as common as "Do not use for ..." in this library, and
# matching only the latter silently scored three skills' anti-scope as attraction.
# The marker must start a sentence: a description listing symptoms says "the loss
# does not decrease", and matching that mid-clause cuts the trigger vocabulary off
# at the knees and files it under the boundary.
ANTISCOPE_MARKER = re.compile(
    r"(?:^|(?<=[.;!。；！])\s*)(Do(?:es)? not\b|Don't\b|不要|不应|不负责|不处理)",
    re.IGNORECASE,
)
# Word overlap cannot separate two skills that score within a few percent of each
# other, so a verdict there reads noise. Measured on this library's 73 correctly
# routed cases, the runner-up stays under 0.75 of the winner in 95% of them; only
# above 0.80 does the ranking stop meaning anything. Report a miss only when the
# expected skill falls outside that tie band.
TIE_RATIO = 0.80
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
    "for",
    "from",
    "help",
    "into",
    "need",
    "needs",
    "not",
    "that",
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
    user_invoked: bool


@dataclass(frozen=True)
class Case:
    """Store one golden trigger case."""

    id: str
    prompt: str
    expected_skills: tuple[str, ...]
    forbidden_skills: tuple[str, ...]
    notes: str
    split: str

    @property
    def is_abstain(self) -> bool:
        """True when the right behavior is to fire no skill at all."""
        return not self.expected_skills


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
    for child in sorted(SKILLS_ROOT.iterdir()):
        if not child.is_dir() or child.name in SKIP or child.name.startswith("."):
            continue
        skill_md = child / "SKILL.md"
        if not skill_md.is_file():
            continue
        metadata = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        name = metadata.get("name", "")
        description = metadata.get("description", "")
        if name:
            skills[name] = Skill(
                name=name,
                path=skill_md,
                description=description,
                user_invoked=metadata.get("disable-model-invocation", "").lower() == "true",
            )
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
                split=item.get("split", "train"),
            )
        )
    return cases


def tokenize(text: str) -> set[str]:
    """Tokenize English words, skill-name fragments, and short CJK n-grams.

    CJK bigrams are taken inside each run of CJK characters. Flattening the whole
    text first would join characters across a comma or an English word and invent
    grams no reader ever wrote: "写摘要, 写引言" would yield "要写".
    """
    lowered = text.lower().replace("-", " ")
    words = {
        token
        for token in re.findall(r"[a-z0-9][a-z0-9_]{2,}", lowered)
        if token not in STOPWORDS
    }
    cjk_grams: set[str] = set()
    for run in re.findall(r"[一-鿿]+", text):
        cjk_grams.update(run[index : index + 2] for index in range(len(run) - 1))
    return words | cjk_grams


def split_description(description: str) -> tuple[str, str]:
    """Split a description into the half that attracts and the anti-scope clause.

    A bag of words cannot represent negation, so the anti-scope clause must stay
    out of the attracting half — its words would pull the skill toward the very
    prompts it declares out of scope. It is scored separately instead, by
    `validate_antiscope`.
    """
    match = ANTISCOPE_MARKER.search(description)
    if not match:
        return description, ""
    cut = match.start(1)
    return description[:cut], description[cut:]


def metadata_tokens(skill: Skill) -> set[str]:
    """Return the pre-load tokens a router can infer from name and description."""
    positive_description, _ = split_description(skill.description)
    return tokenize(f"{skill.name.replace('-', ' ')} {positive_description}")


def antiscope_tokens(skill: Skill) -> set[str]:
    """Return the tokens that appear only in the skill's anti-scope clause.

    A word on both sides carries no sign — it cannot tell a router anything about
    the boundary — so only the exclusive words count as the declared boundary.
    """
    positive, negative = split_description(skill.description)
    if not negative:
        return set()
    return tokenize(negative) - tokenize(f"{skill.name.replace('-', ' ')} {positive}")


def similarity(prompt: str, skill: Skill) -> float:
    """Score how strongly one prompt resembles a skill's visible metadata."""
    prompt_tokens = tokenize(prompt)
    skill_tokens = metadata_tokens(skill)
    if not prompt_tokens or not skill_tokens:
        return 0.0
    overlap = len(prompt_tokens & skill_tokens)
    return overlap / math.sqrt(len(prompt_tokens) * len(skill_tokens))


def rank_skills(prompt: str, skills: dict[str, Skill]) -> list[tuple[str, float]]:
    """Rank skills by deterministic metadata similarity for smoke testing."""
    normalized_prompt = prompt.lower().replace("_", "-")
    scored = [
        (name, similarity(prompt, skill))
        for name, skill in skills.items()
        if not skill.user_invoked
        or name in normalized_prompt
        or name.replace("-", " ") in normalized_prompt
    ]
    return sorted(scored, key=lambda item: (-item[1], item[0]))


def validate_case_contract(cases: list[Case], skills: dict[str, Skill]) -> list[str]:
    """Validate that eval labels reference real skills and cover each skill both ways."""
    failures: list[str] = []
    skill_names = set(skills)
    ids = [case.id for case in cases]
    duplicate_ids = [case_id for case_id, count in Counter(ids).items() if count > 1]
    for case_id in duplicate_ids:
        failures.append(f"duplicate case id: {case_id}")

    positive_counts: Counter[tuple[str, str]] = Counter()
    negative_counts: Counter[tuple[str, str]] = Counter()
    for case in cases:
        if case.split not in SPLITS:
            failures.append(f"{case.id}: unknown split {case.split!r}")
        referenced = set(case.expected_skills) | set(case.forbidden_skills)
        unknown = sorted(referenced - skill_names)
        if unknown:
            failures.append(f"{case.id}: unknown skills {unknown}")
        for skill in case.expected_skills:
            positive_counts[(skill, case.split)] += 1
        for skill in case.forbidden_skills:
            negative_counts[(skill, case.split)] += 1
        if set(case.expected_skills) & set(case.forbidden_skills):
            failures.append(f"{case.id}: skill appears in both expected and forbidden")

    for skill_name in sorted(skill_names):
        for split in SPLITS:
            if positive_counts[(skill_name, split)] < 2:
                failures.append(f"{skill_name}: needs at least 2 positive cases in {split}")
            if negative_counts[(skill_name, split)] < 2:
                failures.append(f"{skill_name}: needs at least 2 forbidden cases in {split}")
    return failures


def smoke_test_metadata(cases: list[Case], skills: dict[str, Skill]) -> list[str]:
    """Run a cheap metadata-only overlap smoke test to flag broad descriptions."""
    failures: list[str] = []
    for case in cases:
        if any(skills[name].user_invoked for name in case.expected_skills):
            continue
        ranked = rank_skills(case.prompt, skills)
        top_name, top_score = ranked[0]
        expected = set(case.expected_skills)
        forbidden = set(case.forbidden_skills)

        if expected and top_name not in expected:
            expected_scores = {name: similarity(case.prompt, skills[name]) for name in expected}
            best_expected, best_score = max(expected_scores.items(), key=lambda item: item[1])
            if best_score < TIE_RATIO * top_score:
                failures.append(
                    f"{case.id}: metadata top={top_name}({top_score:.3f}) "
                    f"but expected {best_expected}({best_score:.3f})"
                )

        # When no skill should fire, which one happens to rank first is meaningless —
        # only whether anything scores high enough to fire. Judging an abstain case by
        # both rules sentences it twice, under two different thresholds.
        if expected and top_name in forbidden and top_score >= 0.10:
            best_expected = max(similarity(case.prompt, skills[name]) for name in expected)
            if best_expected < TIE_RATIO * top_score:
                failures.append(f"{case.id}: forbidden skill {top_name} ranks first ({top_score:.3f})")

        if not expected and top_score >= 0.25:
            failures.append(f"{case.id}: no expected skill but metadata top={top_name}({top_score:.3f})")
    return failures


def validate_antiscope(cases: list[Case], skills: dict[str, Skill]) -> list[str]:
    """Check that every declared anti-scope clause is exercised by a forbidden case.

    The clause is what a real router reads to decide *not* to fire a skill, so it
    is the half that most needs testing — and the half a bag-of-words smoke cannot
    score directly. Tie it to the goldens instead: a boundary nothing tests is a
    boundary that can name a skill deleted two refactors ago and never be caught.
    """
    failures: list[str] = []
    for name in sorted(skills):
        boundary = antiscope_tokens(skills[name])
        if not boundary:
            failures.append(f"{name}: description declares no anti-scope clause")
            continue
        covered = any(
            name in case.forbidden_skills and tokenize(case.prompt) & boundary
            for case in cases
        )
        if not covered:
            failures.append(
                f"{name}: anti-scope declares a boundary no forbidden case exercises "
                f"({sorted(boundary)[:6]}…)"
            )
    return failures










def print_summary(cases: list[Case], skills: dict[str, Skill]) -> None:
    """Print per-split coverage so maintainers can see weak eval areas."""
    counts: Counter[tuple[str, str, str]] = Counter()
    for case in cases:
        for skill in case.expected_skills:
            counts[(skill, case.split, "pos")] += 1
        for skill in case.forbidden_skills:
            counts[(skill, case.split, "forb")] += 1

    per_split = Counter(case.split for case in cases)
    print(
        f"Loaded {len(skills)} skills and {len(cases)} cases "
        f"({per_split['train']} train / {per_split['validation']} validation)."
    )
    for skill_name in sorted(skills):
        train = f"{counts[(skill_name, 'train', 'pos')]}+/{counts[(skill_name, 'train', 'forb')]}-"
        val = f"{counts[(skill_name, 'validation', 'pos')]}+/{counts[(skill_name, 'validation', 'forb')]}-"
        print(f"- {skill_name}: train {train}   validation {val}")



def main(argv: Iterable[str] | None = None) -> int:
    """Validate the trigger contract and run the metadata smoke test."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cases", type=Path, default=EVALS, help="Path to trigger cases JSON"
    )
    parser.add_argument(
        "--skip-smoke",
        action="store_true",
        help="Only validate labels and coverage; skip the metadata-overlap smoke test",
    )
    parser.add_argument(
        "--show-validation",
        action="store_true",
        help="Name the failing validation cases. Reading them is how a description "
             "gets fitted to the held-out half; use only to audit the split itself.",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    skills = load_skills()
    cases = load_cases(args.cases)
    print_summary(cases, skills)

    structural = validate_case_contract(cases, skills) + validate_antiscope(cases, skills)

    train = [case for case in cases if case.split == "train"]
    held_out = [case for case in cases if case.split == "validation"]
    train_failures: list[str] = []
    held_out_failures: list[str] = []
    if not args.skip_smoke:
        train_failures = smoke_test_metadata(train, skills)
        held_out_failures = smoke_test_metadata(held_out, skills)

    if structural:
        print("\nStructural failures:")
        for failure in structural:
            print(f"ERROR {failure}")

    if train_failures:
        print("\nTrain failures — revise the descriptions against these:")
        for failure in train_failures:
            print(f"ERROR {failure}")

    held_out_short = False
    if held_out:
        passed = len(held_out) - len(held_out_failures)
        rate = passed / len(held_out)
        held_out_short = rate < VALIDATION_FLOOR
        print(f"\nValidation: {passed}/{len(held_out)} passed ({rate:.0%}, "
              f"floor {VALIDATION_FLOOR:.0%}).")
    if held_out_failures:
        if args.show_validation:
            for failure in held_out_failures:
                print(f"ERROR {failure}")
        else:
            print(
                "Which cases failed is withheld. A drop here means the description "
                "was fitted to the train half; the fix is a description that "
                "generalises, not a patch aimed at whichever held-out prompt broke."
            )

    if structural or train_failures or held_out_short:
        return 1

    print("\nTrigger health checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
