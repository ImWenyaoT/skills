#!/usr/bin/env python3
"""Extract per-section word counts from a corpus of reference papers, giving robust target \
ranges for writing.

Word counts are right-skewed, so the median is the anchor and the IQR (Q1-Q3) is the target range,
with mean/std/trimmed-mean attached for reference. Each section's extraction coverage
(null rate) is reported too, so statistics from a poorly covered section cannot pass themselves
off as a reliable conclusion.

Example usage:
    python section_wordcount.py \\
        --corpus /path/to/pdfs \\
        --out /path/to/output \\
        --prefix myproject_
"""

from __future__ import annotations

import argparse
import csv
import re
import statistics as st
import subprocess
from pathlib import Path

# Default exclusion regex: review/survey/benchmark and other non-method papers
DEFAULT_EXCLUDE = r"Comprehensive_Review|Survey|UniRTL|Adversarial"

# canonical section bucket -> heading keywords (matched in priority order;
# the first bucket to hit wins)
SECTION_KEYWORDS = [
    ("introduction", [r"introduction"]),
    ("related", [r"related\s+work", r"^background"]),
    (
        "method",
        [
            r"method",
            r"methodology",
            r"proposed",
            r"approach",
            r"\bour\b",
            r"framework",
            r"\bnetwork\b",
            r"architecture",
        ],
    ),
    ("experiments", [r"experiment", r"experimental", r"result", r"evaluation"]),
    ("conclusion", [r"conclusion", r"concluding"]),
]
# Marks the end of the body (nothing after references/acknowledgments counts)
END_KEYWORDS = re.compile(
    r"^(references|acknowledg|declaration|appendix|"
    r"data\s+availability|supplementary)",
    re.I,
)
SECTIONS = ["abstract", "introduction", "related", "method", "experiments", "conclusion"]


def summarize(counts):
    """Compute a robust distribution over a set of word counts: median anchor + IQR range \
(word counts are right-skewed).

    counts: list[int], one section's word counts across papers.
    Returns dict(median/q1/q3/mean/std/n); when n<2, q1/q3 collapse onto the median.
    """
    n = len(counts)
    if n == 0:
        return {"median": None, "q1": None, "q3": None, "mean": None, "std": None, "n": 0}
    s = sorted(counts)
    median = st.median(s)
    if n >= 2:
        q1, q3 = st.quantiles(s, n=4)[0], st.quantiles(s, n=4)[2]
    else:
        q1 = q3 = median
    std = st.pstdev(s) if n >= 2 else 0.0
    return {"median": median, "q1": q1, "q3": q3, "mean": st.fmean(s), "std": std, "n": n}


def parse_args():
    """CLI: corpus directory and output directory are required; exclusion regex and output \
prefix are optional."""
    p = argparse.ArgumentParser(
        description="Per-section word budget from reference papers (median+IQR)"
    )
    p.add_argument(
        "--corpus",
        type=Path,
        required=True,
        help="root directory of the reference-paper PDF corpus",
    )
    p.add_argument(
        "--out", type=Path, required=True, help="output directory for the statistics CSVs"
    )
    p.add_argument("--exclude", default=DEFAULT_EXCLUDE, help="filename exclusion regex")
    p.add_argument("--prefix", default="", help="output filename prefix (e.g. myproject_)")
    return p.parse_args()


def extract_text(pdf: Path) -> str:
    """Extract the full text with pdftotext -raw (it preserves two-column reading order \
better than the default mode)."""
    res = subprocess.run(
        ["pdftotext", "-raw", "-q", str(pdf), "-"],
        capture_output=True,
        text=True,
    )
    return res.stdout


def classify_heading(title: str) -> str | None:
    """Map a section heading's text onto a canonical bucket; returns None when nothing hits."""
    t = title.strip().lower()
    for bucket, pats in SECTION_KEYWORDS:
        if any(re.search(p, t) for p in pats):
            return bucket
    return None


def find_numbered_headings(lines: list[str]) -> list[tuple[int, int, str]]:
    """Find the top-level numbered section headings, returning [(line number, number N, \
canonical bucket)].

    Only short lines of the form 'N. Title' / 'N Title' are accepted (<=6 words, <50 \
characters), and
    the numbering must rise roughly monotonically from 1, which filters out body-text noise such as
    'Fig. 1', list items, and equation numbers.
    """
    cand: list[tuple[int, int, str]] = []
    pat = re.compile(r"^\s*(\d{1,2})\.?\s+([A-Za-z][A-Za-z0-9 \-&/,:]{2,48})\s*$")
    for i, ln in enumerate(lines):
        m = pat.match(ln)
        if not m:
            continue
        num = int(m.group(1))
        title = m.group(2)
        if len(title.split()) > 6:
            continue
        bucket = classify_heading(title)
        if bucket is None:
            continue
        cand.append((i, num, bucket))
    # keep only non-decreasing numbers and the first occurrence of each bucket,
    # filtering stray mismatches
    kept: list[tuple[int, int, str]] = []
    last_num = 0
    seen: set[str] = set()
    for i, num, bucket in cand:
        if num < last_num or num > last_num + 3:
            continue
        if bucket in seen:
            continue
        kept.append((i, num, bucket))
        seen.add(bucket)
        last_num = num
    return kept


def count_words(lines: list[str], a: int, b: int) -> int:
    """Count the English words in the line range [a, b) (skipping obvious short numeric \
header/footer lines)."""
    words = 0
    for ln in lines[a:b]:
        s = ln.strip()
        if not s:
            continue
        if re.fullmatch(r"[\d ./\-]+", s):  # bare page numbers / header digits
            continue
        words += len(re.findall(r"[A-Za-z][A-Za-z\-']+", ln))
    return words


def section_counts(text: str) -> dict[str, int | None]:
    """For one paper's full text, return the word count of each canonical section (None \
where it cannot be recovered)."""
    lines = text.splitlines()
    out: dict[str, int | None] = {s: None for s in SECTIONS}
    headings = find_numbered_headings(lines)
    head_line = {b: i for i, n, b in headings}

    # abstract: from the 'abstract' line (within the first 40% of the text) up to 'keywords'/intro
    n = len(lines)
    abs_start = None
    for i in range(min(n, int(n * 0.4))):
        if re.match(r"^\s*(abstract|a b s t r a c t)\b", lines[i], re.I):
            abs_start = i + 1
            break
    if abs_start is not None:
        abs_end = n
        for i in range(abs_start, min(n, abs_start + 80)):
            if re.match(r"^\s*(keywords|key words|index terms)\b", lines[i], re.I):
                abs_end = i
                break
            if "introduction" in head_line and i >= head_line["introduction"]:
                abs_end = head_line["introduction"]
                break
        out["abstract"] = count_words(lines, abs_start, abs_end)

    # numbered sections: each bucket runs from its heading line to the next section
    # heading / end of body
    order = sorted([(i, b) for i, num, b in headings])
    # find the end of the body: references/acknowledgment and friends appearing after the conclusion
    end_idx = n
    concl_line = head_line.get("conclusion")
    for i in range(concl_line if concl_line else 0, n):
        if END_KEYWORDS.match(lines[i].strip()):
            end_idx = i
            break
    for k, (start_line, bucket) in enumerate(order):
        nxt = order[k + 1][0] if k + 1 < len(order) else end_idx
        out[bucket] = count_words(lines, start_line + 1, nxt)
    return out


def robust_stats(vals: list[int]) -> dict[str, float]:
    """Compute robust statistics over a set of word counts: N/mean/std/median/Q1/Q3/IQR/10% \
trimmed mean."""
    vals = sorted(vals)
    k = len(vals)
    q = st.quantiles(vals, n=4) if k >= 2 else [vals[0], vals[0], vals[0]]
    trim = max(1, int(k * 0.1))
    core = vals[trim : k - trim] if k - 2 * trim >= 1 else vals
    return {
        "N": k,
        "mean": round(st.mean(vals)),
        "std": round(st.pstdev(vals)) if k > 1 else 0,
        "median": round(st.median(vals)),
        "Q1": round(q[0]),
        "Q3": round(q[2]),
        "IQR_lo": round(q[0]),
        "IQR_hi": round(q[2]),
        "trimmed_mean": round(st.mean(core)),
    }


def main() -> None:
    """Main flow: read the command-line arguments, extract each paper's per-section word \
counts -> write the per-paper CSV -> compute and write the per-section statistics CSV."""
    args = parse_args()
    exclude_pat = re.compile(args.exclude, re.I)

    args.out.mkdir(parents=True, exist_ok=True)
    pdfs = sorted(p for p in args.corpus.rglob("*.pdf") if not exclude_pat.search(p.name))
    rows: list[dict] = []
    for p in pdfs:
        counts = section_counts(extract_text(p))
        rows.append({"paper": p.name, **counts})

    # per-paper CSV
    with (args.out / f"{args.prefix}section_wordcounts.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["paper", *SECTIONS])
        w.writeheader()
        w.writerows(rows)

    # per-section statistics + coverage
    total = len(rows)
    summ: list[dict] = []
    for s in SECTIONS:
        vals = [r[s] for r in rows if isinstance(r[s], int) and r[s] > 30]
        cov = len(vals)
        stats = robust_stats(vals) if cov >= 3 else {"N": cov}
        summ.append({"section": s, "coverage": f"{cov}/{total}", **stats})

    with (args.out / f"{args.prefix}section_wordcount_summary.csv").open("w", newline="") as f:
        cols = ["section", "coverage", "N", "median", "Q1", "Q3", "mean", "std", "trimmed_mean"]
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(summ)

    # console output
    print(f"corpus: {total} method papers (excluded: {args.exclude})\n")
    print(
        f"{'section':<13}{'cover':<8}{'median':>8}{'IQR(Q1-Q3)':>16}"
        f"{'mean':>8}{'std':>7}{'trim_mean':>11}"
    )
    for d in summ:
        if "median" in d:
            print(
                f"{d['section']:<13}{d['coverage']:<8}{d['median']:>8}"
                f"{str(d['Q1']) + '-' + str(d['Q3']):>16}{d['mean']:>8}"
                f"{d['std']:>7}{d['trimmed_mean']:>11}"
            )
        else:
            print(f"{d['section']:<13}{d['coverage']:<8}  (coverage too low, statistics skipped)")


if __name__ == "__main__":
    main()
