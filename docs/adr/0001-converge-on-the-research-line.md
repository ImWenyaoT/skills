# 1. Converge the library on the research line

- **Status:** accepted
- **Date:** 2026-08-10

## Context

The library had grown to nineteen skills, then ten, covering agent engineering, document
conversion, skill-library curation, and academic writing. The maintainer's actual work is research
and papers. Several skills existed because they had been written, not because they were reached.

The evidence was in the evals rather than in anyone's opinion. `agent-runtime` held 22 of the
library's positive trigger cases — seven times what `answering-reviewers` had — while the paper
skills, which are the ones used weekly, were the least covered. The eval investment ran opposite to
the work.

## Decision

Five skills, each standing alone:

| Skill | |
|---|---|
| `training-models` | the training is wrong |
| `comparing-runs` | several finished runs have to become one table |
| `writing-papers` | the prose |
| `drawing-figures` | the figures |
| `publishing-papers` | source, packet, and response to reviewers |

Retired: `markdown-pdf` (a one-command job in most runtimes, whose body mostly restated steps a
model already takes), `adversarial-review` (its description required the user to ask for it
explicitly, making it a slash command wearing a skill's frontmatter, and its central read-only rule
lived in prose where nothing enforced it), `agent-runtime` (product engineering that happened to be
about agents), and `curating-skills` (it decided what enters a library now small enough to hold in
one head; by its own rule that a skill must earn its place from repeated evidence, it stopped
earning its own).

Merged into `publishing-papers`: `journal-articles`, `journal-submissions`, and
`answering-reviewers`. They were three things to remember for one stretch of work — a revision
decision fires all three at once — and three rules were being stated more than once across them:
establish the publisher first, the precedence ladder, and page limits judged against the two-column
PDF.

`comparing-runs` was added rather than retired: the layer between a run that works and a claim a
paper can make had no owner, and the repository had already written that down and lost it. The
entry on incomparable ablation arms in `training-models`' checklist says of itself that no gate
covers it and that it is the most expensive defect in the file — and no route in that skill reached
it.

## Consequences

The skills are not a pipeline and must not become one. Each is worth installing alone, which is why
the README index is keyed on the problem in front of you rather than on a position in a sequence,
and why the marketplace manifest lists one plugin per skill instead of bundling them.

A merged skill has a broader description, and a broader description matches any one prompt less
sharply. `publishing-papers` needs 61 metadata tokens where `drawing-figures` needs 30. That
dilution is real for a semantic router too, not an artefact of the lexical smoke.

Retiring a skill retires its goldens. Ten went with the first two retirements and twenty-nine with
the second; a case labelled with a skill that no longer exists cannot be evaluated at all.

Do not resurrect a retired skill without confirming first. Each of these was a decision, not a gap.
