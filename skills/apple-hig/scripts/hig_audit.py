#!/usr/bin/env python3
"""HIG 机械化冒烟检查器 —— 扫描 CSS/HTML，标记高信号、可机判的 Apple HIG 违规。

定位:这是"审查模式"的第一道机械关卡,只能抓**可被正则机判**的违规
(过小点击区、outline:none 无替代、缺 prefers-reduced-motion / prefers-color-scheme、
禁用缩放的 viewport、非系统字体、可点击的裸 div/span、无标签的图标按钮)。
它**不能**判断布局、语义、文案是否符合 HIG —— 那要走 references/review-checklist.md 的人工判断关。

用法:
    uv run apple-hig/scripts/hig_audit.py path/to/src          # 扫描整个目录
    uv run apple-hig/scripts/hig_audit.py styles.css index.html # 或指定文件
    uv run apple-hig/scripts/hig_audit.py src --no-fail         # 有发现也返回 0(仅报告)

仅依赖标准库;有 error/warn 级发现时默认以非零码退出(便于接 CI),info 不影响退出码。
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# 触发扫描的文件后缀(CSS 与各类 HTML/模板;JSX/TSX 也常含内联 className+style,一并扫文本)
CSS_EXT = {".css", ".scss", ".less"}
HTML_EXT = {".html", ".htm", ".vue", ".svelte", ".jsx", ".tsx"}
MIN_TARGET_PX = 44  # HIG 最小点击区:44×44 pt
# 选择器里出现这些词,才把"显式小尺寸"视为可疑点击区(降低误报)
INTERACTIVE_HINT = re.compile(r"button|btn|\.tab|nav|icon|chip|fab|toggle|link|menu", re.I)


@dataclass
class Finding:
    """一条审查发现:严重级、规则名、文件、行号、说明。"""

    severity: str  # "error" | "warn" | "info"
    rule: str
    file: str
    line: int
    message: str


def _line_of(text: str, pos: int, offset: int = 0) -> int:
    """根据字符偏移量计算 1-based 行号;offset 用于把"片段内行号"换算回原文件行号。"""
    return text.count("\n", 0, pos) + 1 + offset


def gather_files(paths: list[str]) -> list[Path]:
    """把输入的文件/目录展开成待扫描的文件列表(目录递归,按后缀过滤)。"""
    out: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            out += [f for f in sorted(p.rglob("*")) if f.suffix.lower() in CSS_EXT | HTML_EXT]
        elif p.is_file():
            out.append(p)
    return out


def scan_css_regex(text: str, fname: str, offset: int = 0) -> list[Finding]:
    """逐条正则检查,对任意文本都安全、行号准确:outline:none、非系统字体。"""
    found: list[Finding] = []

    # outline:none / outline:0 —— 去掉焦点环却未必有替代,焦点不可见是硬伤
    for m in re.finditer(r"outline\s*:\s*(none|0)\b", text, re.I):
        found.append(Finding("warn", "focus-visible", fname, _line_of(text, m.start(), offset),
                             "outline:none 移除了焦点环——必须用 :focus-visible 提供同样可见的替代"))

    # 非系统字体栈 —— 想要原生质感应优先 -apple-system / system-ui
    for m in re.finditer(r"font-family\s*:\s*([^;{}]+)", text, re.I):
        value = m.group(1).lower()
        if "-apple-system" not in value and "system-ui" not in value and "var(" not in value:
            found.append(Finding("info", "system-font", fname, _line_of(text, m.start(), offset),
                                 "font-family 未含系统字体栈(-apple-system/system-ui),原生观感会打折"))
    return found


def scan_css_filelevel(text: str, fname: str) -> list[Finding]:
    """文件级整体判断(只看"有没有",不依赖行号):缺 reduced-motion、缺 dark-mode。"""
    found: list[Finding] = []
    if re.search(r"@keyframes|transition\s*:|animation\s*:", text, re.I) \
            and "prefers-reduced-motion" not in text:
        found.append(Finding("warn", "reduced-motion", fname, 1,
                             "存在 transition/animation 但缺 @media (prefers-reduced-motion: reduce)"))
    if re.search(r"(background|color)\s*:", text, re.I) and "prefers-color-scheme" not in text:
        found.append(Finding("info", "dark-mode", fname, 1,
                             "未见 @media (prefers-color-scheme: dark);确认深色模式是否单独提供"))
    return found


def scan_css_targets(css: str, fname: str, offset: int = 0) -> list[Finding]:
    """块级:交互选择器显式 <44px。只应喂"纯 CSS"(CSS 文件或 <style> 块体),选择器才干净。"""
    found: list[Finding] = []
    for block in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        selector, body = block.group(1), block.group(2)
        if not INTERACTIVE_HINT.search(selector):
            continue
        for d in re.finditer(r"(min-height|height|min-width|width)\s*:\s*(\d+)px", body, re.I):
            if int(d.group(2)) < MIN_TARGET_PX:
                line = _line_of(css, block.start(2) + d.start(), offset)
                found.append(Finding("warn", "touch-target", fname, line,
                                     f"交互选择器 '{selector.strip()[:40]}' 的 {d.group(1)}:{d.group(2)}px "
                                     f"< {MIN_TARGET_PX}px;点击区应≥44×44px(可用 padding 补足)"))
    return found


def iter_style_blocks(html: str):
    """产出 HTML 中每个 <style>…</style> 的(块体, 起始行偏移),供块级扫描换算原文件行号。"""
    for m in re.finditer(r"<style\b[^>]*>(.*?)</style>", html, re.I | re.S):
        yield m.group(1), _line_of(html, m.start(1)) - 1


def check_html_text(text: str, fname: str) -> list[Finding]:
    """对 HTML 文本做结构性检查:禁用缩放、可点击裸 div/span、无标签图标按钮。"""
    found: list[Finding] = []

    # 1) viewport 禁用缩放 —— user-scalable=no / maximum-scale=1 是无障碍硬伤
    for m in re.finditer(r"user-scalable\s*=\s*no|maximum-scale\s*=\s*1(\.0)?\b", text, re.I):
        found.append(Finding("error", "zoom-disabled", fname, _line_of(text, m.start()),
                             "viewport 禁用了缩放;移除 user-scalable=no / maximum-scale=1,尊重用户缩放"))

    # 2) 带 onclick 的裸 <div>/<span>,缺 role+tabindex —— 应改用原生 button/a 或补齐可达性
    for m in re.finditer(r"<(div|span)\b[^>]*\bonclick\b[^>]*>", text, re.I):
        tag = m.group(0)
        if "role=" not in tag.lower() or "tabindex=" not in tag.lower():
            found.append(Finding("warn", "div-button", fname, _line_of(text, m.start()),
                                 "可点击的 <div>/<span> 缺 role/tabindex;优先用 <button>/<a>,否则补齐键盘可达性"))

    # 3) 图标按钮无可访问名 —— <button> 内只有 icon/svg/img 且无 aria-label/文本
    for m in re.finditer(r"<button\b([^>]*)>(.*?)</button>", text, re.I | re.S):
        attrs, inner = m.group(1).lower(), m.group(2)
        text_only = re.sub(r"<[^>]+>", "", inner).strip()
        only_icon = re.search(r"<(svg|img|i)\b", inner, re.I) and not text_only
        if only_icon and "aria-label" not in attrs and "aria-labelledby" not in attrs and "title=" not in attrs:
            found.append(Finding("warn", "icon-label", fname, _line_of(text, m.start()),
                                 "纯图标按钮缺 aria-label;图标控件必须有可访问名"))
    return found


def audit(files: list[Path]) -> list[Finding]:
    """对每个文件按类型分派检查;HTML 同时跑 CSS 规则以覆盖内联 <style> 与 style 属性。"""
    findings: list[Finding] = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        suffix = f.suffix.lower()
        if suffix in CSS_EXT:  # 纯 CSS:三类检查直接喂全文
            findings += scan_css_regex(text, str(f))
            findings += scan_css_filelevel(text, str(f))
            findings += scan_css_targets(text, str(f))
        else:  # HTML/模板:结构检查 + 安全正则(全文,行号准) + 块级仅扫 <style> 块体(行号带偏移)
            findings += check_html_text(text, str(f))
            findings += scan_css_regex(text, str(f))
            findings += scan_css_filelevel(text, str(f))
            for body, off in iter_style_blocks(text):
                findings += scan_css_targets(body, str(f), off)
    return findings


def report(findings: list[Finding]) -> None:
    """按严重级分组打印报告,并给出每条规则的修复指引来源。"""
    order = {"error": 0, "warn": 1, "info": 2}
    icon = {"error": "✗", "warn": "!", "info": "·"}
    findings.sort(key=lambda x: (order[x.severity], x.file, x.line))
    for fd in findings:
        print(f"{icon[fd.severity]} [{fd.severity}] {fd.rule}  {fd.file}:{fd.line}\n    {fd.message}")
    errs = sum(1 for f in findings if f.severity == "error")
    warns = sum(1 for f in findings if f.severity == "warn")
    infos = sum(1 for f in findings if f.severity == "info")
    print(f"\n共 {len(findings)} 条:{errs} error / {warns} warn / {infos} info")
    print("这是机械冒烟;布局/语义/文案请走 references/review-checklist.md 的人工判断关。")


def main() -> int:
    """解析参数,收集文件,执行审查并按发现决定退出码。"""
    ap = argparse.ArgumentParser(description="Apple HIG 机械化冒烟检查(CSS/HTML)")
    ap.add_argument("paths", nargs="+", help="待扫描的文件或目录")
    ap.add_argument("--no-fail", action="store_true", help="即使有发现也返回 0(仅报告)")
    args = ap.parse_args()

    files = gather_files(args.paths)
    if not files:
        print("未找到可扫描的 CSS/HTML 文件。")
        return 0
    findings = audit(files)
    report(findings)
    hard = any(f.severity in ("error", "warn") for f in findings)
    return 0 if args.no_fail else (1 if hard else 0)


if __name__ == "__main__":
    sys.exit(main())
