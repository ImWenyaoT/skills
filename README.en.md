# Agent Skills

[简体中文](README.md) | [English](README.en.md)

[![validate-skills](https://github.com/ImWenyaoT/skills/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/ImWenyaoT/skills/actions/workflows/validate-skills.yml)

A composable collection of Agent Skills maintained by Tian Wenyao for Codex, Claude Code, and other
tools compatible with the [Agent Skills](https://agentskills.io) specification.

The skills come from real workflows and emphasize predictable processes, explicit completion
criteria, and progressive disclosure. The collection has two layers:

- **Orchestrator skills** are invoked explicitly by the user and compose lower-level disciplines.
- **Discipline skills** are selected by the model when their task-specific trigger matches.

## Install

Browse and install with the official [`skills`](https://skills.sh) CLI:

```bash
# List every skill in this repository
npx skills add ImWenyaoT/skills --list

# Select skills interactively
npx skills add ImWenyaoT/skills

# Install one skill globally for Codex
npx skills add ImWenyaoT/skills --skill writing-papers -g -a codex -y

# Install the complete collection
npx skills add ImWenyaoT/skills --all
```

Validate or install from a local checkout:

```bash
npx skills add . --list
npx skills add . --skill answering-reviewers
```

## Skills

### Agent engineering

| Skill | Purpose |
|---|---|
| [`agent-runtime`](skills/agent-runtime) | Bounded agent loops, tool policy and approval gates, async scoring, session/trace persistence, and legacy-lane deletion gates. |
| [`adversarial-review`](skills/adversarial-review) | Dispatch an independent read-only subagent for final verification. |

### Academic papers

| Skill | Purpose |
|---|---|
| [`writing-papers`](skills/writing-papers) | Draft, review, and polish technical papers. |
| [`answering-reviewers`](skills/answering-reviewers) | Implement reviewer comments as a spec and render the revision board. |
| [`drawing-figures`](skills/drawing-figures) | Plan and produce publication-ready figures. |
| [`journal-articles`](skills/journal-articles) | Maintain a reproducibly compiled `elsarticle` or `IEEEtran` manuscript. |
| [`journal-submissions`](skills/journal-submissions) | Build and verify an Elsevier or IEEE submission packet. |

### Machine learning and documents

| Skill | Purpose |
|---|---|
| [`training-models`](skills/training-models) | Build, review, and debug neural-network training workflows. |
| [`markdown-pdf`](skills/markdown-pdf) | Convert Markdown into a polished printable PDF. |

### Skill maintenance

| Skill | Purpose |
|---|---|
| [`curating-skills`](skills/curating-skills) | Decide whether a candidate capability enters the library, whether it was mined from sessions or written by someone else. |

## Design principles

- One directory containing `SKILL.md` is one installable skill; scripts, references, and assets stay
  co-located with it.
- Orchestrators set `disable-model-invocation: true`, compose disciplines, and do not duplicate their rules.
- Discipline skills keep precise descriptions, their own completion criteria, and a single source of truth.
- Split only disciplines with an independent trigger or genuine reuse across workflows; disclose local
  branches through `references/` instead.

## Repository layout

```text
skills/<name>/SKILL.md     # Installable skills
evals/trigger_cases.json   # Trigger-boundary golden cases
scripts/                   # Repository validation and synchronization
docs/research/             # Design audits and research notes
```

`skills/` is an official collection directory supported by
[`npx skills`](https://github.com/vercel-labs/skills). The CLI discovers every first-level child
containing a valid `SKILL.md`.

## Maintain

```bash
# Full local equivalent of CI (requires matplotlib and Pillow)
./scripts/ci.sh

# Core repository-script branch coverage, minimum 70%
./scripts/coverage.sh

# Official installer discovery
npx skills@latest add . --list
```

GitHub Actions runs repository and bundled skill tests on Python 3.11 and 3.13, enforces branch
coverage on 3.13, and separately verifies that the official `skills` CLI discovers all 19 skills.

Run `./scripts/sync-to-local.sh` if you still maintain local mirrors. This repository remains the
single source of truth; installed directories are mirrors.

## License

[MIT](LICENSE)
