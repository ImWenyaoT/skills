---
name: mining-sessions
description: 'Session mining for recurring skill friction: scan past Codex/Claude transcripts, filter guardian-subagent noise, triage skill-vs-memory candidates, and turn repeated struggles into new or improved skills. Trigger on "auto-create skills from sessions" or "scan my sessions and update skills". Do not use for external skill imports or from-scratch authoring without session evidence.'
---

# Creating Skills From Sessions

## Overview

Periodically turn lived experience into skills: scan past agent sessions, find where a
skill caused friction or where a task **recurs and struggles**, then create or improve a
skill. Core principle: **a skill must earn its place from real, repeated evidence — not a
hunch.** Pair it with whatever skill-authoring discipline you use (e.g. a RED-GREEN docs-TDD
workflow); this skill is the *session-mining + triage + placement* layer that feeds authoring.

Before scanning or placing a skill, read
[`references/runtime-paths.md`](references/runtime-paths.md). It is the source of truth for
transcript locations, editable skill homes, cross-runtime placement, and common path mistakes.

## Procedure

1. **Scan** both transcript trees with `scripts/scan_sessions.py` (guardian-filtered). Collect per
   session: `cwd` + first real user ask; skill mentions; friction signals — ENOENT on a
   `SKILL.md`, repeated retries on one command, user corrections, and reverts.
2. **Cluster** by `cwd` + first-ask to surface the recurring task domains.
3. **Triage** each candidate (table below).
4. **Merge before creating**: search the current skill library first and update the nearest
   existing skill when the new pattern is a variant, not a new workflow.
5. **Author** survivors with your skill-authoring workflow and honor the repository's
   `CLAUDE.md` / `AGENTS.md`, language, tool, and replacement conventions.
6. **Report** every candidate using the final report schema below. Done means every
   created/updated skill cites repeated session evidence, and every rejected candidate is
   classified as skill, memory, or neither.

## Final report schema

Report one row per candidate with all of these fields:

| Field | Required content |
|---|---|
| Candidate | Short, stable name for the recurring friction or workflow. |
| Evidence | Evidence count and the contributing session IDs. |
| Decision | `skill`, `memory`, or `neither`. |
| Action taken | Created/updated skill path, recorded memory action, or `none`. |
| Rejected reason | Why no skill was created; use `not rejected` for accepted skill candidates. |

Do not collapse rejected candidates into a summary count: each rejection needs its own
evidence, decision, action, and reason so another agent can audit the triage.

## Triage: skill, memory, or neither

- Reusable **procedure / checklist / technique** that recurs across sessions → **skill**.
- A **fact or preference** ("user dislikes X", "metric protocol is Y") → **memory**, not a
  skill.
- One-off solution → **neither**.
- Require real evidence: repeated mistakes, a user-corrected boundary/preference, a reusable
  recovery path after tool failure, or a workflow with non-obvious verification steps.
- **Never resurrect an intentionally-deleted or archived skill.** A wiped skill is a
  decision, not a gap to refill — confirm with the user first.

## Scan tool

`scripts/scan_sessions.py` (stdlib only) — guardian-filtered inventory of codex + claude
transcripts with friction & skill-mention tallies, plus `--dump <id>` to print one clean
transcript. From the repository root, run
`uv run python mining-sessions/scripts/scan_sessions.py --help`.
