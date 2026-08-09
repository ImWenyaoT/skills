---
name: curating-skills
description: 'Triage a candidate before it enters the skill library: mine past Codex or Claude transcripts for recurring friction worth capturing, or vet a skill someone else published for provenance and license. Decides skill vs memory vs neither, and whether to patch a near-duplicate rather than add one. Trigger on "auto-create skills from my transcripts", "scan my history and update skills", 从会话里提炼 skill, 引入或审核开源 skill. Do not use for authoring new skill prose from scratch, or for designing how an application stores its own sessions, transcripts, or memory.'
license: MIT
---

# Curating the Skill Library

## Overview

Two things feed one decision. Lived sessions surface where a task **recurs and struggles**;
external repositories surface skills someone else already wrote. Both arrive as
*candidates*, and both face the same two questions:

1. Does this capability earn a place in the library at all?
2. If it does, should it **patch an existing skill** rather than become a new one?

Core principle: **a skill must earn its place from real, repeated evidence — not a hunch,
and not from the fact that a well-written external skill exists.**

Scope note: this skill decides *whether and where* a capability enters the library. Writing
the `SKILL.md` prose itself — naming, description wording, structure, degrees of freedom —
is a separate discipline; follow the authoring doctrine in the target repository's
`AGENTS.md` / `CLAUDE.md` and whatever authoring workflow you already run.

Before scanning transcripts or placing a skill, read
[`references/runtime-paths.md`](references/runtime-paths.md). It is the source of truth for
transcript locations, editable skill homes, cross-runtime placement, and common path
mistakes.

## Source A — mine your own sessions

1. **Scan** both transcript trees with `scripts/scan_sessions.py` (guardian-filtered).
   Collect per session: `cwd` + first real user ask; skill mentions; friction signals —
   ENOENT on a `SKILL.md`, repeated retries on one command, user corrections, and reverts.
   Treat injected blocks such as plugin recommendations and environment metadata as runtime
   noise, not user asks.
2. **Cluster** by `cwd` + first-ask to surface the recurring task domains.
3. **Triage** each candidate (table below).
4. **Merge before creating**: search the current skill library first and update the nearest
   existing skill when the new pattern is a variant, not a new workflow.
5. **Author** survivors with your skill-authoring workflow and honor the repository's
   `CLAUDE.md` / `AGENTS.md`, language, tool, and replacement conventions.
6. **Report** every candidate using the final report schema below.

Done means every created/updated skill cites repeated session evidence, and every rejected
candidate is classified as skill, memory, or neither.

## Source B — adopt an external skill

Bring an external skill into your own library deliberately: prefer **adapting a focused
workflow** over copying a broad skill, and never blur provenance.

- Prefer adapting a focused workflow over copying a broad skill wholesale.
- Record **provenance** for every external idea used: source URL/path, license,
  version/commit, license compatibility, required notices, and your local changes.
- Keep imported workflow skills in your skills directory; don't mix them with
  runtime/product code.
- Strip vendor-specific assumptions that don't apply to you.
- If license or provenance is unclear, **do not copy, paraphrase, or closely adapt** the
  source — write a clean-room skill from independently stated needs.
- Preserve required copyright / attribution / NOTICE text when the license demands it.

Adoption checklist:

1. Identify the repeated workflow the skill should improve.
2. Inspect the source skill and its license.
3. Decide: use as-is, adapt, or clean-room rewrite.
4. Keep the `SKILL.md` concise and scoped to your need.
5. Add a `## Provenance` section for any external idea, copy, fork, or adaptation.
6. Run an independent, read-only adversarial review before accepting it.

Done means license, provenance, local changes, and attribution requirements are recorded,
or the skill is rejected.

## Triage: skill, memory, or neither

- Reusable **procedure / checklist / technique** that recurs across sessions → **skill**.
- A **fact or preference** ("user dislikes X", "metric protocol is Y") → **memory**, not a
  skill.
- One-off solution → **neither**.
- Require real evidence: repeated mistakes, a user-corrected boundary/preference, a
  reusable recovery path after tool failure, or a workflow with non-obvious verification
  steps. An external skill's own polish is not evidence — the evidence must be your
  recurring need for it.
- **Never resurrect an intentionally-deleted or archived skill.** A wiped skill is a
  decision, not a gap to refill — confirm with the user first.

## Final report schema

Report one row per candidate, from either source, with all of these fields:

| Field | Required content |
|---|---|
| Candidate | Short, stable name for the recurring friction or workflow. |
| Evidence | Evidence count and the contributing session IDs, or the external source and license. |
| Decision | `skill`, `memory`, or `neither`. |
| Action taken | Created/updated skill path, recorded memory action, or `none`. |
| Rejected reason | Why no skill was created; use `not rejected` for accepted skill candidates. |

Do not collapse rejected candidates into a summary count: each rejection needs its own
evidence, decision, action, and reason so another agent can audit the triage.

## Scan tool

`scripts/scan_sessions.py` (stdlib only) — guardian-filtered inventory of codex + claude
transcripts with friction and skill-mention tallies, plus `--dump <id>` to print one clean
transcript. Run it from this skill's own directory, so the same command works from the
source repository and from an installed copy:

```bash
uv run python scripts/scan_sessions.py --help
```
