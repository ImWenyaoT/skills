# Agent Skills

A personal Agent Skills library. Every skill is a self-contained folder under `skills/`
(`SKILL.md` plus optional `scripts/`, `references/`, `assets/`), loaded by progressive
disclosure: name and description at startup, the full `SKILL.md` on a match, bundled files
on demand.

**Before changing anything here, read [`docs/development.md`](docs/development.md)** — the
golden rules, naming and description conventions, the three layers of checks, the trigger-test
contract, and how to add or modify a skill. `CLAUDE.md` is a symlink to this file, so both
runtimes read the same rules.

## Agent skills

### Issue tracker

Issues are tracked in this repository's GitHub Issues. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the five default canonical triage labels. See `docs/agents/triage-labels.md`.

### Domain docs

Use the single-context layout. See `docs/agents/domain.md`.
