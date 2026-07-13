#!/usr/bin/env python3
"""扫描 Codex / Claude 会话记录，为「从会话里提炼 skill」提供证据。

用法:
    uv run python mining-sessions/scripts/scan_sessions.py                 # 盘点 codex+claude，过滤 guardian
    uv run python mining-sessions/scripts/scan_sessions.py --codex         # 只看 codex
    uv run python mining-sessions/scripts/scan_sessions.py --claude        # 只看 claude 真实 transcript
    uv run python mining-sessions/scripts/scan_sessions.py --dump <子串>   # 打印某个会话的干净对话（按文件名子串匹配）

设计要点:
    - 只依赖标准库（无需联网/安装）。
    - 默认剔除 codex 的 guardian 子代理会话（安全判定子代理，占比约 7 成，
      其基础提示词里满是 retry/failed，会把摩擦统计污染到上万）。
    - ~/.claude/sessions/*.json 只是进程指针(pid/cwd)，不是对话；真实 Claude
      历史在 ~/.claude/projects/<slug>/*.jsonl，本脚本扫的是后者。
"""
from __future__ import annotations
import argparse
import glob
import json
import os
import re
from collections import Counter, defaultdict

CODEX_GLOB = os.path.expanduser("~/.codex/sessions/**/*.jsonl")
CLAUDE_GLOB = os.path.expanduser("~/.claude/projects/**/*.jsonl")

# 摩擦信号（中英混合）：选用足够特异、不易出现在系统脚手架里的措辞，
# 避免像 "revert"/"you keep" 这种泛词在每个会话的注入提示里全员命中。
FRICTION = [
    "no such file", "doesn't work", "didn't work", "not working", "still failing",
    "command not found", "permission denied", "traceback (most recent call last)",
    "重来", "又错了", "还是不行", "不对", "别这样", "你怎么又", "为什么还",
]
# skill 关注词：用于发现哪些 skill 被用、是否伴随报错
SKILL_KW = ["skill", "skill.md", ".agents/skills", ".claude/skills", "superpowers"]

RUNTIME_BLOCK_PREFIX_RE = re.compile(
    r"^<(environment_context|user_instructions|recommended_plugins)(?:\s[^>]*)?>"
    r".*?</\1>\s*",
    re.DOTALL | re.IGNORECASE,
)
AGENTS_PREAMBLE_RE = re.compile(
    r"^# AGENTS\.md instructions.*?(?:</INSTRUCTIONS>|</environment_context>)\s*",
    re.DOTALL | re.IGNORECASE,
)


def strip_runtime_preamble(text: str) -> str:
    """只剥离消息开头连续的运行时注入块，保留正文中的同名标签。"""
    text = text.strip()
    while text:
        cleaned = RUNTIME_BLOCK_PREFIX_RE.sub("", text, count=1)
        cleaned = AGENTS_PREAMBLE_RE.sub("", cleaned, count=1).strip()
        if cleaned == text:
            break
        text = cleaned
    return text


def iter_lines(path):
    """逐行 yield 解析后的 JSON 对象，跳过坏行。"""
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue
    except OSError:
        return


def is_guardian(meta: dict) -> bool:
    """判断一个 codex 会话是否为 guardian 安全判定子代理（应从分析中剔除）。"""
    src = meta.get("source") if isinstance(meta, dict) else None
    if not isinstance(src, dict):
        return False
    sub = src.get("subagent")
    return isinstance(sub, dict) and sub.get("other") == "guardian"


def harvest_text(obj) -> list[str]:
    """从任意嵌套结构里递归抽取所有字符串，便于关键词命中。"""
    out: list[str] = []

    def walk(x):
        if isinstance(x, str):
            out.append(x)
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(obj)
    return out


def first_user_ask(lines: list[dict]) -> str:
    """返回首条真正的用户请求文本（跳过 environment/instructions 注入头）。"""
    for d in lines:
        p = d.get("payload", d)
        if not isinstance(p, dict) or p.get("role") != "user":
            continue
        content = p.get("content")
        text = ""
        if isinstance(content, list):
            for seg in content:
                if isinstance(seg, dict) and seg.get("type") in ("input_text", "text"):
                    text += seg.get("text", "")
        elif isinstance(content, str):
            text = content
        text = strip_runtime_preamble(text)
        if not text or text.startswith("#"):
            continue
        if "My request for Codex:" in text:
            text = text.split("My request for Codex:")[-1].strip()
        return text[:180].replace("\n", " ")
    return "(no user message)"


def analyse(paths: list[str], drop_guardian: bool):
    """盘点会话：输出 cwd 分布、skill 命中、摩擦信号 top。"""
    sessions: list[tuple[str, str, str]] = []   # (basename, cwd, first_ask)
    skill_hits: Counter[str] = Counter()         # skill 关键词 -> 命中片段数
    friction: dict[str, list[int]] = defaultdict(lambda: [0, 0])  # 词 -> [命中文件数, 总次数]
    cwds: Counter[str] = Counter()

    for path in paths:
        lines = list(iter_lines(path))
        meta: dict = next((d.get("payload", {}) for d in lines if d.get("type") == "session_meta"), {})
        if drop_guardian and is_guardian(meta):
            continue
        cwd = meta.get("cwd", "?") if isinstance(meta, dict) else "?"
        cwds[cwd] += 1
        sessions.append((os.path.basename(path), cwd, first_user_ask(lines)))

        blob = "\n".join(s for d in lines for s in harvest_text(d.get("payload", d))).lower()
        for kw in SKILL_KW:
            if kw in blob:
                skill_hits[kw] += blob.count(kw)
        for fr in FRICTION:
            c = blob.count(fr)
            if c:
                friction[fr][0] += 1
                friction[fr][1] += c

    print(f"\n真实会话(已{'剔除 guardian' if drop_guardian else '保留全部'}): {len(sessions)}")
    print("\n=== 工作目录分布(任务域线索) ===")
    for cwd, n in cwds.most_common(20):
        print(f"  {n:3d}  {cwd}")
    print("\n=== 每个会话: cwd + 首条用户请求 ===")
    for name, cwd, ask in sessions:
        print(f"  · [{cwd}] {ask}")
    print("\n=== skill 关键词命中 ===")
    for kw, n in skill_hits.most_common():
        print(f"  {n:5d}  {kw}")
    print("\n=== 摩擦信号 top(文件数 / 总次数) ===")
    for fr, (files, total) in sorted(friction.items(), key=lambda kv: -kv[1][1]):
        print(f"  files={files:3d} total={total:4d}  {fr!r}")


def dump(paths: list[str], needle: str):
    """打印名字含 needle 的会话的干净 user/assistant 对话。"""
    for path in paths:
        if needle not in os.path.basename(path):
            continue
        print("=" * 90, "\nFILE:", os.path.basename(path), "\n" + "=" * 90)
        for d in iter_lines(path):
            t = d.get("type")
            p = d.get("payload", d)
            if t == "event_msg" and p.get("type") in ("agent_message", "agent_reasoning"):
                msg = (p.get("message") or p.get("text") or "").strip()
                if msg:
                    print(f"\n----🤖{p['type']}----\n{msg[:1800]}")
            elif isinstance(p, dict) and p.get("role") in ("user", "assistant"):
                content = p.get("content")
                text = content if isinstance(content, str) else "".join(
                    s.get("text", "") for s in content if isinstance(s, dict)
                ) if isinstance(content, list) else ""
                text = text.strip()
                if text and not text.startswith(("<environment_context>", "<user_instructions>")):
                    tag = "👤USER" if p["role"] == "user" else "🤖ASST"
                    print(f"\n----{tag}----\n{text[:2200]}")


def main():
    """解析命令行参数，分发到盘点或转储。"""
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--codex", action="store_true", help="只扫 codex 会话")
    ap.add_argument("--claude", action="store_true", help="只扫 claude 真实 transcript")
    ap.add_argument("--keep-guardian", action="store_true", help="不剔除 guardian 子代理(默认剔除)")
    ap.add_argument("--dump", metavar="SUBSTR", help="打印文件名含该子串的会话对话")
    args = ap.parse_args()

    paths = []
    if not args.claude:
        paths += sorted(glob.glob(CODEX_GLOB, recursive=True))
    if not args.codex:
        paths += sorted(glob.glob(CLAUDE_GLOB, recursive=True))

    if args.dump:
        dump(paths, args.dump)
    else:
        analyse(paths, drop_guardian=not args.keep_guardian)


if __name__ == "__main__":
    main()
