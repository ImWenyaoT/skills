"""Count the figures/tables in the experiments section of reference papers.

Usage:
    python reference_fig_table_stats.py \\
        --corpus <PDF root directory> \\
        --text-root <pdftotext text directory> \\
        --out <output CSV path>
"""

from __future__ import annotations

import argparse
import csv
import re
import statistics
import subprocess
from dataclasses import dataclass
from pathlib import Path

# Filename regex that excludes review/benchmark papers
EXCLUDE_NAME_PATTERN = re.compile(
    r"(review|survey|benchmark|revisiting|comprehensive_review|experimental_comparison|dynamic_rgbt_tracking)",
    re.IGNORECASE,
)
# Experiments-section heading match (numbered form)
EXPERIMENT_HEADING_PATTERN = re.compile(
    r"^\s*(?:[0-9]+(?:\.[0-9]+)*|[IVX]+)\.?\s+"
    r"(?:Experiments?|Experimental\s+(?:Results?|Evaluation|Setup)|Evaluation|Results\s+and\s+Discussion)\b",
    re.IGNORECASE,
)
# Experiments-section heading fallback match (unnumbered form)
EXPERIMENT_FALLBACK_PATTERN = re.compile(
    r"^\s*(?:Experiments?|EXPERIMENTS|Experimental\s+Results|"
    r"[A-Z]\.\s+(?:Datasets?\s+and\s+Evaluation|Evaluation\s+Dataset|Experimental\s+Settings|"
    r"Experiment\s+Settings|Dataset\s+and\s+Metrics))\b",
    re.IGNORECASE,
)
# Conclusion-section heading match (numbered form)
CONCLUSION_HEADING_PATTERN = re.compile(
    r"^\s*(?:[0-9]+(?:\.[0-9]+)*|[IVX]+)\.?\s+(?:Conclusion|Conclusions)\b",
    re.IGNORECASE,
)
# Conclusion-section heading fallback match (unnumbered form)
CONCLUSION_FALLBACK_PATTERN = re.compile(
    r"^\s*(?:Conclusion|CONCLUSION|Conclusions|CONCLUSIONS)\s*$"
)
# Figure-caption line match
FIGURE_CAPTION_PATTERN = re.compile(r"^\s*(?:Fig\.|Figure)\s*([0-9]+)\b", re.IGNORECASE)
# Table-caption line match
TABLE_CAPTION_PATTERN = re.compile(r"^\s*(?:Table|Tab\.)\s*([0-9]+|[IVXLCDM]+)\b", re.IGNORECASE)


@dataclass(frozen=True)
class PaperCount:
    """Holds the figure/table counts for one reference paper's experiments section."""

    pdf: str
    year: str
    venue: str
    figure_count: int
    table_count: int
    total_count: int
    figures: str
    tables: str
    section_start_line: int
    section_end_line: int


def parse_args() -> argparse.Namespace:
    """CLI: the PDF corpus, the extracted-text directory, and the output CSV path are all \
required."""
    p = argparse.ArgumentParser(
        description="Survey of figure/table counts in reference-paper experiments sections"
    )
    p.add_argument("--corpus", type=Path, required=True, help="reference-paper PDF root directory")
    p.add_argument(
        "--text-root",
        dest="text_root",
        type=Path,
        required=True,
        help="directory of pdftotext output",
    )
    p.add_argument("--out", type=Path, required=True, help="output CSV path")
    return p.parse_args()


def normalize_line(line: str) -> str:
    """Collapse the redundant whitespace in a PDF-extracted line into single spaces."""
    return re.sub(r"\s+", " ", line).strip()


def parse_year_and_venue(pdf_path: Path) -> tuple[str, str]:
    """Pull the year and the venue identifier out of a reference's filename."""
    parts = pdf_path.stem.split("_")
    year = parts[0] if parts and re.fullmatch(r"\d{4}", parts[0]) else ""
    venue = parts[1] if len(parts) > 1 else ""
    return year, venue


def find_experiment_slice(lines: list[str]) -> tuple[int, int]:
    """Locate the start and end line numbers of the experiments section in a list of PDF text lines.

    Tries the numbered heading form first, and falls back to the unnumbered form when that misses.
    Returns the (start, end) line indices; (-1, -1) when no experiments section is found.
    """
    normalized = [normalize_line(line) for line in lines]
    start = -1
    for index, line in enumerate(normalized):
        if EXPERIMENT_HEADING_PATTERN.match(line):
            start = index
            break
    if start < 0:
        for index, line in enumerate(normalized):
            if EXPERIMENT_FALLBACK_PATTERN.match(line):
                start = index
                break
    if start < 0:
        return -1, -1

    end = len(lines)
    for index in range(start + 1, len(normalized)):
        if CONCLUSION_HEADING_PATTERN.match(normalized[index]) or CONCLUSION_FALLBACK_PATTERN.match(
            normalized[index]
        ):
            end = index
            break
    return start, end


def collect_unique_captions(lines: list[str], pattern: re.Pattern[str]) -> set[str]:
    """Collect the unique figure/table number identifiers from a set of text lines."""
    identifiers: set[str] = set()
    for raw_line in lines:
        line = normalize_line(raw_line)
        match = pattern.match(line)
        if match:
            identifiers.add(match.group(1).upper())
    return identifiers


def count_experiment_floats(lines: list[str]) -> dict[str, int]:
    """Count the figures and tables inside the experiments section of a list of text lines \
(pure function).

    Locate the experiments heading → count the unique Fig./Table. references within that span.
    Returns {"figures": n, "tables": m}; both are 0 when no experiments section is found.
    """
    start, end = find_experiment_slice(lines)
    if start < 0:
        return {"figures": 0, "tables": 0}
    section_lines = lines[start:end]
    figure_ids = collect_unique_captions(section_lines, FIGURE_CAPTION_PATTERN)
    table_ids = collect_unique_captions(section_lines, TABLE_CAPTION_PATTERN)
    return {"figures": len(figure_ids), "tables": len(table_ids)}


def pdf_text_path(pdf_path: Path, text_root: Path) -> Path:
    """Return the text-cache path that corresponds to a given PDF."""
    return text_root / f"{pdf_path.stem}.txt"


def ensure_pdf_text(pdf_path: Path, text_root: Path) -> Path:
    """Create or reuse the pdftotext cache for a single PDF."""
    text_root.mkdir(parents=True, exist_ok=True)
    text_path = pdf_text_path(pdf_path, text_root)
    if not text_path.exists():
        subprocess.run(["pdftotext", str(pdf_path), str(text_path)], check=True)
    return text_path


def list_method_reference_pdfs(corpus: Path) -> list[Path]:
    """List the journal reference PDFs under the corpus directory, minus the \
review/benchmark ones."""
    pdfs = sorted(corpus.glob("**/*.pdf"))
    return [pdf for pdf in pdfs if not EXCLUDE_NAME_PATTERN.search(pdf.stem)]


def count_one_pdf(pdf_path: Path, corpus: Path, text_root: Path) -> PaperCount | None:
    """Count the figures/tables in one reference PDF's experiments section; returns None \
on failure."""
    text_path = ensure_pdf_text(pdf_path, text_root)
    lines = text_path.read_text(encoding="utf-8", errors="replace").splitlines()
    start, end = find_experiment_slice(lines)
    if start < 0:
        return None

    section_lines = lines[start:end]
    figure_ids = collect_unique_captions(section_lines, FIGURE_CAPTION_PATTERN)
    table_ids = collect_unique_captions(section_lines, TABLE_CAPTION_PATTERN)
    year, venue = parse_year_and_venue(pdf_path)
    return PaperCount(
        pdf=str(pdf_path.relative_to(corpus)),
        year=year,
        venue=venue,
        figure_count=len(figure_ids),
        table_count=len(table_ids),
        total_count=len(figure_ids) + len(table_ids),
        figures=";".join(
            sorted(figure_ids, key=lambda item: int(item) if item.isdigit() else item)
        ),
        tables=";".join(sorted(table_ids)),
        section_start_line=start + 1,
        section_end_line=end,
    )


def percentile(values: list[float], q: float) -> float:
    """Compute a linearly interpolated percentile over a list of numbers."""
    if not values:
        raise ValueError("percentile requires at least one value")
    sorted_values = sorted(values)
    position = (len(sorted_values) - 1) * q
    lower = int(position)
    upper = min(lower + 1, len(sorted_values) - 1)
    weight = position - lower
    return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight


def summarize(values: list[int]) -> tuple[float, float, float, float]:
    """Return the mean, Q1, Q3, and IQR of a list of integers."""
    numeric = [float(value) for value in values]
    q1 = percentile(numeric, 0.25)
    q3 = percentile(numeric, 0.75)
    return statistics.mean(numeric), q1, q3, q3 - q1


def write_counts(counts: list[PaperCount], out: Path) -> None:
    """Write the per-paper counts to a CSV file."""
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(PaperCount.__dataclass_fields__))
        writer.writeheader()
        for row in counts:
            writer.writerow(row.__dict__)


def main() -> None:
    """Run the reference-paper figure/table counting workflow and print the summary statistics."""
    args = parse_args()

    counts: list[PaperCount] = []
    skipped: list[str] = []
    for pdf_path in list_method_reference_pdfs(args.corpus):
        count = count_one_pdf(pdf_path, args.corpus, args.text_root)
        if count is None:
            skipped.append(str(pdf_path.relative_to(args.corpus)))
        else:
            counts.append(count)

    write_counts(counts, args.out)
    print(f"counted_papers={len(counts)}")
    print(f"skipped_no_experiment_heading={len(skipped)}")
    if skipped:
        for item in skipped:
            print(f"skipped: {item}")

    for label, values in [
        ("figures", [row.figure_count for row in counts]),
        ("tables", [row.table_count for row in counts]),
        ("figures_plus_tables", [row.total_count for row in counts]),
    ]:
        mean, q1, q3, iqr = summarize(values)
        print(f"{label}: mean={mean:.2f}, q1={q1:.2f}, q3={q3:.2f}, iqr={iqr:.2f}")
    print(f"wrote={args.out}")


if __name__ == "__main__":
    main()
