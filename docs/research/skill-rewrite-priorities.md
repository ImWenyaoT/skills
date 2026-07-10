# Skill Rewrite Priorities

## Purpose

Answer GitHub issue #3: after the rubric and audits resolve, decide which
skill-quality changes should be implemented first.

This is the handoff map from wayfinding into implementation. It does not make
the rewrites itself.

## Inputs

- `docs/research/skill-quality-rubric.md`
- `docs/research/audit-information-hierarchy.md`
- `docs/research/audit-invocation-descriptions.md`
- `docs/research/audit-trigger-eval-coverage.md`
- `docs/research/audit-completion-determinism.md`

## Priority Principles

Prioritize a change when it:

- blocks reliable execution today;
- appears in more than one audit dimension;
- must happen before safe description rewrites;
- reduces token/context load without weakening routing;
- creates verification evidence for later rewrites.

Do not prioritize work that only makes prose nicer, duplicates a lower-risk
cleanup, or belongs to maintenance infrastructure rather than skill content.

## Recommended Implementation Order

### 0. Add route-eval guardrails before broad description edits

Type: eval expansion.

Why first:

The trigger suite is structurally healthy, but several planned description
edits need targeted protection before they are safe.

Scope:

- Add Chinese `drawing-figures` positive and Chinese caption-only hard negative.
- Add resume PDF/layout-only forbidden cases for `writing-resumes`.
- Add generic cover-letter and non-packet negatives for `elsevier-submissions`.
- Add non-paper LaTeX / academic-adjacent abstain negatives for
  `writing-papers`.
- Add a Chinese `markdown-pdf` positive.
- Run `evaluate_skill_triggers.py` after the case additions.

Optional but recommended before broad metadata changes:

- Run `route_with_llm.py` and score with
  `evaluate_skill_triggers.py --predictions`.

Not included:

- Full outcome evals. Those are separate work below.

### 1. Repair `elsevier-submissions`

Types: reference restructuring, small description edit, deterministic support.

Why this is first among skill rewrites:

`elsevier-submissions` has the clearest correctness blocker. Its authoritative
archive path and final-check checklist are missing from this repo, so the skill
cannot execute its own definition of done.

Scope:

- Vendor the needed paper-pipeline checklist/playbook/templates into this
  skill's `references/` folder, or replace the missing archive dependency with
  an explicit user-provided project path branch.
- Rewrite the final check so it is local and executable:
  - current EM step identified;
  - required statements present and ordered;
  - live journal limits checked;
  - source zip, when required, unzips cleanly and compiles standalone;
  - side-material DOCX outputs generated and inspected.
- Add anti-scope and Chinese triggers in the description:
  `Elsevier 投稿`, `修回稿`, `投稿材料`, `Editorial Manager`, `源码 zip`.
- Add a tiny smoke for `scripts/md_to_docx.py` using a Markdown fixture.

Verification:

- `uv run python scripts/validate_skills.py`
- `uv run python scripts/evaluate_skill_triggers.py`
- `uv run python -m py_compile elsevier-submissions/scripts/md_to_docx.py`
- A fixture run proving `md_to_docx.py` writes a `.docx`.

### 2. Restructure `drawing-figures`

Types: reference restructuring, eval expansion, deterministic support, small
description edit.

Why second:

`drawing-figures` has the largest `SKILL.md` and the heaviest script surface.
It is useful, but the hot path is buried under command manuals and examples.
It also needs Chinese trigger coverage before adding Chinese description terms.

Scope:

- Split script manuals out of `SKILL.md`:
  - `references/budget-workflow.md`
  - `references/figure-script-reference.md` or `references/draw-workflow.md`
- Keep inline:
  - phase router;
  - figure design system;
  - final figure evidence criteria;
  - pointers to RGB-T references.
- Add Chinese trigger phrasing to the description after eval guards exist.
- Add script smoke fixtures for the most deterministic scripts:
  - `stitch.py`;
  - `annotate_renders.py`;
  - budget scripts where tiny fixtures are practical.
- Require final evidence for figure outputs: artifact path, format/DPI or vector
  status, font/palette check, and paper-text/caption linkage.

Verification:

- Existing skill validation and trigger evals.
- Script smoke commands over fixture inputs.
- `py_compile` over `drawing-figures/scripts/*.py`.

### 3. Prune and protect `writing-papers`

Types: small description edit, eval expansion, outcome eval expansion.

Why third:

`writing-papers` is broadly useful and already has good information hierarchy,
but its description is the longest and broadest in the repo. It also handles
subjective, high-impact outputs where route-level evals cannot prove quality.

Scope:

- Prune the description:
  - keep one trigger per branch;
  - front-load academic paper drafting/review and Chinese equivalents;
  - keep only core branches: structure/draft, argument/evidence consistency,
    AI-tone/language polish for papers, rebuttal/redline;
  - add anti-scope for generic English editing, blog/README drafting,
    non-paper LaTeX, standalone figure production, and submission packaging.
- Add trigger negatives:
  - non-paper LaTeX;
  - academic bio;
  - generic academic-adjacent writing that is not a paper.
- Add outcome fixtures:
  - LaTeX polish preserves `\cite`, `\ref`, formulas, labels, and meaning;
  - final redline emits pass text when no substantive issue exists;
  - experiment analysis cites only supplied data;
  - review findings include location, risk, and concrete fix.

Verification:

- Trigger evals before and after description rewrite.
- LLM router scored with predictions for the broad metadata change.
- Outcome fixture grader(s) for the highest-risk modes.

### 4. Tighten `training-models`

Types: small description edit, reference restructuring.

Why fourth:

`training-models` has strong diagnostic completion criteria and sample code, so
it is not broken. Its main issue is hot-path density and missing Chinese trigger
phrasing in the description.

Scope:

- Add Chinese trigger phrases: `loss 不下降`, `acc 卡住`, `过拟合单 batch`,
  `训练循环`, `train/eval`, `zero_grad`, `logits`.
- Shorten non-trigger stack detail in the description.
- Keep only highest-signal sanity checks inline:
  - init loss;
  - input-independent baseline;
  - overfit one batch;
  - train/eval/zero-grad/logits contract;
  - data/normalization leak checks.
- Move or defer full stage/checklist material to references.
- Optionally add sample-code smoke for `sanity_check.py`.

Verification:

- Trigger evals.
- `py_compile` sample code.
- Optional minimal sample-code execution if dependency availability allows.

### 5. Patch `writing-resumes`

Types: small description edit, eval expansion.

Why fifth:

`writing-resumes` is already a compact and healthy skill. It needs localized
metadata/eval hardening, not a rewrite.

Scope:

- Add Chinese trigger phrasing: `简历`, `经历 bullet`, `量化成果`,
  `匹配 JD`, `一页`, `技能栏`.
- Add trigger negatives for resume PDF/layout-only prompts.
- Preserve the existing anti-scope against academic bios, submission cover
  letters, and PDF-only export/layout.

Verification:

- Trigger evals.
- No reference restructuring required unless later edits make the body grow.

### 6. Normalize `mining-sessions`

Types: small structural cleanup, possible reference restructuring.

Why sixth:

The completion model is good, but deterministic support is oddly placed and the
skill is close to accumulating too much operational path detail.

Scope:

- Move `scan_sessions.py` to `mining-sessions/scripts/scan_sessions.py`, or
  explicitly document why it intentionally lives at the skill root.
- Make the final report schema explicit:
  - candidate;
  - evidence count/session ids;
  - decision (`skill` / `memory` / `neither`);
  - action taken;
  - rejected reason.
- If the body grows, split runtime path inventory into
  `references/runtime-paths.md` and common mistakes into
  `references/common-mistakes.md`.
- Add optional Chinese positive trigger if this workflow is commonly invoked in
  Chinese.

Verification:

- `uv run python mining-sessions/scan_sessions.py --help` or updated path.
- Trigger evals if description changes.

### 7. Decide `markdown-pdf` determinism

Types: deterministic support or stricter checklist, eval expansion.

Why seventh:

The skill is well scoped, but output quality depends on whatever renderer the
agent picks.

Scope:

- Either bundle a small deterministic Markdown-to-HTML template plus known PDF
  print path, or keep the skill tool-agnostic and strengthen the output
  checklist.
- Add a Chinese Markdown-to-PDF positive trigger.
- Add an outcome fixture with headings, table, and fenced code block if a
  deterministic render path is chosen.

Verification:

- Trigger evals.
- If bundled: fixture render proving HTML and PDF artifacts are produced.

### 8. Dedupe `agent-loops` metadata

Type: small description edit.

Why later:

The skill is otherwise sound. The issue is duplicated trigger wording in a
metadata field, not execution correctness.

Scope:

- Collapse the repeated "Use for" vocabulary while preserving boundaries
  against `tool-policies`.

Verification:

- Trigger evals, especially `agent-loops` versus `tool-policies`.
- LLM router only if the description change is larger than expected.

## Defer

No immediate rewrite needed:

- `apple-hig`: keep as the pattern for progressive disclosure plus mechanical
  smoke and judgment reconciliation.
- `adversarial-review`: completion criterion and scope are narrow enough.
- `agent-evals`: route coverage and completion criteria are adequate for now.
- `bridging-legacy`: minimal but sufficient.
- `importing-skills`: good boundary against `mining-sessions`.
- `persisting-traces`: good boundary against `agent-evals`.
- `spec-first`: useful docs-backed gate; add Chinese trigger only if needed.
- `tool-policies`: keep as-is unless `agent-loops` dedupe changes routing.

## Out Of Scope For This Map

These items should not be done as part of the skill-quality rewrite map:

- Refactoring `SkillCatalog`, `BundleInventory`, local sync, or other
  maintenance infrastructure modules.
- Reworking `validate_skills.py`, `evaluate_skill_triggers.py`,
  `route_with_llm.py`, or CI architecture, except for normal use of those
  scripts during verification.
- Implementing actual skill rewrites inside the wayfinding phase.
- Versioning LLM router prediction JSONL by default; keep predictions in
  `.cache/` unless there is an explicit policy decision to preserve snapshots.

## Handoff Shape

The next phase should not be one broad "fix skills" ticket. Split it into small
implementation issues in this order:

1. Add trigger eval guardrails.
2. Repair `elsevier-submissions`.
3. Restructure `drawing-figures`.
4. Prune/protect `writing-papers`.
5. Tighten `training-models`.
6. Patch `writing-resumes`.
7. Normalize `mining-sessions`.
8. Decide `markdown-pdf` deterministic rendering.
9. Dedupe `agent-loops` metadata.

After the trigger guardrails and any broad description rewrite, run both the
offline trigger contract and an LLM-router scoring pass.

