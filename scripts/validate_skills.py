#!/usr/bin/env python3
"""校验仓库内每个 SKILL.md 是否符合 Agent-Skills frontmatter 规范。

错误(error)会让 CI 失败;警告(warning)只提示不失败。检查项:
  - 每个 skill 目录都有 SKILL.md
  - frontmatter 含 name 与 description
  - name:<=64 字符、仅小写字母/数字/连字符、无保留词(anthropic/claude)、且 == 目录名
  - description:非空、<=1024 字符
  - SKILL.md 正文 <=500 行
  - references/ 下 >100 行的文件应以 "## Contents" 目录开头(警告)
仅用标准库;有任何 error 时以非零码退出。
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME_RE = re.compile(r"^[a-z0-9-]+$")
RESERVED = ("anthropic", "claude")
SKIP = {"scripts", ".git", ".github"}

errors: list[str] = []
warnings: list[str] = []


def parse_frontmatter(text: str) -> dict[str, str]:
    """解析 SKILL.md 顶部 YAML frontmatter 的标量键(name/description),无需 yaml 依赖。"""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out: dict[str, str] = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        out[key] = val
    return out


def main() -> int:
    """遍历所有 skill 目录,逐项校验并汇总。"""
    count = 0
    for name in sorted(os.listdir(ROOT)):
        d = os.path.join(ROOT, name)
        if not os.path.isdir(d) or name in SKIP or name.startswith("."):
            continue
        skill_md = os.path.join(d, "SKILL.md")
        if not os.path.isfile(skill_md):
            continue  # 非 skill 目录
        count += 1
        text = open(skill_md, encoding="utf-8").read()
        fm = parse_frontmatter(text)
        nm, desc = fm.get("name", ""), fm.get("description", "")

        if not nm:
            errors.append(f"{name}: 缺少 frontmatter name")
        else:
            if nm != name:
                errors.append(f'{name}: name "{nm}" 与目录名不一致')
            if len(nm) > 64:
                errors.append(f"{name}: name 超过 64 字符")
            if not NAME_RE.match(nm):
                errors.append(f"{name}: name 含非法字符(仅允许小写字母/数字/连字符)")
            if any(r in nm.lower() for r in RESERVED):
                errors.append(f"{name}: name 含保留词(anthropic/claude)")

        if not desc:
            errors.append(f"{name}: 缺少或空 description")
        elif len(desc) > 1024:
            errors.append(f"{name}: description 超过 1024 字符({len(desc)})")

        body_lines = text.count("\n") + 1
        if body_lines > 500:
            errors.append(f"{name}: SKILL.md 超过 500 行({body_lines})")

        refdir = os.path.join(d, "references")
        if os.path.isdir(refdir):
            for rf in sorted(os.listdir(refdir)):
                if not rf.endswith(".md"):
                    continue
                rtext = open(os.path.join(refdir, rf), encoding="utf-8").read()
                if rtext.count("\n") + 1 > 100 and "## Contents" not in rtext:
                    warnings.append(f"{name}/references/{rf}: >100 行但无 '## Contents' 目录")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\n已校验 {count} 个 skill — {len(errors)} 个错误, {len(warnings)} 个警告")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
