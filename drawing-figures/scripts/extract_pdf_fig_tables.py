#!/usr/bin/env python3
"""从本地 PDF 论文中抽取 figure/table caption 候选，输出 Markdown 审计文件。"""

from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Caption:
    """存储一条抽取到的 figure 或 table caption 候选。"""

    kind: str
    number: str
    text: str


def parse_args() -> argparse.Namespace:
    """命令行:本地 PDF 目录与输出 md 必填。"""
    p = argparse.ArgumentParser(description="从本地 PDF 抽 figure/table caption 候选")
    p.add_argument("--pdf-dir", dest="pdf_dir", type=Path, required=True, help="PDF 根目录")
    p.add_argument("--out", type=Path, required=True, help="输出 md 路径")
    return p.parse_args()


def pdf_to_lines(pdf_path: Path) -> list[str]:
    """调用 pdftotext，返回原始行列表（已去首尾空白）。"""
    result = subprocess.run(
        ["pdftotext", "-raw", str(pdf_path), "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        errors="replace",
    )
    return [line.strip() for line in result.stdout.splitlines()]


def normalize_text(text: str) -> str:
    """归一化空白及常见 PDF 抽取乱码（连字符等）。"""
    text = re.sub(r"\s+", " ", text)
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl")
    text = text.replace("state-of-the-art", "state of the art")
    text = re.sub(r"-\s+", "", text)
    return text.strip()


def looks_like_caption_start(line: str) -> re.Match[str] | None:
    """检测行是否为 Figure/Table caption 起始，忽略正文引用。"""
    fig_match = re.match(r"^(Fig\.|Figure)\s+([0-9]+|[IVX]+)[\.:]\s*(.*)$", line, flags=re.I)
    if fig_match:
        return fig_match
    table_match = re.match(r"^(Table)\s+([0-9]+|[IVX]+)\.?\s*(.*)$", line, flags=re.I)
    if not table_match:
        return None
    rest = table_match.group(3).strip()
    if re.match(r"^(compares|shows|depicts|outlines|presents|displays|summarizes)\b", rest, flags=re.I):
        return None
    return table_match


def collect_caption(lines: list[str], start_index: int, match: re.Match[str]) -> Caption:
    """从起始行及后续续行收集完整 caption 文本。"""
    kind_token, number, rest = match.groups()
    kind = "Figure" if kind_token in {"Fig.", "Figure"} else "Table"
    parts = [rest] if rest else []

    max_extra_lines = 5 if kind == "Figure" else 4
    for offset in range(1, max_extra_lines + 1):
        if start_index + offset >= len(lines):
            break
        candidate = lines[start_index + offset].strip()
        if not candidate:
            if parts:
                break
            continue
        if looks_like_caption_start(candidate):
            break
        if re.match(r"^([0-9]+\.|Abstract|Introduction|References|Keywords)\b", candidate):
            break
        if re.match(r"^[A-Z][a-z]+ et al\.", candidate):
            break
        parts.append(candidate)
        joined = normalize_text(" ".join(parts))
        if len(joined) > 60 and joined.endswith("."):
            break

    text = normalize_text(" ".join(parts))
    text = re.sub(r"^(compares|shows|depicts|outlines)\b.*", "", text, flags=re.I).strip()
    return Caption(kind=kind, number=number, text=text)


def parse_captions(lines: list[str]) -> list[Caption]:
    """从文本行列表中解析所有 caption 候选，返回 Caption 列表（纯函数，无 IO）。"""
    results: list[Caption] = []
    for idx, line in enumerate(lines):
        match = looks_like_caption_start(line)
        if not match:
            continue
        caption = collect_caption(lines, idx, match)
        results.append(caption)
    return results


def extract_captions(pdf_path: Path) -> tuple[list[Caption], list[Caption]]:
    """从单个 PDF 抽取去重后的 figure/table caption 列表。"""
    lines = pdf_to_lines(pdf_path)
    figures: dict[str, Caption] = {}
    tables: dict[str, Caption] = {}
    for cap in parse_captions(lines):
        if len(cap.text) < 8:
            continue
        bucket = figures if cap.kind == "Figure" else tables
        old = bucket.get(cap.number)
        if old is None or len(cap.text) > len(old.text):
            bucket[cap.number] = cap
    fig_list = sorted(figures.values(), key=lambda c: int(c.number) if c.number.isdigit() else 999)
    tab_list = sorted(tables.values(), key=lambda c: int(c.number) if c.number.isdigit() else 999)
    return fig_list, tab_list


def paper_label(pdf_path: Path) -> str:
    """从 PDF 文件名生成简短论文标签。"""
    return pdf_path.stem.replace("_", " ")


def render_markdown(rows: list[tuple[Path, list[Caption], list[Caption]]]) -> str:
    """将抽取结果渲染为中文 Markdown 审计文件字符串。"""
    lines = [
        "# 论文图表审计",
        "",
        "本文档从指定 PDF 目录批量抽取 Figure/Table caption，用于快速观察论文通常画哪些图、放哪些表。",
        "",
        "说明：caption 保留论文原文英文，方便后续回到 PDF 核对；自动抽取结果可能包含换行、断词或少量正文误匹配，正式引用前需要人工复核。",
        "",
        f"PDF 总数：{len(rows)}",
        "",
        "| 论文 | 图数量 | 表数量 |",
        "| --- | ---: | ---: |",
    ]
    for pdf_path, figures, tables in rows:
        lines.append(f"| {paper_label(pdf_path)} | {len(figures)} | {len(tables)} |")
    lines.append("")

    for pdf_path, figures, tables in rows:
        lines.append(f"## {paper_label(pdf_path)}")
        lines.append("")
        lines.append("图：")
        if figures:
            for cap in figures:
                lines.append(f"- Fig. {cap.number}: {cap.text}")
        else:
            lines.append("- 未抽取到图 caption")
        lines.append("")
        lines.append("表：")
        if tables:
            for cap in tables:
                lines.append(f"- Table {cap.number}: {cap.text}")
        else:
            lines.append("- 未抽取到表 caption")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    """主入口：扫描 PDF 目录，抽取 caption 并写出 Markdown 文件。"""
    args = parse_args()
    pdf_dir: Path = args.pdf_dir
    out_path: Path = args.out

    pdfs = sorted(pdf_dir.glob("*.pdf"))
    rows = []
    for pdf_path in pdfs:
        try:
            rows.append((pdf_path, *extract_captions(pdf_path)))
        except subprocess.CalledProcessError as exc:
            rows.append((pdf_path, [], [Caption("Table", "ERR", normalize_text(exc.stderr))]))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_markdown(rows), encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
