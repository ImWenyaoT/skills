#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


SLOTS = ("recognition", "character", "trajectory")
CLAIM_TYPES = {"verified_fact", "user_statement", "inference"}
EVIDENCE_CLASSES = {"external_recognition", "behavior", "direction"}
PROJECTION_STATES = {"not_requested", "drafted", "included"}
SOURCE_KINDS = {"external_artifact", "candidate_material", "user_statement"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def normalize(value: str) -> str:
    return re.sub(r"\s+", "", value).casefold()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    args = parser.parse_args()

    profile_path = args.profile.resolve()
    workspace = args.workspace.resolve()
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    errors: list[str] = []

    if profile.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if profile.get("visibility") != "main_only":
        errors.append("visibility must be main_only")
    if profile_path != workspace / ".offer-magic" / "grill-resume" / "candidate-profile.json":
        errors.append("candidate profile must use the main-only workspace path")
    if not isinstance(profile.get("updated_reason"), str) or not profile["updated_reason"].strip():
        errors.append("updated_reason must be non-empty")

    sources: dict[str, tuple[str, str]] = {}
    source_files = profile.get("source_files")
    if not isinstance(source_files, list) or not source_files:
        errors.append("source_files must be a non-empty list")
        source_files = []
    for index, item in enumerate(source_files):
        if not isinstance(item, dict):
            errors.append(f"source_files[{index}] must be an object")
            continue
        relative = item.get("path")
        expected_hash = item.get("sha256")
        source_kind = item.get("kind")
        if not isinstance(relative, str) or not relative.strip():
            errors.append(f"source_files[{index}].path must be non-empty")
            continue
        if source_kind not in SOURCE_KINDS:
            errors.append(f"source_files[{index}].kind is invalid")
        source = (workspace / relative).resolve()
        try:
            source.relative_to(workspace)
        except ValueError:
            errors.append(f"source_files[{index}] escapes the workspace")
            continue
        if source == profile_path:
            errors.append("candidate profile cannot cite itself")
            continue
        if not source.is_file():
            errors.append(f"source file missing: {relative}")
            continue
        actual_hash = digest(source)
        if expected_hash != actual_hash:
            errors.append(f"source hash mismatch: {relative}")
        sources[relative] = (
            source.read_text(encoding="utf-8", errors="ignore"),
            source_kind,
        )

    slots = profile.get("slots")
    if not isinstance(slots, dict) or set(slots) != set(SLOTS):
        errors.append("slots must contain recognition, character, and trajectory only")
        slots = {}

    for slot_name in SLOTS:
        slot = slots.get(slot_name)
        if not isinstance(slot, dict):
            errors.append(f"slots.{slot_name} must be an object")
            continue
        status = slot.get("status")
        summary = slot.get("summary")
        claims = slot.get("claims")
        questions = slot.get("open_questions")
        confidence = slot.get("confidence")

        if status not in {"supported", "missing"}:
            errors.append(f"slots.{slot_name}.status must be supported or missing")
        if not isinstance(claims, list):
            errors.append(f"slots.{slot_name}.claims must be a list")
            claims = []
        if not isinstance(questions, list) or any(not isinstance(value, str) for value in questions):
            errors.append(f"slots.{slot_name}.open_questions must be a string list")
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 1:
            errors.append(f"slots.{slot_name}.confidence must be between 0 and 1")

        if status == "missing":
            if summary is not None:
                errors.append(f"slots.{slot_name}.summary must be null when missing")
            if claims:
                errors.append(f"slots.{slot_name}.claims must be empty when missing")
            continue
        if not isinstance(summary, str) or not summary.strip():
            errors.append(f"slots.{slot_name}.summary must be non-empty when supported")
        if not claims:
            errors.append(f"slots.{slot_name}.claims must be non-empty when supported")

        for index, claim in enumerate(claims):
            prefix = f"slots.{slot_name}.claims[{index}]"
            if not isinstance(claim, dict):
                errors.append(f"{prefix} must be an object")
                continue
            claim_type = claim.get("type")
            evidence_class = claim.get("evidence_class")
            if claim_type not in CLAIM_TYPES:
                errors.append(f"{prefix}.type is invalid")
            if evidence_class not in EVIDENCE_CLASSES:
                errors.append(f"{prefix}.evidence_class is invalid")
            if evidence_class != {
                "recognition": "external_recognition",
                "character": "behavior",
                "trajectory": "direction",
            }[slot_name]:
                errors.append(f"{prefix}.evidence_class does not match its slot")
            for field in ("text", "source", "quote"):
                if not isinstance(claim.get(field), str) or not claim[field].strip():
                    errors.append(f"{prefix}.{field} must be non-empty")
            source_name = claim.get("source")
            quote = claim.get("quote")
            if not isinstance(source_name, str) or source_name not in sources:
                errors.append(f"{prefix}.source is not registered")
            elif isinstance(quote, str) and quote.strip():
                source_text, source_kind = sources[source_name]
                if normalize(quote) not in normalize(source_text):
                    errors.append(f"{prefix}.quote is not present in its source")
                if claim_type == "verified_fact" and source_kind != "external_artifact":
                    errors.append(f"{prefix}.verified_fact needs an external_artifact source")
                if claim_type == "user_statement" and source_kind not in {
                    "candidate_material",
                    "user_statement",
                }:
                    errors.append(f"{prefix}.user_statement needs a candidate statement source")
            if claim_type == "inference":
                if not isinstance(claim.get("basis"), str) or not claim["basis"].strip():
                    errors.append(f"{prefix}.basis must be non-empty for inference")
                value = claim.get("confidence")
                if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 <= value <= 1:
                    errors.append(f"{prefix}.confidence must be between 0 and 1 for inference")

        if slot_name == "recognition" and claims and not any(
            claim.get("type") in {"verified_fact", "user_statement"}
            and claim.get("evidence_class") == "external_recognition"
            for claim in claims
            if isinstance(claim, dict)
        ):
            errors.append("recognition needs external evidence, not inference alone")
        if slot_name == "trajectory" and claims and not any(
            claim.get("type") in {"verified_fact", "user_statement"}
            for claim in claims
            if isinstance(claim, dict)
        ):
            errors.append("trajectory needs a stated direction or current fact")

    abstract = profile.get("abstract")
    if not isinstance(abstract, dict):
        errors.append("abstract must be an object")
    else:
        status = abstract.get("status")
        sentences = abstract.get("sentences")
        projection = abstract.get("resume_projection")
        projection_evidence = abstract.get("resume_projection_evidence")
        if projection not in PROJECTION_STATES:
            errors.append("abstract.resume_projection is invalid")
        if projection == "not_requested" and projection_evidence is not None:
            errors.append("not_requested projection must not have authorization evidence")
        if projection in {"drafted", "included"}:
            if not isinstance(projection_evidence, dict):
                errors.append("visible projection requires explicit user-request evidence")
            else:
                source_name = projection_evidence.get("source")
                quote = projection_evidence.get("quote")
                if not isinstance(source_name, str) or source_name not in sources:
                    errors.append("projection authorization source is not registered")
                elif sources[source_name][1] not in {"candidate_material", "user_statement"}:
                    errors.append("projection authorization must come from a user statement source")
                elif not isinstance(quote, str) or not quote.strip():
                    errors.append("projection authorization quote must be non-empty")
                elif normalize(quote) not in normalize(sources[source_name][0]):
                    errors.append("projection authorization quote is not present in its source")
        if not isinstance(sentences, list):
            errors.append("abstract.sentences must be a list")
            sentences = []
        all_supported = all(
            isinstance(slots.get(name), dict) and slots[name].get("status") == "supported"
            for name in SLOTS
        )
        if status == "complete":
            if not all_supported:
                errors.append("complete abstract requires three supported slots")
            if len(sentences) != 3:
                errors.append("complete abstract requires exactly three sentences")
            else:
                kinds = [item.get("kind") for item in sentences if isinstance(item, dict)]
                if kinds != list(SLOTS):
                    errors.append("abstract sentence order must be recognition, character, trajectory")
                for item in sentences:
                    if not isinstance(item, dict):
                        continue
                    kind = item.get("kind")
                    text = item.get("text")
                    if kind in slots and text != slots[kind].get("summary"):
                        errors.append(f"abstract sentence for {kind} must equal slot summary")
        elif status == "incomplete":
            if all_supported:
                errors.append("incomplete abstract requires at least one missing slot")
            if sentences:
                errors.append("incomplete abstract must not generate partial sentences")
        elif status == "not_generated":
            if sentences:
                errors.append("not_generated abstract must have no sentences")
        else:
            errors.append("abstract.status must be complete, incomplete, or not_generated")

    if errors:
        raise SystemExit("candidate profile validation failed:\n- " + "\n- ".join(errors))
    print("candidate profile valid")


if __name__ == "__main__":
    main()
