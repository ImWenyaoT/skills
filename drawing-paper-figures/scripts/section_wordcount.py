#!/usr/bin/env python3
"""从参考论文语料抽取各章节字数，给出稳健的写作目标区间。

word count 右偏，因此用中位数(median)做锚、IQR(Q1-Q3)做目标区间，
并附 mean/std/trimmed-mean 供参考，同时报告每个 section 的抽取覆盖率
(null 率)，避免用低覆盖 section 的统计冒充可靠结论。

用法示例:
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

# 默认排除正则：review/survey/benchmark 等非方法论文
DEFAULT_EXCLUDE = r"Comprehensive_Review|Survey|UniRTL|Adversarial"

# section 规范桶 -> 标题关键词（按优先级匹配；第一个命中的桶胜出）
SECTION_KEYWORDS = [
    ("introduction", [r"introduction"]),
    ("related", [r"related\s+work", r"^background"]),
    ("method", [r"method", r"methodology", r"proposed", r"approach",
                r"\bour\b", r"framework", r"\bnetwork\b", r"architecture"]),
    ("experiments", [r"experiment", r"experimental", r"result", r"evaluation"]),
    ("conclusion", [r"conclusion", r"concluding"]),
]
# 标记正文结束（参考文献/致谢之后不计入）
END_KEYWORDS = re.compile(r"^(references|acknowledg|declaration|appendix|"
                          r"data\s+availability|supplementary)", re.I)
SECTIONS = ["abstract", "introduction", "related", "method",
            "experiments", "conclusion"]


def summarize(counts):
    """对一组字数算稳健分布:中位数锚 + IQR 区间(word count 右偏)。

    counts: list[int] 某 section 跨论文的字数。
    返回 dict(median/q1/q3/mean/std/n);n<2 时 q1/q3 退化为 median。
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
    """命令行:语料目录与输出目录必填,排除正则与输出前缀可选。"""
    p = argparse.ArgumentParser(description="参考论文逐 section 字数预算(中位数+IQR)")
    p.add_argument("--corpus", type=Path, required=True, help="参考论文 PDF 语料根目录")
    p.add_argument("--out", type=Path, required=True, help="统计 CSV 输出目录")
    p.add_argument("--exclude", default=DEFAULT_EXCLUDE, help="文件名排除正则")
    p.add_argument("--prefix", default="", help="输出文件名前缀(如 myproject_)")
    return p.parse_args()


def extract_text(pdf: Path) -> str:
    """用 pdftotext -raw 抽全文(保留两栏阅读顺序优于默认模式)。"""
    res = subprocess.run(
        ["pdftotext", "-raw", "-q", str(pdf), "-"],
        capture_output=True, text=True,
    )
    return res.stdout


def classify_heading(title: str) -> str | None:
    """把一个 section 标题文字归到规范桶；命中不了返回 None。"""
    t = title.strip().lower()
    for bucket, pats in SECTION_KEYWORDS:
        if any(re.search(p, t) for p in pats):
            return bucket
    return None


def find_numbered_headings(lines: list[str]) -> list[tuple[int, int, str]]:
    """找顶层 numbered section 标题，返回 [(行号, 编号N, 规范桶)]。

    只接受形如 'N. Title' / 'N Title' 的短行(<=6 词, <50 字符)，且编号从 1
    起大致单调递增，以过滤正文里的 'Fig. 1'、列表项、公式编号等噪声。
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
    # 保留编号单调不降且去重桶首次出现，过滤偶发误匹配
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
    """统计 [a, b) 行区间的英文词数（跳过明显的页眉/页脚短数字行）。"""
    words = 0
    for ln in lines[a:b]:
        s = ln.strip()
        if not s:
            continue
        if re.fullmatch(r"[\d ./\-]+", s):  # 纯页码/页眉数字
            continue
        words += len(re.findall(r"[A-Za-z][A-Za-z\-']+", ln))
    return words


def section_counts(text: str) -> dict[str, int | None]:
    """对单篇全文，返回各规范 section 的词数（取不到为 None）。"""
    lines = text.splitlines()
    out: dict[str, int | None] = {s: None for s in SECTIONS}
    headings = find_numbered_headings(lines)
    head_line = {b: i for i, n, b in headings}

    # abstract: 'abstract' 行(前 40% 文本内) 到 'keywords'/intro 之间
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

    # numbered sections: 每个桶从它的标题行到下一个 section 标题/正文结束
    order = sorted([(i, b) for i, num, b in headings])
    # 找正文结束: conclusion 之后出现的 references/acknowledgment 等
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
    """给一组词数算稳健统计：N/mean/std/median/Q1/Q3/IQR/10%截尾均值。"""
    vals = sorted(vals)
    k = len(vals)
    q = st.quantiles(vals, n=4) if k >= 2 else [vals[0], vals[0], vals[0]]
    trim = max(1, int(k * 0.1))
    core = vals[trim:k - trim] if k - 2 * trim >= 1 else vals
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
    """主流程：读取命令行参数，抽取每篇各章字数 -> 写逐篇 CSV -> 算并写各章统计 CSV。"""
    args = parse_args()
    exclude_pat = re.compile(args.exclude, re.I)

    args.out.mkdir(parents=True, exist_ok=True)
    pdfs = sorted(p for p in args.corpus.rglob("*.pdf") if not exclude_pat.search(p.name))
    rows: list[dict] = []
    for p in pdfs:
        counts = section_counts(extract_text(p))
        rows.append({"paper": p.name, **counts})

    # 逐篇 CSV
    with (args.out / f"{args.prefix}section_wordcounts.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["paper", *SECTIONS])
        w.writeheader()
        w.writerows(rows)

    # 逐 section 统计 + 覆盖率
    total = len(rows)
    summ: list[dict] = []
    for s in SECTIONS:
        vals = [r[s] for r in rows if isinstance(r[s], int) and r[s] > 30]
        cov = len(vals)
        stats = robust_stats(vals) if cov >= 3 else {"N": cov}
        summ.append({"section": s, "coverage": f"{cov}/{total}", **stats})

    with (args.out / f"{args.prefix}section_wordcount_summary.csv").open("w", newline="") as f:
        cols = ["section", "coverage", "N", "median", "Q1", "Q3",
                "mean", "std", "trimmed_mean"]
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(summ)

    # 控制台打印
    print(f"语料: {total} 篇方法论文 (已排除: {args.exclude})\n")
    print(f"{'section':<13}{'cover':<8}{'median':>8}{'IQR(Q1-Q3)':>16}"
          f"{'mean':>8}{'std':>7}{'trim_mean':>11}")
    for d in summ:
        if "median" in d:
            print(f"{d['section']:<13}{d['coverage']:<8}{d['median']:>8}"
                  f"{str(d['Q1'])+'-'+str(d['Q3']):>16}{d['mean']:>8}"
                  f"{d['std']:>7}{d['trimmed_mean']:>11}")
        else:
            print(f"{d['section']:<13}{d['coverage']:<8}  (覆盖不足, 跳过统计)")


if __name__ == "__main__":
    main()
