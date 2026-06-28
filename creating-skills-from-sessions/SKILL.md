---
name: creating-skills-from-sessions
description: Use when asked to mine past Codex/Claude sessions for skill friction or recurring struggles and turn them into new or improved skills (the "auto-create skills from sessions" / "scan my sessions and update the skills" task). Covers where transcripts and custom skills actually live, filtering guardian-subagent noise, and skill-vs-memory triage.
---

# Creating Skills From Sessions

## Overview

Periodically turn lived experience into skills: scan past agent sessions, find where a
skill caused friction or where a task **recurs and struggles**, then create or improve a
skill. Core principle: **a skill must earn its place from real, repeated evidence — not a
hunch.** Authoring discipline lives in `superpowers:writing-skills` (RED-GREEN for docs)
and `skill-creator`; this skill is the *session-mining + triage + placement* layer that
feeds them.

## Where things actually live (verify before you grep — these paths bite)

| What | Location | Note |
|---|---|---|
| Codex transcripts (rich) | `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` | full conversation |
| — guardian noise | `session_meta.payload.source.subagent.other == "guardian"` | **~70% of files**; safety-judge subagents whose base prompt is full of "retry/failed". Exclude them or friction counts are garbage (one real run showed `retry`≈26000, almost all guardian). |
| Claude *pointers* (NOT transcripts) | `~/.claude/sessions/*.json` | only `pid`/`sessionId`/`cwd` — **no conversation**. Do not grep these for content. |
| Claude transcripts (rich) | `~/.claude/projects/<slugified-cwd>/*.jsonl` | the real Claude history (dozens per project) |
| User custom skills (codex / cross-runtime) | `tian_wenyao/.agents/skills/<name>/SKILL.md` | in scope |
| User custom skills (Claude) | `tian_wenyao/.claude/skills/<name>/SKILL.md` | in scope |
| Personal / plugin skills | `~/.claude/skills/`, plugin caches | **OFF-LIMITS — never edit** |

Skills are **not** at `~/.codex/skills/` — probing that path is the single most-observed
friction in real sessions (repeated `sed: can't read .../SKILL.md: No such file`). The
custom-skill homes are the two `tian_wenyao` dirs above. `.skills_managed.json` is the
defunct auto-sync ledger; leave hand-written skills **out** of it (keep it `[]`).

## Procedure

1. **Scan** both transcript trees with `scan_sessions.py` (guardian-filtered). Collect per
   session: `cwd` + first real user ask; skill mentions; friction signals — ENOENT on a
   `SKILL.md`, repeated retries on one command, user corrections (`不对` / `重来` / `又错` /
   "doesn't work" / "you keep"), reverts.
2. **Cluster** by `cwd` + first-ask to surface the recurring task domains.
3. **Triage** each candidate (table below).
4. **Author** survivors via `superpowers:writing-skills` — and honor the user's
   `CLAUDE.md` / `AGENTS.md` (e.g. 中文对话, function-level comments, Python via `uv run`
   over new `.sh`, 替换而非叠加).
5. **Report** what you made and *why*; explicitly flag what you deliberately did **not**
   make.

## Triage: skill, memory, or neither

- Reusable **procedure / checklist / technique** that recurs across sessions → **skill**.
- A **fact or preference** ("user dislikes X", "metric protocol is Y") → **memory**, not a
  skill.
- One-off solution → **neither**.
- **Never resurrect an intentionally-deleted or archived skill.** A wiped skill is a
  decision, not a gap to refill — confirm with the user first. (See workspace memory on
  intentional deletions / "别复原".)

## Placement & keeping both dirs in sync

- Both runtime dirs are kept **identical**: `tian_wenyao/.agents/skills/` (codex / cross-
  runtime) and the **project-level** `tian_wenyao/.claude/skills/` (Claude Code project
  skills — NOT global `~/.claude/skills`, which is off-limits). Claude can't read `.agents`
  and codex can't read `.claude`, so the two real copies are structural, not waste.
- **Convention, not machinery:** after adding or editing a skill in one dir, copy the whole
  skill folder to the other so they match — `cp -r <skill> <other-skills-dir>/`. That's it:
  no symlink, no sync script, no systemd timer (the old auto-sync infra was deliberately
  removed, and a standalone sync tool was rejected as the awkward middle — a plain copy is
  lighter for the same result). If you ever want it hands-off, wire the copy into a runtime
  hook instead of carrying a tool.
- One directory per skill: `creating-skills-from-sessions/SKILL.md` (+ tools alongside).

## Common mistakes

- Counting friction without filtering guardian subagents → tens-of-thousands of phantom
  "retry/failed".
- Grepping `~/.claude/sessions/*.json` for content — they are pointers; use
  `~/.claude/projects/`.
- Mass-producing skills from a single session, or duplicating a live tool instead of
  pointing the skill at it.
- Editing personal / plugin skills — scope is the two `tian_wenyao` dirs only.

## Scan tool

`scan_sessions.py` (stdlib only) — guardian-filtered inventory of codex + claude
transcripts with friction & skill-mention tallies, plus `--dump <id>` to print one clean
transcript. Run `uv run python scan_sessions.py --help`.
