#!/usr/bin/env python3
"""Validate a local Elsevier Editorial Manager packet from a JSON manifest."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


STATEMENTS = (
    ("CRediT authorship contribution statement", ("credit authorship contribution statement",)),
    ("Declaration of competing interest", ("declaration of competing interest",)),
    ("Acknowledgements / Funding", ("acknowledgements", "acknowledgments", "funding")),
    ("Data availability", ("data availability",)),
)
DOCX_PARTS = {"[Content_Types].xml", "_rels/.rels", "word/document.xml"}
WORD_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
CONTENT_TYPE_NS = {"ct": "http://schemas.openxmlformats.org/package/2006/content-types"}
RELATIONSHIP_NS = {"r": "http://schemas.openxmlformats.org/package/2006/relationships"}


@dataclass(frozen=True)
class JournalLimits:
    """Live journal limits that can be checked against local packet content."""

    abstract_max_words: int
    highlights_min_items: int | None
    highlights_max_items: int | None
    highlight_max_characters: int | None


@dataclass(frozen=True)
class PacketManifest:
    """Validated packet inputs resolved relative to the manifest file."""

    em_step: str
    em_step_checked_on: str
    journal_guide_url: str
    journal_limits_checked_on: str
    limits: JournalLimits
    manuscript: Path
    source_required: bool
    source_zip: Path | None
    source_entrypoint: str
    side_materials: tuple[Path, ...]
    submission_stage: str
    response_to_reviewers: Path | None
    marked_manuscript: Path | None


def resolve(base: Path, value: str) -> Path:
    """Resolve a manifest path relative to the manifest directory."""
    path = Path(value)
    return path if path.is_absolute() else base / path


def strip_tex_comments(text: str) -> str:
    """Remove unescaped TeX comments before structural checks."""
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in text.splitlines())


def manuscript_text(manuscript: Path) -> tuple[str | None, list[str]]:
    """Read canonical manuscript source once with TeX comments removed."""
    if not manuscript.is_file():
        return None, [f"manuscript does not exist: {manuscript}"]
    text = manuscript.read_text(encoding="utf-8", errors="replace")
    return strip_tex_comments(text), []


def check_statements(text: str) -> list[str]:
    """Verify required structural backmatter headings and their order."""
    headings = [
        (match.start(), re.sub(r"\\[A-Za-z]+", "", match.group(1)).lower())
        for match in re.finditer(
            r"\\(?:section|subsection|paragraph)\*?\s*\{([^{}]+)\}", text, re.IGNORECASE
        )
    ]
    positions: list[int] = []
    errors: list[str] = []
    for label, variants in STATEMENTS:
        position = next(
            (offset for offset, heading in headings if any(item in heading for item in variants)),
            -1,
        )
        if position < 0:
            errors.append(f"missing required statement heading: {label}")
        positions.append(position)
    present = [position for position in positions if position >= 0]
    if len(present) == len(positions) and present != sorted(present):
        errors.append("required statement headings are not in the required order")
    return errors


def parse_positive_int(raw: object, key: str, errors: list[str]) -> int | None:
    """Parse one positive integer manifest field."""
    if not isinstance(raw, int) or isinstance(raw, bool) or raw <= 0:
        errors.append(f"{key} must be a positive integer")
        return None
    return raw


KNOWN_MANIFEST_KEYS = frozenset(
    {
        "em_step",
        "em_step_checked_on",
        "journal_guide_url",
        "journal_limits_checked_on",
        "journal_limits",
        "manuscript",
        "source_required",
        "source_zip",
        "source_entrypoint",
        "side_materials",
        "submission_stage",
        "response_to_reviewers",
        "marked_manuscript",
    }
)

SUBMISSION_STAGES = ("initial", "revision")


def parse_manifest(raw: object, base: Path) -> tuple[PacketManifest | None, list[str]]:
    """Validate the JSON schema once before packet checks consume it."""
    if not isinstance(raw, dict):
        return None, ["manifest must be a JSON object"]
    errors: list[str] = []
    unknown = sorted(set(raw) - KNOWN_MANIFEST_KEYS)
    if unknown:
        # A silently ignored key is how a misspelled revision field turns into a
        # green packet that is missing the file it claimed to declare.
        errors.append(f"unknown manifest key(s): {', '.join(unknown)}")

    def required_string(key: str) -> str:
        value = raw.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{key} must be a non-empty string")
            return ""
        return value.strip()

    em_step = required_string("em_step")
    em_step_checked_on = required_string("em_step_checked_on")
    journal_guide_url = required_string("journal_guide_url")
    journal_limits_checked_on = required_string("journal_limits_checked_on")
    manuscript_value = required_string("manuscript")
    source_required = raw.get("source_required")
    if not isinstance(source_required, bool):
        errors.append("source_required must be true or false")
        source_required = False
    if "source" in em_step.lower() and not source_required:
        errors.append("an EM source step cannot set source_required to false")
    side_values = raw.get("side_materials")
    if (
        not isinstance(side_values, list)
        or not side_values
        or not all(isinstance(item, str) and item.strip() for item in side_values)
    ):
        errors.append("side_materials must be a non-empty JSON array of paths")
        side_values = []
    source_zip_value = raw.get("source_zip")
    if source_required and (not isinstance(source_zip_value, str) or not source_zip_value.strip()):
        errors.append("source_zip must be a non-empty path when source_required is true")
    source_entrypoint = raw.get("source_entrypoint", "main.tex")
    if not isinstance(source_entrypoint, str) or not source_entrypoint.strip():
        errors.append("source_entrypoint must be a non-empty path")
        source_entrypoint = "main.tex"

    submission_stage = raw.get("submission_stage")
    if submission_stage not in SUBMISSION_STAGES:
        errors.append(f"submission_stage must be one of {' or '.join(SUBMISSION_STAGES)}")
        submission_stage = ""
    response_value = raw.get("response_to_reviewers")
    if submission_stage == "revision" and (
        not isinstance(response_value, str) or not response_value.strip()
    ):
        errors.append("response_to_reviewers must be a non-empty path for a revision packet")
        response_value = None
    marked_value = raw.get("marked_manuscript")
    if marked_value is not None and (not isinstance(marked_value, str) or not marked_value.strip()):
        errors.append("marked_manuscript must be a non-empty path when present")
        marked_value = None

    raw_limits = raw.get("journal_limits")
    if not isinstance(raw_limits, dict):
        errors.append("journal_limits must be a JSON object with checked numeric limits")
        raw_limits = {}
    abstract_max_words = parse_positive_int(
        raw_limits.get("abstract_max_words"), "journal_limits.abstract_max_words", errors
    )
    highlight_paths = [item for item in side_values if "highlight" in Path(item).stem.lower()]
    highlight_values: list[int | None] = [None, None, None]
    if highlight_paths:
        highlight_values = [
            parse_positive_int(
                raw_limits.get(key), f"journal_limits.{key}", errors
            )
            for key in (
                "highlights_min_items",
                "highlights_max_items",
                "highlight_max_characters",
            )
        ]
        if all(item is not None for item in highlight_values):
            minimum, maximum, _ = highlight_values
            if minimum is not None and maximum is not None and minimum > maximum:
                errors.append("journal_limits highlights_min_items cannot exceed highlights_max_items")
    if errors:
        return None, errors
    assert abstract_max_words is not None
    return PacketManifest(
        em_step=em_step,
        em_step_checked_on=em_step_checked_on,
        journal_guide_url=journal_guide_url,
        journal_limits_checked_on=journal_limits_checked_on,
        limits=JournalLimits(
            abstract_max_words=abstract_max_words,
            highlights_min_items=highlight_values[0],
            highlights_max_items=highlight_values[1],
            highlight_max_characters=highlight_values[2],
        ),
        manuscript=resolve(base, manuscript_value),
        source_required=source_required,
        source_zip=resolve(base, source_zip_value) if isinstance(source_zip_value, str) else None,
        source_entrypoint=source_entrypoint,
        side_materials=tuple(resolve(base, item) for item in side_values),
        submission_stage=submission_stage,
        response_to_reviewers=(
            resolve(base, response_value) if isinstance(response_value, str) else None
        ),
        marked_manuscript=resolve(base, marked_value) if isinstance(marked_value, str) else None,
    ), []


def check_revision(manifest: PacketManifest) -> list[str]:
    """Require a revision packet to ship the files that answer the reviewers.

    The skill's completion criteria demand a point-by-point response and a
    clean/marked distinction. Both are declared as manifest paths, so both are
    checkable here — declaring a path that does not exist must not pass.
    """
    if manifest.submission_stage != "revision":
        return []
    errors: list[str] = []
    response = manifest.response_to_reviewers
    if response is None or not response.is_file():
        errors.append(f"response_to_reviewers is missing: {response}")
    marked = manifest.marked_manuscript
    if marked is not None:
        if not marked.is_file():
            errors.append(f"marked_manuscript is missing: {marked}")
        elif marked.resolve() == manifest.manuscript.resolve():
            errors.append("marked_manuscript must differ from the clean manuscript")
    return errors


def check_recent_date(label: str, raw_date: str, max_age_days: int) -> list[str]:
    """Require one evidence date to be valid, nonfuture, and recent."""
    try:
        checked = dt.date.fromisoformat(raw_date)
    except ValueError:
        return [f"{label} must use YYYY-MM-DD"]
    age = (dt.date.today() - checked).days
    if age < 0:
        return [f"{label} cannot be in the future"]
    if age > max_age_days:
        return [f"{label} is {age} days old; recheck it (max {max_age_days})"]
    return []


def check_guide(manifest: PacketManifest, max_age_days: int) -> list[str]:
    """Require live journal and current EM evidence to be recent."""
    errors: list[str] = []
    parsed = urlparse(manifest.journal_guide_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        errors.append("journal_guide_url must identify the live journal guide")
    errors.extend(
        check_recent_date(
            "journal_limits_checked_on", manifest.journal_limits_checked_on, max_age_days
        )
    )
    errors.extend(check_recent_date("em_step_checked_on", manifest.em_step_checked_on, max_age_days))
    return errors


def read_docx_paragraphs(path: Path) -> tuple[list[str] | None, list[str]]:
    """Validate core OOXML parts and extract Word paragraph text."""
    if path.suffix.lower() != ".docx" or not path.is_file():
        return None, [f"side-material DOCX does not exist: {path}"]
    if not zipfile.is_zipfile(path):
        return None, [f"side material is not a valid DOCX container: {path}"]
    with zipfile.ZipFile(path) as archive:
        missing = sorted(DOCX_PARTS - set(archive.namelist()))
        if missing:
            return None, [f"side material lacks required OOXML parts {missing}: {path}"]
        try:
            content_types = ET.fromstring(archive.read("[Content_Types].xml"))
            relationships = ET.fromstring(archive.read("_rels/.rels"))
            root = ET.fromstring(archive.read("word/document.xml"))
        except ET.ParseError as error:
            return None, [f"side material has invalid OOXML ({error}): {path}"]
    has_document_type = any(
        node.get("PartName") == "/word/document.xml"
        for node in content_types.findall("ct:Override", CONTENT_TYPE_NS)
    )
    has_document_relationship = any(
        node.get("Type", "").endswith("/officeDocument")
        and node.get("Target") == "word/document.xml"
        for node in relationships.findall("r:Relationship", RELATIONSHIP_NS)
    )
    expected_document_tag = f"{{{WORD_NS['w']}}}document"
    if not has_document_type or not has_document_relationship or root.tag != expected_document_tag:
        return None, [f"side material lacks a valid Word document content type or relationship: {path}"]
    paragraphs = []
    for paragraph in root.findall(".//w:p", WORD_NS):
        text = "".join(node.text or "" for node in paragraph.findall(".//w:t", WORD_NS)).strip()
        if text:
            paragraphs.append(text)
    if not paragraphs:
        return None, [f"side material contains no readable paragraphs: {path}"]
    return paragraphs, []


def check_docx(paths: tuple[Path, ...], limits: JournalLimits) -> list[str]:
    """Verify declared DOCX outputs and enforce recorded highlight limits."""
    errors: list[str] = []
    for path in paths:
        paragraphs, docx_errors = read_docx_paragraphs(path)
        errors.extend(docx_errors)
        if paragraphs is None or "highlight" not in path.stem.lower():
            continue
        items = paragraphs[1:] if paragraphs[0].strip().lower() == "highlights" else paragraphs
        minimum = limits.highlights_min_items or 1
        maximum = limits.highlights_max_items or minimum
        if not minimum <= len(items) <= maximum:
            errors.append(f"highlights item count is {len(items)}; expected {minimum}-{maximum}")
        max_chars = limits.highlight_max_characters or 1
        for index, item in enumerate(items, start=1):
            if len(item) > max_chars:
                errors.append(
                    f"highlight {index} has {len(item)} characters; maximum is {max_chars}"
                )
    return errors


def check_abstract(text: str, maximum: int) -> list[str]:
    """Enforce the recorded live abstract word limit against manuscript source."""
    match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.DOTALL)
    if not match:
        return ["manuscript lacks an abstract environment"]
    words = re.findall(r"\b[\w'-]+\b", re.sub(r"\\[A-Za-z]+", " ", match.group(1)))
    if len(words) > maximum:
        return [f"abstract has {len(words)} words; live journal maximum is {maximum}"]
    return []


def check_source_zip(path: Path, entrypoint: str) -> tuple[list[str], bool]:
    """Inspect a required flat ASCII source archive and compile it when possible."""
    if not path.is_file():
        return [f"source zip does not exist: {path}"], False
    if not zipfile.is_zipfile(path):
        return [f"source zip is not a readable zip archive: {path}"], False
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        errors = []
        for name in names:
            if name in {".", ".."} or name.endswith("/") or "/" in name or "\\" in name:
                errors.append(f"source zip is not flat: {name}")
            try:
                name.encode("ascii")
            except UnicodeEncodeError:
                errors.append(f"source zip filename is not ASCII: {name}")
        if entrypoint not in names:
            errors.append(f"source entrypoint is missing from zip: {entrypoint}")
        generated_pdf = str(Path(entrypoint).with_suffix(".pdf"))
        if generated_pdf in names:
            errors.append(f"source zip contains generated manuscript PDF: {generated_pdf}")
        if errors:
            return errors, False
        latexmk = shutil.which("latexmk")
        if not latexmk:
            return [
                "source zip structure passed, but standalone compile is blocked: install "
                "latexmk and a LaTeX runtime, then rerun the packet check"
            ], True
        with tempfile.TemporaryDirectory(prefix="elsevier-packet-") as tmp:
            workdir = Path(tmp)
            archive.extractall(workdir)
            result = subprocess.run(
                [latexmk, "-pdf", "-interaction=nonstopmode", "-halt-on-error", entrypoint],
                cwd=workdir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                excerpt = "\n".join(result.stdout.splitlines()[-20:])
                return [f"standalone source zip compile failed:\n{excerpt}"], False
            log_path = workdir / Path(entrypoint).with_suffix(".log")
            if not log_path.is_file():
                return ["standalone source zip compile did not produce a LaTeX log"], False
            log = log_path.read_text(encoding="utf-8", errors="replace")
            if "undefined references" in log.lower() or "undefined citations" in log.lower():
                return ["standalone source zip compile has undefined references or citations"], False
    return [], False


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Check an Elsevier EM packet manifest")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--max-evidence-age-days", type=int, default=30)
    args = parser.parse_args()
    try:
        raw_manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"manifest error: {error}")
        return 1
    base = args.manifest.resolve().parent
    manifest, errors = parse_manifest(raw_manifest, base)
    if manifest is None:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    errors.extend(check_guide(manifest, args.max_evidence_age_days))
    errors.extend(check_revision(manifest))
    text, manuscript_errors = manuscript_text(manifest.manuscript)
    errors.extend(manuscript_errors)
    if text is not None:
        errors.extend(check_statements(text))
        errors.extend(check_abstract(text, manifest.limits.abstract_max_words))
    errors.extend(check_docx(manifest.side_materials, manifest.limits))

    blocked = False
    if manifest.source_required:
        source_errors, blocked = check_source_zip(
            manifest.source_zip or base,
            manifest.source_entrypoint,
        )
        errors.extend(source_errors)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 2 if blocked and len(errors) == 1 else 1
    print("Elsevier packet check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
