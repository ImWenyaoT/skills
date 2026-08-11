# Context

The vocabulary this repository runs on. Each term means one thing here; use it as written rather
than reaching for a synonym, because several of these words are load-bearing in checks and in
skill prose at the same time.

This is a glossary, not a second copy of the rules. Where a term carries a rule, the entry says
where the rule lives.

## The library

**Skill** — one directory under `skills/` holding a `SKILL.md`, plus optional `scripts/`,
`references/`, and `assets/`. It is the unit of installation: a user installs a skill, not the
repository.

**Self-contained** — a skill references no other skill, so sharing it alone still works. This is
the first golden rule; boundaries are expressed by describing behaviour ("does not handle X"),
never by naming a sibling. See `docs/development.md`.

**Description** — the frontmatter field a router reads before loading anything. It is not a summary
of the skill; it answers *when to use this*. It is also the only part of a skill that costs context
on every turn.

**Anti-scope** — the clause of a description that says what the skill is not for ("Do not use
for …", "Does not apply to …"). It is scored separately from the attracting half, because a bag of
words cannot represent negation and its terms would otherwise pull the skill toward the prompts it
excludes.

**Shipped script** — Python under `skills/*/scripts/`. It installs onto other people's machines,
so it guards its third-party imports and names uv, pip and conda when one is missing. Contrast with
`scripts/` at the repository root, which is tooling that never leaves here.

## Evaluation

**Trigger case** (also **golden**) — one labelled prompt in `evals/trigger_cases.json`: which
skills it should reach, which it must not, and which split it belongs to.

**Split** — every trigger case is `train` or `validation`, 60/40. Descriptions are revised against
train failures only; validation answers whether a revision generalised.

**Hard negative** — a forbidden case that shares vocabulary with the skill but needs something
else. A negative sharing no words with the skill tests nothing.

**Abstain case** — a trigger case where the right behaviour is to fire no skill at all.

**`TIE_RATIO`** — 0.80. Above it, two skills' scores are too close for the lexical smoke to render
a verdict, so it renders none. Calibrated from this library's correctly routed cases.

**`VALIDATION_FLOOR`** — 0.85. The validation half is graded as a pass rate against this floor
rather than case by case, because grading it case by case would force you to read which case failed,
and reading it is what turns the held-out half into more training data.

## Verification

**Blocked**, and **exit code 2** — the check could not run, as opposed to running and failing. A
missing `pdfinfo`, `latexmk`, or Python package blocks; it never passes quietly and never counts as
a failure of the thing being checked.

**The three layers** — `tests/` verifies the repository's own tooling, `evals/` verifies that
descriptions reach the right skill, and `skills/<name>/tests/` verifies the scripts that ship. Only
the third one travels to a user. See `docs/development.md`.

## Skill vocabulary

These words are defined inside one skill and mean exactly this when they appear:

**Gate** (`training-models`) — the evidence that permits entry to the next stage. A gate is open or
shut; a check that cannot decide reports `not_applicable` rather than a pass.

**Arm** (`comparing-runs`) — one configuration in an ablation matrix. Arms are *comparable* when
they differ only in the thing under study.

**Method figure** (`drawing-figures`) — a figure with no data behind it: the architecture, or one
module's mechanism. Made through an image model and traced by hand.

**Result figure** (`drawing-figures`) — a figure produced by Python running over experiment
artifacts. Its correctness question is whether the pixels came from the run they claim to.

**The ask is the spec** (`publishing-papers`) — a reviewer comment is a work item to implement, not
a proposition to evaluate.

**Precedence** (`publishing-papers`) — the ranking of conflicting instruction sources: the decision
letter, then the live submission screen, then the guide, then publisher-wide policy. Your own notes
about a source hold no rank.
