"""统计参考论文实验章节中的图/表数量。

用法:
    python reference_fig_table_stats.py \\
        --corpus <PDF根目录> \\
        --text-root <pdftotext文本目录> \\
        --out <输出CSV路径>
"""

from __future__ import annotations

import argparse
import csv
import re
import statistics
import subprocess
from dataclasses import dataclass
from pathlib import Path


# 排除综述/基准类论文的文件名正则
EXCLUDE_NAME_PATTERN = re.compile(
    r"(review|survey|benchmark|revisiting|comprehensive_review|experimental_comparison|dynamic_rgbt_tracking)",
    re.IGNORECASE,
)
# 实验章节标题匹配(带编号形式)
EXPERIMENT_HEADING_PATTERN = re.compile(
    r"^\s*(?:[0-9]+(?:\.[0-9]+)*|[IVX]+)\.?\s+"
    r"(?:Experiments?|Experimental\s+(?:Results?|Evaluation|Setup)|Evaluation|Results\s+and\s+Discussion)\b",
    re.IGNORECASE,
)
# 实验章节标题回退匹配(无编号形式)
EXPERIMENT_FALLBACK_PATTERN = re.compile(
    r"^\s*(?:Experiments?|EXPERIMENTS|Experimental\s+Results|"
    r"[A-Z]\.\s+(?:Datasets?\s+and\s+Evaluation|Evaluation\s+Dataset|Experimental\s+Settings|"
    r"Experiment\s+Settings|Dataset\s+and\s+Metrics))\b",
    re.IGNORECASE,
)
# 结论章节标题匹配(带编号形式)
CONCLUSION_HEADING_PATTERN = re.compile(
    r"^\s*(?:[0-9]+(?:\.[0-9]+)*|[IVX]+)\.?\s+(?:Conclusion|Conclusions)\b",
    re.IGNORECASE,
)
# 结论章节标题回退匹配(无编号形式)
CONCLUSION_FALLBACK_PATTERN = re.compile(r"^\s*(?:Conclusion|CONCLUSION|Conclusions|CONCLUSIONS)\s*$")
# 图题行匹配
FIGURE_CAPTION_PATTERN = re.compile(r"^\s*(?:Fig\.|Figure)\s*([0-9]+)\b", re.IGNORECASE)
# 表题行匹配
TABLE_CAPTION_PATTERN = re.compile(r"^\s*(?:Table|Tab\.)\s*([0-9]+|[IVXLCDM]+)\b", re.IGNORECASE)


@dataclass(frozen=True)
class PaperCount:
    """存储单篇参考论文实验章节的图/表数量信息。"""

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
    """命令行:PDF 语料、已抽取文本目录、输出 CSV 路径全部必填。"""
    p = argparse.ArgumentParser(description="参考论文实验章节图/表数量普查")
    p.add_argument("--corpus", type=Path, required=True, help="参考论文 PDF 根目录")
    p.add_argument("--text-root", dest="text_root", type=Path, required=True, help="已 pdftotext 的文本目录")
    p.add_argument("--out", type=Path, required=True, help="输出 CSV 路径")
    return p.parse_args()


def normalize_line(line: str) -> str:
    """将 PDF 提取行中的多余空白折叠为单个空格。"""
    return re.sub(r"\s+", " ", line).strip()


def parse_year_and_venue(pdf_path: Path) -> tuple[str, str]:
    """从参考文献文件名中提取年份和会议/期刊标识。"""
    parts = pdf_path.stem.split("_")
    year = parts[0] if parts and re.fullmatch(r"\d{4}", parts[0]) else ""
    venue = parts[1] if len(parts) > 1 else ""
    return year, venue


def find_experiment_slice(lines: list[str]) -> tuple[int, int]:
    """在 PDF 文本行列表中定位实验章节的起止行号。

    先按带编号标题匹配，找不到则回退到无编号形式。
    返回 (start, end) 行索引；若未找到实验段则返回 (-1, -1)。
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
        if CONCLUSION_HEADING_PATTERN.match(normalized[index]) or CONCLUSION_FALLBACK_PATTERN.match(normalized[index]):
            end = index
            break
    return start, end


def collect_unique_captions(lines: list[str], pattern: re.Pattern[str]) -> set[str]:
    """从文本行中收集唯一的图/表编号标识符。"""
    identifiers: set[str] = set()
    for raw_line in lines:
        line = normalize_line(raw_line)
        match = pattern.match(line)
        if match:
            identifiers.add(match.group(1).upper())
    return identifiers


def count_experiment_floats(lines: list[str]) -> dict[str, int]:
    """统计文本行列表中实验章节内的图和表数量(纯函数)。

    定位实验章节 heading → 在该段内计数唯一的 Fig./Table. 引用。
    返回 {"figures": n, "tables": m}；若找不到实验段则两项均为 0。
    """
    start, end = find_experiment_slice(lines)
    if start < 0:
        return {"figures": 0, "tables": 0}
    section_lines = lines[start:end]
    figure_ids = collect_unique_captions(section_lines, FIGURE_CAPTION_PATTERN)
    table_ids = collect_unique_captions(section_lines, TABLE_CAPTION_PATTERN)
    return {"figures": len(figure_ids), "tables": len(table_ids)}


def pdf_text_path(pdf_path: Path, text_root: Path) -> Path:
    """返回指定 PDF 对应的文本缓存路径。"""
    return text_root / f"{pdf_path.stem}.txt"


def ensure_pdf_text(pdf_path: Path, text_root: Path) -> Path:
    """为单个 PDF 创建或复用 pdftotext 缓存。"""
    text_root.mkdir(parents=True, exist_ok=True)
    text_path = pdf_text_path(pdf_path, text_root)
    if not text_path.exists():
        subprocess.run(["pdftotext", str(pdf_path), str(text_path)], check=True)
    return text_path


def list_method_reference_pdfs(corpus: Path) -> list[Path]:
    """列出 corpus 目录下排除综述/基准类后的期刊参考 PDF。"""
    pdfs = sorted(corpus.glob("**/*.pdf"))
    return [pdf for pdf in pdfs if not EXCLUDE_NAME_PATTERN.search(pdf.stem)]


def count_one_pdf(pdf_path: Path, corpus: Path, text_root: Path) -> PaperCount | None:
    """统计单篇参考 PDF 实验章节内的图/表数量，失败返回 None。"""
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
        figures=";".join(sorted(figure_ids, key=lambda item: int(item) if item.isdigit() else item)),
        tables=";".join(sorted(table_ids)),
        section_start_line=start + 1,
        section_end_line=end,
    )


def percentile(values: list[float], q: float) -> float:
    """对数值列表计算线性插值百分位数。"""
    if not values:
        raise ValueError("percentile requires at least one value")
    sorted_values = sorted(values)
    position = (len(sorted_values) - 1) * q
    lower = int(position)
    upper = min(lower + 1, len(sorted_values) - 1)
    weight = position - lower
    return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight


def summarize(values: list[int]) -> tuple[float, float, float, float]:
    """返回整数列表的均值、Q1、Q3 和 IQR。"""
    numeric = [float(value) for value in values]
    q1 = percentile(numeric, 0.25)
    q3 = percentile(numeric, 0.75)
    return statistics.mean(numeric), q1, q3, q3 - q1


def write_counts(counts: list[PaperCount], out: Path) -> None:
    """将逐篇计数写入 CSV 文件。"""
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(PaperCount.__dataclass_fields__))
        writer.writeheader()
        for row in counts:
            writer.writerow(row.__dict__)


def main() -> None:
    """执行参考论文图/表计数工作流并打印汇总统计。"""
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
