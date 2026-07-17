#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter")
    try:
        raw, body = text[4:].split("\n---\n", 1)
    except ValueError as error:
        raise ValueError(f"{path}: unclosed YAML frontmatter") from error
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.startswith((" ", "\t")):
            continue
        key, separator, value = line.partition(":")
        if separator:
            data[key.strip()] = value.strip().strip('"')
    return data, body


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        meta, body = frontmatter(path)
    except ValueError as error:
        return [str(error)]

    name = meta.get("name", "")
    description = meta.get("description", "")
    if not NAME.fullmatch(name):
        errors.append(f"{path}: invalid name {name!r}")
    if name != path.parent.name:
        errors.append(f"{path}: name must match directory {path.parent.name!r}")
    if not 1 <= len(description) <= 1024:
        errors.append(f"{path}: description must be 1-1024 characters")
    if len(body.splitlines()) > 500:
        errors.append(f"{path}: body exceeds 500 lines")

    for target in LINK.findall(body):
        target = target.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            errors.append(f"{path}: broken link {target!r}")

    metadata = path.parent / "agents" / "openai.yaml"
    if not metadata.is_file():
        errors.append(f"{path}: missing agents/openai.yaml")
    else:
        content = metadata.read_text(encoding="utf-8")
        for field in ("display_name:", "short_description:", "default_prompt:"):
            if field not in content:
                errors.append(f"{metadata}: missing {field[:-1]}")
    return errors


def validate_evals() -> list[str]:
    errors: list[str] = []
    skills = {"offer-magic", "grill-resume", "grill-interview"}
    trigger_path = ROOT / "evals" / "trigger-cases.json"
    behavior_path = ROOT / "evals" / "behavior-cases.json"
    try:
        triggers = json.loads(trigger_path.read_text(encoding="utf-8"))
        behaviors = json.loads(behavior_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"evals: {error}"]

    counts: Counter[str | None] = Counter()
    for index, case in enumerate(triggers):
        expected = case.get("expected_skill")
        if expected is not None and expected not in skills:
            errors.append(f"trigger case {index}: unknown skill {expected!r}")
        if not case.get("query") or case.get("invocation") not in {"explicit", "implicit"}:
            errors.append(f"trigger case {index}: invalid query or invocation")
        counts[expected] += 1
    for skill in skills - {"offer-magic"}:
        if counts[skill] < 2:
            errors.append(f"trigger evals need at least two positives for {skill}")
    if counts[None] < 2:
        errors.append("trigger evals need at least two near-miss negatives")

    for index, case in enumerate(behaviors):
        if case.get("skill") not in skills or not case.get("request"):
            errors.append(f"behavior case {index}: invalid skill or request")
        assertions = case.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            errors.append(f"behavior case {index}: assertions must be non-empty")
    return errors


def main() -> None:
    skill_files = [
        ROOT / "SKILL.md",
        ROOT / "grill-resume" / "SKILL.md",
        ROOT / "grill-interview" / "SKILL.md",
    ]
    errors = [error for path in skill_files for error in validate_skill(path)]
    errors.extend(validate_evals())

    router_metadata = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
    if "allow_implicit_invocation: false" not in router_metadata:
        errors.append("router must disable implicit invocation in agents/openai.yaml")
    legacy_story_bank = ROOT / "grill-interview" / "story-bank"
    if legacy_story_bank.exists() and any(legacy_story_bank.iterdir()):
        errors.append("candidate story state must not live inside the skill bundle")
    expected_subagents = {
        "grill-resume/subagents/hr-reviewer.md",
        "grill-interview/subagents/interviewer.md",
    }
    actual_subagents = {
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*")
        if path.is_file() and "subagents" in path.relative_to(ROOT).parts
    }
    if actual_subagents != expected_subagents:
        errors.append(
            "bundle must contain exactly the HR Reviewer and Interviewer subagents"
        )
    if list(ROOT.rglob("candidate-profile.json")):
        errors.append("candidate profile state must not live inside the skill bundle")

    if errors:
        raise SystemExit("bundle validation failed:\n- " + "\n- ".join(errors))
    print(
        f"bundle valid: {len(skill_files)} skills; "
        "trigger and behavior eval schemas valid (model selection not executed)"
    )


if __name__ == "__main__":
    main()
