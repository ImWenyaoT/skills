#!/usr/bin/env python3
"""Validate a local journal submission packet from a JSON manifest."""
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


PUBLISHERS = ("elsevier", "ieee")
SUBMISSION_STAGES = ("initial", "revision")

# Keys every publisher shares, plus the extra keys one publisher adds. The union
# is a closed set: a key that belongs to the other publisher is as wrong as a
# misspelled one, because the check it names never runs here.
COMMON_KEYS = frozenset(
    {
        "publisher",
        "submission_step",
        "submission_step_checked_on",
        "journal_guide_url",
        "journal_limits_checked_on",
        "journal_limits",
        "manuscript",
        "side_materials",
        "submission_stage",
        "response_to_reviewers",
        "source_required",
        "source_zip",
        "source_entrypoint",
    }
)
PUBLISHER_KEYS = {
    "elsevier": frozenset({"marked_manuscript"}),
    "ieee": frozenset({"manuscript_pdf", "edics", "supplemental_pdf", "difference_statement"}),
}
COMMON_LIMIT_KEYS = frozenset({"abstract_max_words"})
PUBLISHER_LIMIT_KEYS = {
    "elsevier": frozenset(
        {"highlights_min_items", "highlights_max_items", "highlight_max_characters"}
    ),
    "ieee": frozenset({"abstract_min_words", "max_pages", "supplemental_max_pages"}),
}

# Elsevier mandates these back-matter headings and this order.
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
    abstract_min_words: int | None = None
    max_pages: int | None = None
    supplemental_max_pages: int | None = None
    highlights_min_items: int | None = None
    highlights_max_items: int | None = None
    highlight_max_characters: int | None = None


@dataclass(frozen=True)
class PacketManifest:
    """Validated packet inputs resolved relative to the manifest file."""

    publisher: str
    submission_step: str
    submission_step_checked_on: str
    journal_guide_url: str
    journal_limits_checked_on: str
    limits: JournalLimits
    manuscript: Path
    side_materials: tuple[Path, ...]
    submission_stage: str
    response_to_reviewers: Path | None
    source_required: bool
    source_zip: Path | None
    source_entrypoint: str
    marked_manuscript: Path | None = None
    manuscript_pdf: Path | None = None
    edics: tuple[str, ...] = ()
    supplemental_pdf: Path | None = None
    difference_statement: Path | None = None


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


def parse_positive_int(raw: object, key: str, errors: list[str]) -> int | None:
    """Parse one positive integer manifest field."""
    if not isinstance(raw, int) or isinstance(raw, bool) or raw <= 0:
        errors.append(f"{key} must be a positive integer")
        return None
    return raw


def parse_manifest(raw: object, base: Path) -> tuple[PacketManifest | None, list[str]]:
    """Validate the JSON schema once before packet checks consume it."""
    if not isinstance(raw, dict):
        return None, ["manifest must be a JSON object"]
    publisher = raw.get("publisher")
    if publisher not in PUBLISHERS:
        return None, [f"publisher must be one of {' or '.join(PUBLISHERS)}"]

    errors: list[str] = []
    allowed = COMMON_KEYS | PUBLISHER_KEYS[publisher]
    unknown = sorted(set(raw) - allowed)
    if unknown:
        # A silently ignored key is how a misspelled field, or a field copied from
        # the other publisher, turns into a green packet that is missing the file
        # it claimed to declare.
        errors.append(f"unknown manifest key(s) for {publisher}: {', '.join(unknown)}")

    def required_string(key: str) -> str:
        value = raw.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{key} must be a non-empty string")
            return ""
        return value.strip()

    def optional_path(key: str) -> str | None:
        value = raw.get(key)
        if value is None:
            return None
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{key} must be a non-empty path when present")
            return None
        return value.strip()

    submission_step = required_string("submission_step")
    submission_step_checked_on = required_string("submission_step_checked_on")
    journal_guide_url = required_string("journal_guide_url")
    journal_limits_checked_on = required_string("journal_limits_checked_on")
    manuscript_value = required_string("manuscript")

    side_values = raw.get("side_materials")
    if not isinstance(side_values, list) or not all(
        isinstance(item, str) and item.strip() for item in side_values
    ):
        errors.append("side_materials must be a JSON array of paths")
        side_values = []
    if publisher == "elsevier" and not side_values:
        errors.append("side_materials must be a non-empty JSON array for an Elsevier packet")

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

    source_required = raw.get("source_required")
    if not isinstance(source_required, bool):
        errors.append("source_required must be true or false")
        source_required = False
    step = submission_step.lower()
    if ("source" in step or "final" in step) and not source_required:
        errors.append("a source/final-files step cannot set source_required to false")
    source_zip_value = raw.get("source_zip")
    if source_required and (not isinstance(source_zip_value, str) or not source_zip_value.strip()):
        errors.append("source_zip must be a non-empty path when source_required is true")
    source_entrypoint = raw.get("source_entrypoint", "main.tex")
    if not isinstance(source_entrypoint, str) or not source_entrypoint.strip():
        errors.append("source_entrypoint must be a non-empty path")
        source_entrypoint = "main.tex"

    raw_limits = raw.get("journal_limits")
    if not isinstance(raw_limits, dict):
        errors.append("journal_limits must be a JSON object with checked numeric limits")
        raw_limits = {}
    unknown_limits = sorted(set(raw_limits) - (COMMON_LIMIT_KEYS | PUBLISHER_LIMIT_KEYS[publisher]))
    if unknown_limits:
        errors.append(f"unknown journal_limits key(s) for {publisher}: {', '.join(unknown_limits)}")
    abstract_max_words = parse_positive_int(
        raw_limits.get("abstract_max_words"), "journal_limits.abstract_max_words", errors
    )

    # Publisher-specific fields. Elsevier packets carry highlights and a marked
    # manuscript; IEEE packets carry EDICS, an upload PDF judged by page count,
    # supplemental material, and a conference-extension difference statement.
    marked_value: str | None = None
    manuscript_pdf_value = ""
    edics_values: list[str] = []
    supplemental_value: str | None = None
    difference_value: str | None = None
    limits = JournalLimits(abstract_max_words=abstract_max_words or 1)

    if publisher == "elsevier":
        marked_value = optional_path("marked_manuscript")
        highlight_values: list[int | None] = [None, None, None]
        if any("highlight" in Path(item).stem.lower() for item in side_values):
            highlight_values = [
                parse_positive_int(raw_limits.get(key), f"journal_limits.{key}", errors)
                for key in (
                    "highlights_min_items",
                    "highlights_max_items",
                    "highlight_max_characters",
                )
            ]
            minimum, maximum, _ = highlight_values
            if minimum is not None and maximum is not None and minimum > maximum:
                errors.append(
                    "journal_limits highlights_min_items cannot exceed highlights_max_items"
                )
        limits = JournalLimits(
            abstract_max_words=abstract_max_words or 1,
            highlights_min_items=highlight_values[0],
            highlights_max_items=highlight_values[1],
            highlight_max_characters=highlight_values[2],
        )
    elif publisher == "ieee":
        manuscript_pdf_value = required_string("manuscript_pdf")
        edics_raw = raw.get("edics")
        if (
            not isinstance(edics_raw, list)
            or not edics_raw
            or not all(isinstance(item, str) and item.strip() for item in edics_raw)
        ):
            errors.append("edics must be a non-empty JSON array of category strings")
        else:
            edics_values = [item.strip() for item in edics_raw]
        supplemental_value = optional_path("supplemental_pdf")
        difference_value = optional_path("difference_statement")
        abstract_min_words = parse_positive_int(
            raw_limits.get("abstract_min_words"), "journal_limits.abstract_min_words", errors
        )
        if (
            abstract_min_words is not None
            and abstract_max_words is not None
            and abstract_min_words > abstract_max_words
        ):
            errors.append("journal_limits abstract_min_words cannot exceed abstract_max_words")
        max_pages = parse_positive_int(
            raw_limits.get("max_pages"), "journal_limits.max_pages", errors
        )
        supplemental_max_pages = None
        if supplemental_value is not None:
            supplemental_max_pages = parse_positive_int(
                raw_limits.get("supplemental_max_pages"),
                "journal_limits.supplemental_max_pages",
                errors,
            )
        limits = JournalLimits(
            abstract_max_words=abstract_max_words or 1,
            abstract_min_words=abstract_min_words,
            max_pages=max_pages,
            supplemental_max_pages=supplemental_max_pages,
        )

    if errors:
        return None, errors
    return PacketManifest(
        publisher=publisher,
        submission_step=submission_step,
        submission_step_checked_on=submission_step_checked_on,
        journal_guide_url=journal_guide_url,
        journal_limits_checked_on=journal_limits_checked_on,
        limits=limits,
        manuscript=resolve(base, manuscript_value),
        side_materials=tuple(resolve(base, item) for item in side_values),
        submission_stage=submission_stage,
        response_to_reviewers=(
            resolve(base, response_value) if isinstance(response_value, str) else None
        ),
        source_required=source_required,
        source_zip=resolve(base, source_zip_value) if isinstance(source_zip_value, str) else None,
        source_entrypoint=source_entrypoint,
        marked_manuscript=resolve(base, marked_value) if marked_value else None,
        manuscript_pdf=resolve(base, manuscript_pdf_value) if manuscript_pdf_value else None,
        edics=tuple(edics_values),
        supplemental_pdf=resolve(base, supplemental_value) if supplemental_value else None,
        difference_statement=resolve(base, difference_value) if difference_value else None,
    ), []


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
    """Require live journal and current submission-step evidence to be recent."""
    errors: list[str] = []
    parsed = urlparse(manifest.journal_guide_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        errors.append("journal_guide_url must identify the live journal guide")
    errors.extend(
        check_recent_date(
            "journal_limits_checked_on", manifest.journal_limits_checked_on, max_age_days
        )
    )
    errors.extend(
        check_recent_date(
            "submission_step_checked_on", manifest.submission_step_checked_on, max_age_days
        )
    )
    return errors


def check_revision(manifest: PacketManifest) -> list[str]:
    """Require a revision packet to ship the files that answer the reviewers.

    Both the point-by-point response and the clean/marked distinction are declared
    as manifest paths, so both are checkable here — declaring a path that does not
    exist must not pass.
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

    # The editable-source slot rejects PDF: production typesets from these files.
    # A built PDF dropped into that slot stalls the revision before review, and the
    # mistake is easy to make because the same PDF is correct for the marked slot.
    if manifest.source_required and manifest.source_zip is not None:
        if manifest.source_zip.suffix.lower() == ".pdf":
            errors.append(
                f"source archive must be editable source, not a PDF: {manifest.source_zip}"
            )
        elif manifest.source_zip.suffix.lower() == ".zip" and manifest.source_zip.is_file():
            errors.extend(check_em_archive(manifest.source_zip))
    return errors


def check_em_archive(archive: Path) -> list[str]:
    """Enforce the constraints Editorial Manager's own LaTeX build imposes.

    EM compiles the archive itself and fails on structures a local latexmk
    accepts: subfolders are not processed at all, multi-period filenames are
    excluded, and a LaTeX submission is expected to carry its .bib (with .bbl,
    .cls, and .bst riding along so nothing resolves against the build host).
    """
    import zipfile

    errors: list[str] = []
    with zipfile.ZipFile(archive) as bundle:
        names = [n for n in bundle.namelist() if not n.endswith("/")]
    nested = sorted({n.split("/")[0] + "/" for n in names if "/" in n})
    if nested:
        errors.append(
            f"EM cannot process subfolders in a LaTeX archive; found {', '.join(nested)} "
            f"in {archive.name} — flatten to one level and strip path prefixes from "
            "\\input/\\includegraphics/\\bibliography"
        )
    multi_period = [n for n in names if Path(n).name.count(".") != 1]
    if multi_period:
        errors.append(
            f"EM excludes filenames with more than one period: {multi_period[:5]}"
        )
    flat = [Path(n).name for n in names]
    if any(n.endswith(".tex") for n in flat) and not any(n.endswith(".bib") for n in flat):
        errors.append(f"LaTeX archive {archive.name} carries no .bib file")
    return errors


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


def check_abstract(text: str, limits: JournalLimits) -> list[str]:
    """Enforce the recorded live abstract limit — a range when one was recorded."""
    match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.DOTALL)
    if not match:
        return ["manuscript lacks an abstract environment"]
    words = re.findall(r"\b[\w'-]+\b", re.sub(r"\\[A-Za-z]+", " ", match.group(1)))
    count = len(words)
    minimum = limits.abstract_min_words
    if minimum is not None:
        if not minimum <= count <= limits.abstract_max_words:
            return [
                f"abstract has {count} words; live journal range is "
                f"{minimum}-{limits.abstract_max_words}"
            ]
    elif count > limits.abstract_max_words:
        return [f"abstract has {count} words; live journal maximum is {limits.abstract_max_words}"]
    return []


def read_docx_paragraphs(path: Path) -> tuple[list[str] | None, list[str]]:
    """Validate core OOXML parts and extract Word paragraph text."""
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
        return None, [
            f"side material lacks a valid Word document content type or relationship: {path}"
        ]
    paragraphs = []
    for paragraph in root.findall(".//w:p", WORD_NS):
        text = "".join(node.text or "" for node in paragraph.findall(".//w:t", WORD_NS)).strip()
        if text:
            paragraphs.append(text)
    if not paragraphs:
        return None, [f"side material contains no readable paragraphs: {path}"]
    return paragraphs, []


def check_highlight_limits(paragraphs: list[str], limits: JournalLimits) -> list[str]:
    """Enforce the recorded highlights item count and character limit."""
    items = paragraphs[1:] if paragraphs[0].strip().lower() == "highlights" else paragraphs
    minimum = limits.highlights_min_items or 1
    maximum = limits.highlights_max_items or minimum
    errors: list[str] = []
    if not minimum <= len(items) <= maximum:
        errors.append(f"highlights item count is {len(items)}; expected {minimum}-{maximum}")
    max_chars = limits.highlight_max_characters or 1
    for index, item in enumerate(items, start=1):
        if len(item) > max_chars:
            errors.append(f"highlight {index} has {len(item)} characters; maximum is {max_chars}")
    return errors


def check_side_materials(manifest: PacketManifest) -> list[str]:
    """Verify declared side materials exist and DOCX files are real documents."""
    errors: list[str] = []
    for path in manifest.side_materials:
        if not path.is_file():
            errors.append(f"side material does not exist: {path}")
            continue
        if path.suffix.lower() != ".docx":
            continue
        paragraphs, docx_errors = read_docx_paragraphs(path)
        errors.extend(docx_errors)
        if (
            paragraphs
            and manifest.publisher == "elsevier"
            and "highlight" in path.stem.lower()
        ):
            errors.extend(check_highlight_limits(paragraphs, manifest.limits))
    return errors


def count_pdf_pages(path: Path) -> tuple[int | None, list[str], bool]:
    """Count PDF pages with pdfinfo; block instead of guessing without it."""
    if path.suffix.lower() != ".pdf" or not path.is_file():
        return None, [f"PDF does not exist: {path}"], False
    pdfinfo = shutil.which("pdfinfo")
    if not pdfinfo:
        return None, [
            "page-count check is blocked: install poppler-utils (pdfinfo), then rerun "
            "the packet check"
        ], True
    result = subprocess.run([pdfinfo, str(path)], capture_output=True, text=True, check=False)
    match = re.search(r"^Pages:\s+(\d+)$", result.stdout, re.MULTILINE)
    if result.returncode != 0 or not match:
        return None, [f"pdfinfo could not read the PDF: {path}"], False
    return int(match.group(1)), [], False


def check_page_limits(manifest: PacketManifest) -> tuple[list[str], bool]:
    """Enforce recorded page limits on the upload PDF and any supplemental PDF."""
    errors: list[str] = []
    blocked = False
    if manifest.manuscript_pdf is None or manifest.limits.max_pages is None:
        return errors, blocked
    pages, page_errors, page_blocked = count_pdf_pages(manifest.manuscript_pdf)
    errors.extend(page_errors)
    blocked = blocked or page_blocked
    if pages is not None and pages > manifest.limits.max_pages:
        errors.append(
            f"manuscript PDF has {pages} pages; live journal maximum is {manifest.limits.max_pages}"
        )
    if manifest.supplemental_pdf is not None:
        pages, page_errors, page_blocked = count_pdf_pages(manifest.supplemental_pdf)
        errors.extend(page_errors)
        blocked = blocked or page_blocked
        maximum = manifest.limits.supplemental_max_pages
        if pages is not None and maximum is not None and pages > maximum:
            errors.append(f"supplemental PDF has {pages} pages; live journal maximum is {maximum}")
    return errors, blocked


def check_difference_statement(manifest: PacketManifest) -> list[str]:
    """Require a declared conference-extension difference statement to exist."""
    statement = manifest.difference_statement
    if statement is not None and not statement.is_file():
        return [f"difference_statement is missing: {statement}"]
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
        with tempfile.TemporaryDirectory(prefix="journal-packet-") as tmp:
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
    parser = argparse.ArgumentParser(description="Check a journal submission packet manifest")
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
        errors.extend(check_abstract(text, manifest.limits))
        if manifest.publisher == "elsevier":
            errors.extend(check_statements(text))
    errors.extend(check_side_materials(manifest))

    blocked = False
    if manifest.publisher == "ieee":
        page_errors, blocked = check_page_limits(manifest)
        errors.extend(page_errors)
        errors.extend(check_difference_statement(manifest))
    if manifest.source_required:
        source_errors, source_blocked = check_source_zip(
            manifest.source_zip or base,
            manifest.source_entrypoint,
        )
        errors.extend(source_errors)
        blocked = blocked or source_blocked
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 2 if blocked and len(errors) == 1 else 1
    print(f"{manifest.publisher} packet check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
