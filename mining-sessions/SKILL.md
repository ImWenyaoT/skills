---
name: mining-sessions
description: Use when asked to mine past Codex/Claude sessions for skill friction or recurring struggles and turn them into new or improved skills (the "auto-create skills from sessions" / "scan my sessions and update the skills" task). Covers where transcripts and custom skills actually live, filtering guardian-subagent noise, and skill-vs-memory triage. Do not trigger for importing an external/open-source skill, or for authoring a skill from scratch without mining past sessions.
---

# Creating Skills From Sessions

## Overview

Periodically turn lived experience into skills: scan past agent sessions, find where a
skill caused friction or where a task **recurs and struggles**, then create or improve a
skill. Core principle: **a skill must earn its place from real, repeated evidence — not a
hunch.** Pair it with whatever skill-authoring discipline you use (e.g. a RED-GREEN docs-TDD
workflow); this skill is the *session-mining + triage + placement* layer that feeds authoring.

## Where things actually live (verify before you grep — these paths bite)

| What | Location | Note |
|---|---|---|
| Codex transcripts (rich) | `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` | full conversation |
| — guardian noise | `session_meta.payload.source.subagent.other == "guardian"` | **~70% of files**; safety-judge subagents whose base prompt is full of "retry/failed". Exclude them or friction counts are garbage (one real run showed `retry`≈26000, almost all guardian). |
| Claude *pointers* (NOT transcripts) | `~/.claude/sessions/*.json` | only `pid`/`sessionId`/`cwd` — **no conversation**. Do not grep these for content. |
| Claude transcripts (rich) | `~/.claude/projects/<slugified-cwd>/*.jsonl` | the real Claude history (dozens per project) |
| Codex skills (user scope) | `~/.agents/skills/<name>/SKILL.md` | cross-runtime user skills |
| Codex skills (repo scope) | `$CWD/.agents/skills/`, `$REPO_ROOT/.agents/skills/` | project/org skills, scanned CWD→root |
| Claude skills (user scope) | `~/.claude/skills/<name>/SKILL.md` | global user skills |
| Claude skills (project scope) | `<project>/.claude/skills/<name>/SKILL.md` | per-project skills |
| Legacy personal staging | a non-standard staging dir left from an earlier setup (historically under `~/Documents`) | historical local staging area; migrate useful skills into the source repo, then remove duplicates |
| Installed/vendored packs | large third-party skill collections | **read-only — mine for patterns, never edit/republish** |

**Verify the path before you grep — skill homes vary by runtime and version** (some installs
also drop skills under `~/.codex/skills/`). Codex and Claude can't read each other's skill
trees, so a skill meant for both is copied into each. Tell *authored* skills (yours, editable)
apart from *installed* packs (third-party, read-only) before touching anything.

## Procedure

1. **Scan** both transcript trees with `scan_sessions.py` (guardian-filtered). Collect per
   session: `cwd` + first real user ask; skill mentions; friction signals — ENOENT on a
   `SKILL.md`, repeated retries on one command, user corrections (`不对` / `重来` / `又错` /
   "doesn't work" / "you keep"), reverts.
2. **Cluster** by `cwd` + first-ask to surface the recurring task domains.
3. **Triage** each candidate (table below).
4. **Merge before creating**: search the current skill library first and update the nearest
   existing skill when the new pattern is a variant, not a new workflow.
5. **Author** survivors with your skill-authoring workflow — and honor the user's
   `CLAUDE.md` / `AGENTS.md` (e.g. 中文对话, function-level comments, Python via `uv run`
   over new `.sh`, 替换而非叠加).
6. **Report** what you made and *why*; explicitly flag what you deliberately did **not**
   make.

## Triage: skill, memory, or neither

- Reusable **procedure / checklist / technique** that recurs across sessions → **skill**.
- A **fact or preference** ("user dislikes X", "metric protocol is Y") → **memory**, not a
  skill.
- One-off solution → **neither**.
- Require real evidence: repeated mistakes, a user-corrected boundary/preference, a reusable
  recovery path after tool failure, or a workflow with non-obvious verification steps.
- **Never resurrect an intentionally-deleted or archived skill.** A wiped skill is a
  decision, not a gap to refill — confirm with the user first.

## Placement & keeping runtimes in sync

- Keep the version-controlled skills repo as the source of truth. Do not write newly authored
  skills into `~/.codex/skills`, `~/.claude/skills`, or `~/.agents/skills` unless the user
  explicitly asks for an installed copy.
- Treat any non-standard legacy staging dir (e.g. an old `~/Documents/.agents/skills`) as a
  historical location, not a new home. If a skill there is still useful, absorb it into the
  source repo and delete the duplicate.
- Do not place a personal skill inside a project repo unless it is clearly project-specific.
- Pick scope by reach: a skill useful everywhere → user scope (`~/.agents/skills/` for Codex,
  `~/.claude/skills/` for Claude); a skill only meaningful inside one repo → that repo's
  `.agents/skills/` or `.claude/skills/`.
- To serve **both** Codex and Claude, the skill folder must exist in each tree (they can't
  read each other's). **Convention, not machinery:** after adding or editing a skill in one
  tree, copy the whole folder to the other so they match — `cp -r <skill> <other-skills-dir>/`.
  No symlink, no sync daemon needed; a plain copy is the lightest thing that works. If you
  want it hands-off, wire that copy into a runtime hook rather than maintaining a sync tool.
- One directory per skill, holding `SKILL.md` plus any tools/references alongside it.

## Common mistakes

- Counting friction without filtering guardian subagents → tens-of-thousands of phantom
  "retry/failed".
- Grepping `~/.claude/sessions/*.json` for content — they are pointers; use
  `~/.claude/projects/`.
- Mass-producing skills from a single session, or duplicating a live tool instead of
  pointing the skill at it.
- Editing installed/vendored third-party packs instead of only your own authored skills.

## Scan tool

`scan_sessions.py` (stdlib only) — guardian-filtered inventory of codex + claude
transcripts with friction & skill-mention tallies, plus `--dump <id>` to print one clean
transcript. Run `uv run python scan_sessions.py --help`.
