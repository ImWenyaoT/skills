#!/usr/bin/env python3
"""Evaluate skill trigger health from golden prompts and optional trace predictions.

The default mode is an offline contract check: it verifies that every local skill
has positive and negative coverage in evals/trigger_cases.json, then runs a small
metadata-similarity smoke test to catch obviously overlapping descriptions.

For real trigger metrics, pass --predictions JSONL with one record PER RUN:
  {"id": "case-id", "actual_skills": ["writing-papers"]}
Repeat the same id across multiple lines to record multiple trials of one case;
that unlocks pass@k / pass^k reliability metrics. A single line per id == 1 trial.

The scorer answers two separable questions (Anthropic Claude Code guidance):
  (A) ROUTING  — did the right skill TRIGGER and the wrong ones stay silent?
                 -> per-skill / macro / micro / weighted precision-recall-F1,
                    abstain false-trigger rate, confusion matrix, pass@k / pass^k.
  (B) OUTCOME  — given a skill triggered, did following it produce a GOOD result?
                 -> --outcomes JSONL of code-graded / LLM-judge assertion results.
Pass --baseline-predictions (skills disabled) to confirm the skill is what changed
behavior.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
EVALS = ROOT / "evals" / "trigger_cases.json"
SKIP = {"scripts", ".git", ".github", "evals"}
NONE_LABEL = "<none>"  # explicit abstain class so "fire nothing" is first-class
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
    user_invoked: bool


@dataclass(frozen=True)
class Case:
    """Store one golden trigger case."""

    id: str
    prompt: str
    expected_skills: tuple[str, ...]
    forbidden_skills: tuple[str, ...]
    notes: str

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
    cjk_chars = re.findall(r"[一-鿿]", text)
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
        if any(skills[name].user_invoked for name in case.expected_skills):
            continue
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


def load_predictions(path: Path) -> dict[str, list[tuple[str, ...]]]:
    """Load JSONL predictions as id -> list of per-trial fired-skill tuples.

    Each line is ONE trial: {"id": ..., "actual_skills": [...]}. Repeating an id
    across lines records multiple trials of the same case (for pass@k / pass^k).
    Back-compatible with the old one-line-per-id format (yields a 1-trial list).
    """
    predictions: dict[str, list[tuple[str, ...]]] = defaultdict(list)
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
            predictions[case_id].append(tuple(str(skill) for skill in actual))
    return dict(predictions)


def load_outcomes(path: Path) -> dict[str, tuple[int, int]]:
    """Load layer-(B) outcome grading as id -> (assertions_passed, assertions_total).

    Accepts either explicit assertion counts
      {"id": ..., "assertions_passed": 3, "assertions_total": 4}
    or a boolean pass {"id": ..., "passed": true} (treated as 1/1).
    """
    outcomes: dict[str, tuple[int, int]] = {}
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            item = json.loads(stripped)
            case_id = item.get("id")
            if not isinstance(case_id, str):
                raise ValueError(f"{path}:{line_no}: expected string id")
            if "assertions_total" in item:
                passed = int(item.get("assertions_passed", 0))
                total = int(item["assertions_total"])
            elif "passed" in item:
                passed, total = (1, 1) if item["passed"] else (0, 1)
            else:
                raise ValueError(f"{path}:{line_no}: need assertions_total or passed")
            outcomes[case_id] = (passed, total)
    return outcomes


def _prf(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    """Return (precision, recall, f1) from a confusion tally; empty class -> 1.0."""
    precision = tp / (tp + fp) if (tp + fp) else 1.0
    recall = tp / (tp + fn) if (tp + fn) else 1.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return precision, recall, f1


def pass_at_k(n: int, c: int, k: int) -> float | None:
    """Probability >=1 of k sampled runs succeeds, given c successes in n runs."""
    if k > n:
        return None
    if c == 0:
        return 0.0
    if n - c < k:  # fewer than k failures -> every k-subset contains a success
        return 1.0
    return 1.0 - math.comb(n - c, k) / math.comb(n, k)


def pass_hat_k(n: int, c: int, k: int) -> float | None:
    """Probability ALL k sampled runs succeed, given c successes in n runs."""
    if k > n:
        return None
    if c < k:
        return 0.0
    return math.comb(c, k) / math.comb(n, k)


def compute_routing_metrics(
    cases: list[Case],
    predictions: dict[str, list[tuple[str, ...]]],
    skills: dict[str, Skill],
    pass_k: int,
) -> dict:
    """Compute the full layer-(A) routing report over all (case, trial) samples.

    Treats every trial of every case as one sample for precision/recall/F1, and
    computes pass@k / pass^k per case across its trials. Returns a dict with
    per-skill tallies, macro/micro/weighted F1, abstain (false-trigger) metrics,
    selection accuracy, a confusion matrix, pass metrics, and per-case failures.
    """
    skill_names = sorted(skills)
    # Per-skill confusion tallies summed over all (case, trial) samples.
    tp: Counter[str] = Counter()
    fp: Counter[str] = Counter()
    fn: Counter[str] = Counter()
    support: Counter[str] = Counter()  # gold-positive samples per skill (for weighting)

    micro_tp = micro_fp = micro_fn = 0
    forbidden_hits = 0
    selection_ok = 0
    sample_total = 0

    # Abstain ("fire nothing") as a first-class class.
    none_tp = none_fp = none_fn = 0
    abstain_runs = 0
    abstain_false_fires = 0

    confusion: Counter[tuple[str, str]] = Counter()  # (gold, predicted) for 1-expected cases
    pass_at_k_vals: list[float] = []
    pass_hat_k_vals: list[float] = []
    failures: list[str] = []

    for case in cases:
        runs = predictions.get(case.id)
        if not runs:
            failures.append(f"{case.id}: no prediction trials provided")
            continue
        expected = set(case.expected_skills)
        forbidden = set(case.forbidden_skills)

        successes = 0
        for actual_tuple in runs:
            actual = set(actual_tuple)
            sample_total += 1

            # Per-skill + micro confusion over the full skill vocabulary.
            for name in skill_names:
                gold_pos = name in expected
                pred_pos = name in actual
                if gold_pos:
                    support[name] += 1
                if gold_pos and pred_pos:
                    tp[name] += 1
                    micro_tp += 1
                elif pred_pos and not gold_pos:
                    fp[name] += 1
                    micro_fp += 1
                elif gold_pos and not pred_pos:
                    fn[name] += 1
                    micro_fn += 1

            forbidden_hits += len(actual & forbidden)

            # Abstain class bookkeeping.
            gold_none = case.is_abstain
            pred_none = not actual
            if gold_none and pred_none:
                none_tp += 1
            elif pred_none and not gold_none:
                none_fp += 1
            elif gold_none and not pred_none:
                none_fn += 1
            if gold_none:
                abstain_runs += 1
                if actual:
                    abstain_false_fires += 1

            # Selection accuracy: needed skill(s) fired (abstain == fired nothing).
            if (gold_none and pred_none) or (expected and expected.issubset(actual)):
                selection_ok += 1

            # Confusion matrix for single-expected cases.
            if len(expected) == 1:
                gold = next(iter(expected))
                preds = sorted(actual) if actual else [NONE_LABEL]
                for pred in preds:
                    confusion[(gold, pred)] += 1

            # Exact-set match defines a successful trial (abstain-respecting).
            if actual == expected:
                successes += 1

            if (expected - actual) or (actual - expected) or (actual & forbidden):
                failures.append(
                    f"{case.id}: missing={sorted(expected - actual)} "
                    f"extra={sorted(actual - expected)} "
                    f"forbidden_hits={sorted(actual & forbidden)} actual={sorted(actual)}"
                )

        n = len(runs)
        pak = pass_at_k(n, successes, pass_k)
        phk = pass_hat_k(n, successes, pass_k)
        if pak is not None:
            pass_at_k_vals.append(pak)
        if phk is not None:
            pass_hat_k_vals.append(phk)

    # Per-skill precision/recall/F1 + the three averaging schemes.
    per_skill: dict[str, dict[str, float]] = {}
    f1s: list[float] = []
    weighted_num = 0.0
    weighted_den = 0
    for name in skill_names:
        p, r, f1 = _prf(tp[name], fp[name], fn[name])
        per_skill[name] = {
            "precision": p,
            "recall": r,
            "f1": f1,
            "support": support[name],
            "tp": tp[name],
            "fp": fp[name],
            "fn": fn[name],
        }
        f1s.append(f1)
        weighted_num += support[name] * f1
        weighted_den += support[name]

    micro_p, micro_r, micro_f1 = _prf(micro_tp, micro_fp, micro_fn)
    macro_f1 = sum(f1s) / len(f1s) if f1s else 0.0
    weighted_f1 = weighted_num / weighted_den if weighted_den else 0.0
    none_p, none_r, none_f1 = _prf(none_tp, none_fp, none_fn)

    return {
        "per_skill": per_skill,
        "precision": micro_p,
        "recall": micro_r,
        "f1": micro_f1,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "forbidden_hits": forbidden_hits,
        "false_trigger_rate": (abstain_false_fires / abstain_runs) if abstain_runs else 0.0,
        "abstain_runs": abstain_runs,
        "none_precision": none_p,
        "none_recall": none_r,
        "none_f1": none_f1,
        "selection_accuracy": (selection_ok / sample_total) if sample_total else 1.0,
        "confusion": confusion,
        "pass_at_k": (sum(pass_at_k_vals) / len(pass_at_k_vals)) if pass_at_k_vals else 1.0,
        "pass_hat_k": (sum(pass_hat_k_vals) / len(pass_hat_k_vals)) if pass_hat_k_vals else 1.0,
        "pass_k": pass_k,
        "sample_total": sample_total,
        "failures": failures,
    }


def compute_outcome_metrics(cases: list[Case], outcomes: dict[str, tuple[int, int]]) -> dict:
    """Compute layer-(B) outcome quality over cases that should trigger a skill."""
    assertions_passed = assertions_total = 0
    cases_full_pass = cases_graded = 0
    missing: list[str] = []
    for case in cases:
        if case.is_abstain:
            continue  # outcome grading only applies when a skill should run
        if case.id not in outcomes:
            missing.append(case.id)
            continue
        passed, total = outcomes[case.id]
        assertions_passed += passed
        assertions_total += total
        cases_graded += 1
        if total and passed == total:
            cases_full_pass += 1
    return {
        "assertion_pass_rate": (assertions_passed / assertions_total) if assertions_total else 1.0,
        "case_pass_rate": (cases_full_pass / cases_graded) if cases_graded else 1.0,
        "cases_graded": cases_graded,
        "missing": missing,
    }


def compare_baseline(
    cases: list[Case],
    predictions: dict[str, list[tuple[str, ...]]],
    baseline: dict[str, list[tuple[str, ...]]],
) -> dict:
    """Diff with-skill vs skills-disabled fired behavior to prove the skill is the cause."""
    changed = 0
    compared = 0
    examples: list[str] = []
    for case in cases:
        with_runs = predictions.get(case.id)
        base_runs = baseline.get(case.id)
        if not with_runs or not base_runs:
            continue
        compared += 1
        with_set = set(with_runs[0])
        base_set = set(base_runs[0])
        if with_set != base_set:
            changed += 1
            if len(examples) < 8:
                examples.append(
                    f"{case.id}: baseline={sorted(base_set) or ['<none>']} -> with={sorted(with_set) or ['<none>']}"
                )
    return {
        "compared": compared,
        "changed": changed,
        "change_rate": (changed / compared) if compared else 0.0,
        "examples": examples,
    }


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


def print_routing_report(metrics: dict) -> None:
    """Render the layer-(A) routing metrics block for humans and CI logs."""
    print(
        "\nRouting metrics (over {n} trials):".format(n=metrics["sample_total"])
    )
    print(
        f"  micro    precision={metrics['precision']:.3f} recall={metrics['recall']:.3f} f1={metrics['f1']:.3f}"
    )
    print(f"  macro-F1={metrics['macro_f1']:.3f}  weighted-F1={metrics['weighted_f1']:.3f}")
    print(
        f"  abstain  false_trigger_rate={metrics['false_trigger_rate']:.3f} "
        f"(over {metrics['abstain_runs']} abstain trials)  none-F1={metrics['none_f1']:.3f}"
    )
    print(
        f"  selection_accuracy={metrics['selection_accuracy']:.3f}  forbidden_hits={metrics['forbidden_hits']}"
    )
    k = metrics["pass_k"]
    print(f"  pass@{k}={metrics['pass_at_k']:.3f}  pass^{k}={metrics['pass_hat_k']:.3f}")

    print("\nPer-skill routing (precision / recall / f1 / support):")
    for name, row in sorted(metrics["per_skill"].items()):
        print(
            f"  {name:<38} P={row['precision']:.2f} R={row['recall']:.2f} "
            f"F1={row['f1']:.2f} n={row['support']}"
        )

    off_diagonal = sorted(
        ((g, p, c) for (g, p), c in metrics["confusion"].items() if g != p),
        key=lambda item: -item[2],
    )
    if off_diagonal:
        print("\nConfusion (gold -> wrongly fired, single-expected cases):")
        for gold, pred, count in off_diagonal:
            print(f"  {gold} -> {pred}: {count}")


def main(argv: Iterable[str] | None = None) -> int:
    """Run trigger-contract validation and optional prediction/outcome scoring."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=EVALS, help="Path to trigger cases JSON")
    parser.add_argument("--predictions", type=Path, help="JSONL of actual_skills, one line per trial")
    parser.add_argument("--baseline-predictions", type=Path, help="JSONL captured with skills disabled")
    parser.add_argument("--outcomes", type=Path, help="JSONL of layer-(B) outcome grading results")
    parser.add_argument("--pass-k", type=int, default=1, help="k for pass@k / pass^k reliability")
    # Layer-(A) gates (only enforced when --predictions is given).
    parser.add_argument("--min-precision", type=float, default=0.90, help="Min micro precision")
    parser.add_argument("--min-recall", type=float, default=0.90, help="Min micro recall")
    parser.add_argument("--min-f1", type=float, default=0.90, help="Min micro F1")
    parser.add_argument("--min-macro-f1", type=float, default=0.0, help="Min macro-F1 (per-skill equal weight)")
    parser.add_argument("--max-false-trigger-rate", type=float, default=1.0, help="Max abstain false-trigger rate")
    parser.add_argument("--min-pass-hat-k", type=float, default=0.0, help="Min mean pass^k reliability")
    # Layer-(B) gate (only enforced when --outcomes is given).
    parser.add_argument("--min-outcome-pass-rate", type=float, default=0.0, help="Min outcome assertion pass rate")
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
        predictions = load_predictions(args.predictions)
        metrics = compute_routing_metrics(cases, predictions, skills, args.pass_k)
        failures.extend(metrics["failures"])
        print_routing_report(metrics)

        # Layer-(A) threshold gates.
        if metrics["precision"] < args.min_precision:
            failures.append(f"micro precision {metrics['precision']:.3f} below {args.min_precision:.3f}")
        if metrics["recall"] < args.min_recall:
            failures.append(f"micro recall {metrics['recall']:.3f} below {args.min_recall:.3f}")
        if metrics["f1"] < args.min_f1:
            failures.append(f"micro f1 {metrics['f1']:.3f} below {args.min_f1:.3f}")
        if metrics["macro_f1"] < args.min_macro_f1:
            failures.append(f"macro-f1 {metrics['macro_f1']:.3f} below {args.min_macro_f1:.3f}")
        if metrics["false_trigger_rate"] > args.max_false_trigger_rate:
            failures.append(
                f"false-trigger-rate {metrics['false_trigger_rate']:.3f} above {args.max_false_trigger_rate:.3f}"
            )
        if metrics["pass_hat_k"] < args.min_pass_hat_k:
            failures.append(f"pass^{args.pass_k} {metrics['pass_hat_k']:.3f} below {args.min_pass_hat_k:.3f}")

        if args.baseline_predictions:
            baseline = load_predictions(args.baseline_predictions)
            delta = compare_baseline(cases, predictions, baseline)
            print(
                f"\nBaseline delta: {delta['changed']}/{delta['compared']} cases changed "
                f"(change_rate={delta['change_rate']:.3f})"
            )
            for example in delta["examples"]:
                print(f"  {example}")

    if args.outcomes:
        outcome_metrics = compute_outcome_metrics(cases, load_outcomes(args.outcomes))
        print(
            f"\nOutcome metrics: assertion_pass_rate={outcome_metrics['assertion_pass_rate']:.3f} "
            f"case_pass_rate={outcome_metrics['case_pass_rate']:.3f} "
            f"(graded {outcome_metrics['cases_graded']} should-trigger cases)"
        )
        if outcome_metrics["missing"]:
            print(f"  ungraded should-trigger cases: {len(outcome_metrics['missing'])}")
        if outcome_metrics["assertion_pass_rate"] < args.min_outcome_pass_rate:
            failures.append(
                f"outcome pass-rate {outcome_metrics['assertion_pass_rate']:.3f} below {args.min_outcome_pass_rate:.3f}"
            )

    if failures:
        print("\nTrigger health failures:")
        for failure in failures:
            print(f"ERROR {failure}")
        return 1

    print("\nTrigger health checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
