# Information Hierarchy Audit

## Purpose

Answer GitHub issue #2: using the shared skill quality rubric, identify which
skills put always-needed instructions, branch-specific procedure, references,
external pointers, and completion criteria at the wrong disclosure level.

This audit does not rewrite the skills. It supplies the priority list for later
rewrite work.

## Rubric Used

The source rubric is `docs/research/skill-quality-rubric.md`, especially
"Progressive Disclosure And Information Hierarchy":

- `SKILL.md` should contain only what every relevant run needs immediately.
- Branch-specific or heavy reference material should sit behind reliable
  context pointers.
- Reference files should be one level deep and long references need a
  `## Contents` section.
- Pointer wording should tell the agent when to open each file.
- Related definitions, caveats, rules, and completion criteria should be
  co-located.

## Method

Checks performed:

- Counted every `SKILL.md` and `references/*.md` file by line count.
- Checked long references for `## Contents`.
- Scanned `SKILL.md` files for `references/`, `scripts/`, `sample_codes/`,
  and archive path pointers.
- Sample-read the largest skills and the most reference-heavy skills.
- Verified whether referenced archived paper-pipeline material exists in this
  repository.

## Must Fix

### `drawing-figures`

`drawing-figures/SKILL.md` is the clearest hierarchy problem. At 326 lines, it
keeps a correct top-level two-phase shape, but then inlines most of the
branch-specific script manual:

- Phase A lists four budget scripts with full command blocks and outputs.
- Phase B inlines detailed command snippets and Python/JSON examples for
  `diagram_primitives.py`, `figkit`, `stitch.py`, `measure_model.py`, and
  `annotate_renders.py`.
- `Typical Workflow` repeats many of the same script invocations after the
  detailed sections.

The always-needed material is much smaller: scope, the two-phase router, the
figure design system, the caption/reference pointers, and final completion
criteria.

Recommended rewrite:

- Keep `SKILL.md` as a short router:
  - when to run Phase A vs Phase B;
  - non-negotiable figure design system;
  - what counts as done;
  - links to the RGB-T reference data.
- Move budget-script usage into `references/budget-workflow.md`.
- Move draw-script usage and examples into `references/figure-script-reference.md`
  or `references/draw-workflow.md`.
- Delete or shrink `Typical Workflow` after the references exist, so commands
  have one canonical home.

### `elsevier-submissions`

`elsevier-submissions/SKILL.md` points to
`docs/_archive/paper-pipeline/knowledge-work-half/` as reusable authority for
the playbook, templates, checklist, guides, tools, and journals registry.
That path is absent from the current repository.

This is a pointer reliability issue, not just a length issue. A skill that says
"read these first" must point to material the agent can actually read, or it
will either stop, ask the user, or reconstruct missing process from memory.

Recommended rewrite:

- Either vendor the required archived files into this skill's own
  `references/` and `scripts/` folders, or replace the archive dependency with
  a clear "ask the user for the project-local paper pipeline path" branch.
- Keep only durable packaging invariants inline: statement order, hard specs
  to verify live, single-vs-double-column strategy, source-zip constraints, and
  final checklist.
- Treat `scripts/md_to_docx.py` as the only currently reliable local script
  pointer in this skill unless the archived pipeline is restored.

## Worth Fixing

### `training-models`

`training-models/SKILL.md` is usable, but it mixes three layers in the same
file:

- every-run discipline and stack assumptions;
- the full 6-stage training recipe;
- the 14-item bug checklist, quick-start sample pointers, and a "Learn More"
  external search table.

The skill already has `references/karpathy-recipe.md` and
`references/checklist.md`, so the hierarchy can be tightened without changing
behavior.

Recommended rewrite:

- Keep the first-response decision rule inline: "from-scratch setup uses the
  recipe; broken training uses the checklist; always establish minimal repro,
  sanity checks, and the first failing invariant."
- Keep only the highest-signal sanity checks inline:
  - init loss;
  - input-independent baseline;
  - overfit one batch;
  - train/eval/zero-grad/logits contract;
  - data/normalization leak checks.
- Move the full stage-by-stage recipe and full 14-row checklist to references,
  or keep the current references as canonical and make the inline tables
  shorter.
- Move "Learn More" out of the hot path; it is reference lookup guidance, not
  action guidance for every run.

### `mining-sessions`

`mining-sessions/SKILL.md` is not currently broken, but it is near the point
where operational path tables, extraction workflow, placement rules, and common
mistakes compete for attention.

Recommended rewrite only if it grows:

- Keep the extraction loop and final artifact standard inline.
- Move runtime path inventory and sync/placement details to
  `references/runtime-paths.md`.
- Move recurring mistake patterns to `references/common-mistakes.md`.

## Accept / Keep As Pattern

### `apple-hig`

`apple-hig/SKILL.md` is the best current model for progressive disclosure in
this repo:

- It has an explicit "How this skill loads" section.
- It separates always-true non-negotiables from topic-specific references.
- It uses a routing index to decide which reference to open.
- Review mode co-locates mechanical audit, judgment pass, and completion
  criteria.

Use this structure as the pattern for complex reference-heavy skills.

### `writing-resumes`

`writing-resumes/SKILL.md` is a healthy compact skill. Core writing techniques
stay inline, while verb lists, worked examples, checklist, and layout guidance
live in references. The final self-check points to the right reference material
without overloading the hot path.

### `writing-papers`

`writing-papers/SKILL.md` combines drafting and review branches, but the
information hierarchy is acceptable for now. The branch boundary is visible,
full frameworks and output modes are behind reference pointers, and completion
criteria are local to the work modes.

Potential future invocation/scope questions belong to the invocation audit, not
this hierarchy audit.

## No Immediate Action

Smaller workflow skills such as `agent-loops`, `agent-evals`,
`adversarial-review`, `bridging-legacy`, `importing-skills`, `markdown-pdf`,
`persisting-traces`, `spec-first`, and `tool-policies` are short enough that
their hierarchy is not the current constraint. They may still need invocation
or outcome-quality work in later audits.

## Decision

Prioritize information hierarchy fixes in this order:

1. `drawing-figures`: split script manuals and examples out of `SKILL.md`.
2. `elsevier-submissions`: repair or vendor missing archive pointers.
3. `training-models`: shorten the hot path and move lookup material out.
4. `mining-sessions`: split references only if future edits make it longer.

