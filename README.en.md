# Agent Skills

[简体中文](README.md) | [English](README.en.md)

[![validate-skills](https://github.com/ImWenyaoT/skills/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/ImWenyaoT/skills/actions/workflows/validate-skills.yml)

A composable collection of Agent Skills maintained by Tian Wenyao for Codex, Claude Code, and other
tools compatible with the [Agent Skills](https://agentskills.io) specification.

The skills come from real workflows and emphasize predictable processes, explicit completion
criteria, and progressive disclosure. Every skill is selected by the model when its task-specific
trigger matches, keeps a boundary that does not overlap its neighbours, and installs on its own.

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
npx skills add . --skill publishing-papers
```

## Skills

These skills are **not a pipeline** and do not depend on each other. Install whichever one
matches the problem in front of you.

| Skill | When to reach for it |
|---|---|
| [`training-models`](skills/training-models) | The training is wrong: loss will not fall, accuracy stalls, gradients blow up, train and eval disagree. |
| [`writing-papers`](skills/writing-papers) | Draft, review, or polish the prose of a technical paper. |
| [`drawing-figures`](skills/drawing-figures) | Plan and produce publication-grade figures. |
| [`publishing-papers`](skills/publishing-papers) | Everything after the science is settled: the journal's manuscript source and local build, the upload packet, and the point-by-point response to reviewers. |

## Design principles

- One directory containing `SKILL.md` is one installable skill; scripts, references, and assets stay
  co-located with it.
- Each skill is self-contained: it references no other skill, so sharing it alone still works.
- Each skill keeps a precise description, its own completion criteria, and a single source of truth.
- Split only disciplines with an independent trigger or genuine reuse across workflows; disclose local
  branches through `references/` instead.

## Repository layout

```text
skills/<name>/SKILL.md     # Installable skills
evals/trigger_cases.json   # Trigger-boundary golden cases
scripts/                   # Repository validation tools
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
coverage on 3.13, and separately verifies that the official `skills` CLI discovers all 4 skills.

Installed skills are managed by `npx skills`. After publishing new commits, run
`npx skills@latest update -g` to update the global installation.

## License

[MIT](LICENSE)
