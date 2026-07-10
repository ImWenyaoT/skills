# Runtime paths and placement

Read this reference before scanning transcripts or deciding where a mined skill belongs.

## Transcript and skill locations

| What | Location | Note |
|---|---|---|
| Codex transcripts | `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` | Full conversations. |
| Guardian noise | `session_meta.payload.source.subagent.other == "guardian"` | Exclude these safety-judge sessions or friction counts become meaningless. |
| Claude pointers | `~/.claude/sessions/*.json` | Process metadata only; never scan these for conversation content. |
| Claude transcripts | `~/.claude/projects/<slugified-cwd>/*.jsonl` | Full conversations. |
| Codex user skills | `~/.agents/skills/<name>/SKILL.md` | Cross-runtime user skills. |
| Codex repo skills | `$CWD/.agents/skills/`, `$REPO_ROOT/.agents/skills/` | Project or organization scope. |
| Claude user skills | `~/.claude/skills/<name>/SKILL.md` | User scope. |
| Claude project skills | `<project>/.claude/skills/<name>/SKILL.md` | Project scope. |
| Legacy staging | Non-standard personal directories | Migrate useful skills to the source repo, then remove duplicates. |
| Installed packs | Third-party skill collections | Read-only: mine patterns, never edit or republish. |

Verify paths before scanning because runtime versions can use additional locations such as
`~/.codex/skills/`. Separate authored skills from installed packs before editing anything.

## Placement and cross-runtime copies

- Keep the version-controlled skills repository as the source of truth. Install copies into
  runtime directories only when the user explicitly requests it.
- Use project scope only for skills whose meaning is specific to that project; otherwise use
  user scope.
- Codex and Claude do not read each other's skill trees. To serve both, copy the entire skill
  directory into both trees. Prefer a plain copy or runtime hook over symlinks or a sync daemon.
- Keep one directory per skill with `SKILL.md` plus its scripts, references, and assets.

## Common mistakes

- Counting friction without filtering guardian subagents.
- Grepping Claude pointer files instead of `~/.claude/projects/` transcripts.
- Creating a skill from one session without repeated evidence.
- Duplicating a live tool instead of pointing the skill at it.
- Editing installed or vendored packs instead of authored skills.
