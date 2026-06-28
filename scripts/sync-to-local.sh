#!/usr/bin/env bash
# 把本仓库的所有 skill 同步到本地 Claude + Codex 的 skill 目录。
# 本仓库是唯一源(source of truth);本地只是它的镜像。
#
# 目标目录优先级:仓库根的 .sync-local.env(gitignored)> 环境变量 > 标准默认。
#   CLAUDE_SKILLS_DIR  默认 $HOME/.claude/skills
#   AGENTS_SKILLS_DIR  默认 $HOME/.agents/skills
#
# 只新增/覆盖本仓库里的 skill 目录;本地已有的其它 skill(如第三方 kami)保持不动。
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck disable=SC1091
[ -f "$REPO/.sync-local.env" ] && source "$REPO/.sync-local.env"
CLAUDE_SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
AGENTS_SKILLS_DIR="${AGENTS_SKILLS_DIR:-$HOME/.agents/skills}"

# 将仓库里每个含 SKILL.md 的目录拷到 $1;清理 Python 缓存;保留目标里的其它 skill。
sync_one() {
  local target="$1" n=0
  mkdir -p "$target"
  for d in "$REPO"/*/; do
    [ -f "${d}SKILL.md" ] || continue   # 只同步 skill 目录(跳过 scripts/ 等)
    local name; name="$(basename "$d")"
    rm -rf "${target:?}/$name"
    cp -r "$d" "$target/$name"
    n=$((n + 1))
  done
  find "$target" -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null || true
  find "$target" \( -name '*.pyc' -o -name '.DS_Store' \) -delete 2>/dev/null || true
  echo "  -> $target  ($n skills)"
}

echo "Syncing skills from: $REPO"
sync_one "$CLAUDE_SKILLS_DIR"
sync_one "$AGENTS_SKILLS_DIR"
echo "Done. 本地已有的非仓库 skill(如第三方)未受影响。"
