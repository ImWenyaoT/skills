# Completion Criteria And Determinism Audit

## Purpose

Answer GitHub issue #6: using the shared skill quality rubric, identify which
skills lack checkable completion criteria or deterministic support.

This audit does not rewrite skills. It decides where later implementation work
needs sharper "done" criteria, scripts, fixtures, smoke tests, or outcome evals
before skill rewrites should be trusted.

## Rubric Used

The source rubric is `docs/research/skill-quality-rubric.md`, especially:

- "Steps And Completion Criteria": each step should end in a checkable
  completion criterion, critical criteria should prevent premature completion,
  and the skill should say what evidence proves the work is done.
- "Specificity And Determinism": scripts should solve concrete deterministic
  subproblems, dependencies/runtime assumptions should be explicit, and
  intermediate outputs should be verifiable.
- "Eval Coverage": route-level trigger evals are not enough when success
  depends on following the loaded skill correctly.

## Method

Checks performed:

- Scanned every `SKILL.md` for `Done means`, `Final check`, `Self-check`,
  `verify`, `checklist`, `scripts/`, and `uv run` signals.
- Inventoried bundled scripts, references, and sample code.
- Sample-read the high-risk skills: `elsevier-submissions`, `drawing-figures`,
  `writing-papers`, `apple-hig`, `training-models`, `writing-resumes`,
  `mining-sessions`, `agent-loops`, `agent-evals`, and `tool-policies`.
- Ran a syntax-level script smoke with `uv run python -m py_compile` over repo
  scripts, skill scripts, `mining-sessions/scan_sessions.py`, and
  `training-models/sample_codes/**/*.py`.

## Current State

Most skills do include some completion language. The problem is not total
absence of "done" criteria. The problem is uneven evidence quality:

- Some skills have checkable criteria and deterministic scripts.
- Some have a good criterion but no local script/fixture/eval to prove it.
- One key skill has a final check that points to files missing from this repo.
- Subjective writing/review skills need outcome evals or stronger output
  contracts because route-level trigger evals cannot prove they follow the
  loaded skill.

## Must Fix

### `elsevier-submissions`

This is the highest-risk completion issue.

Evidence:

- The skill says reusable playbook/templates/CLI survive under
  `docs/_archive/paper-pipeline/` (`elsevier-submissions/SKILL.md:13-15`).
- It names `docs/_archive/paper-pipeline/knowledge-work-half/` as the reusable
  authority for playbook, templates, checklists, guides, and tools
  (`elsevier-submissions/SKILL.md:22-25`).
- Its final check says to walk `checklist_initial.md` or `checklist_revision.md`
  under that same archive before declaring ready
  (`elsevier-submissions/SKILL.md:80-84`).
- Earlier information-hierarchy audit verified that this archive path is absent
  from the current repository.

Why it matters:

The completion criterion is directionally good: the packet must match the
current EM step, not just a generic author guide. But the criterion is not
currently executable because its authoritative checklist is missing. The agent
can still perform parts of the workflow from inline rules, but it cannot prove
the final check the skill asks it to perform.

Recommended rewrite:

- Vendor the required checklist/playbook/templates into this skill's own
  `references/` folder, or change the workflow to require a user-provided
  project-local paper-pipeline path.
- Make the final check local and explicit:
  - current EM step identified;
  - required statements present and ordered;
  - live journal limits checked;
  - single-column manuscript PDF generated when appropriate;
  - source zip, when needed, unzips cleanly and compiles standalone;
  - DOCX side materials generated and inspected.
- Add a script smoke for `scripts/md_to_docx.py` using a tiny Markdown fixture
  and verifying a `.docx` output exists.

## Worth Fixing

### `drawing-figures`

`drawing-figures` has the strongest deterministic support in the repo by file
count: eight bundled scripts plus reference data. It also has checkable output
criteria in places.

Evidence:

- Phase A says the four budget scripts are done when outputs record section
  word counts, figure/table counts, palette, caption patterns, or missing
  corpus artifacts (`drawing-figures/SKILL.md:31-35`).
- It lists concrete script invocations for budget, stitching, measurement, and
  QA annotation (`drawing-figures/SKILL.md:41-87`,
  `drawing-figures/SKILL.md:191-278`).
- The final workflow says each final figure needs the requested source artifact,
  600 dpi raster or vector export, fonts/palette checked against the design
  system, and a caption/finding matching the paper text
  (`drawing-figures/SKILL.md:301-326`).

Why it matters:

The deterministic pieces exist, but there is no script-level smoke suite or
fixture contract. For a script-heavy skill, `py_compile` is too weak; it only
proves imports/grammar. It does not prove that `stitch.py` creates the expected
image, that extraction scripts write stable output shapes, or that
`annotate_renders.py` handles a minimal config.

Recommended rewrite:

- After the information-hierarchy split, add `references/script-smoke.md` or
  a test fixture directory describing minimal inputs/outputs for each script.
- Add smoke tests for:
  - `stitch.py` with two tiny generated PNGs;
  - `annotate_renders.py` with one tiny image and one anchor;
  - `section_wordcount.py` / caption extraction on a small text/PDF fixture if
    feasible;
  - `measure_model.py` helper return shapes via a toy `torch.nn.Module` if
    torch is available.
- Make the final criterion require recorded evidence: command output path,
  dimensions/DPI, font/palette check, and paper-text/caption linkage note.

### `writing-papers`

`writing-papers` has rich output contracts but little deterministic support.

Evidence:

- It has a top-level completion criterion for drafting and review
  (`writing-papers/SKILL.md:30`).
- It lists concrete review actions for language, logic, figure/table linkage,
  word count, LaTeX preservation, and evidence-bound claims
  (`writing-papers/SKILL.md:60-67`).
- It defines severity labels P0/P1/P2 and warns not to inflate ordinary taste
  preferences (`writing-papers/SKILL.md:101-107`).
- Its self-check is a dense list of questions rather than a graded outcome
  (`writing-papers/SKILL.md:109-113`).

Why it matters:

This is a subjective writing/review skill. Scripts are not the right answer for
most of it, but route-level trigger evals cannot prove that the agent:

- marks missing facts as `[作者补充]`;
- preserves equations/citations/labels in LaTeX;
- does not fabricate claims;
- classifies P0/P1/P2 correctly;
- follows the requested output mode.

Recommended rewrite:

- Add outcome eval fixtures for the highest-risk modes:
  - LaTeX polish must preserve `\cite`, `\ref`, formulas, labels, and meaning;
  - final redline must output pass text when no substantive issue exists;
  - experiment analysis must cite only supplied data;
  - review findings must include location, risk, and concrete fix.
- Convert the final self-check into mode-specific output requirements, not just
  questions.
- Keep scripts out unless a narrow deterministic helper emerges; this skill
  needs graders and fixtures more than automation.

### `mining-sessions`

`mining-sessions` has a strong evidence-based completion criterion but its
deterministic helper sits outside the usual `scripts/` convention.

Evidence:

- The workflow requires scanning, clustering, triage, merge-before-create,
  authoring, and reporting (`mining-sessions/SKILL.md:38-51`).
- Done means every created/updated skill cites repeated session evidence and
  every rejected candidate is classified as skill, memory, or neither
  (`mining-sessions/SKILL.md:49-51`).
- The scan tool is named as `scan_sessions.py`, with `uv run python
  scan_sessions.py --help` (`mining-sessions/SKILL.md:93-97`).
- The actual file exists at `mining-sessions/scan_sessions.py`, not under
  `mining-sessions/scripts/`.

Why it matters:

The completion criterion is good, but the helper is non-standard for this repo
and easy to miss when auditing skill scripts. The script itself does useful
deterministic work: guardian filtering, path inventory, friction counts, and
dumping clean transcripts. It should be treated as first-class bundled
deterministic support.

Recommended rewrite:

- Move `scan_sessions.py` to `mining-sessions/scripts/scan_sessions.py`, or
  explicitly document why it intentionally lives at the root.
- Add a smoke command to validation or docs: `uv run python
  mining-sessions/scan_sessions.py --help`.
- Make the final report format explicit: candidate, evidence count/session ids,
  decision (`skill` / `memory` / `neither`), action taken, and rejected reason.

### `markdown-pdf`

`markdown-pdf` has a clear output completion criterion but no bundled
deterministic implementation.

Evidence:

- Done means both the HTML artifact and final PDF exist and the PDF opens with
  headings, code blocks, tables, and footer intact (`markdown-pdf/SKILL.md:26-27`).
- Tooling is described as "prefer a renderer plus print/PDF step" with runtime
  helpers or local toolchain (`markdown-pdf/SKILL.md:36-41`).

Why it matters:

The criterion is checkable, but because there is no bundled script/template,
different agents may choose different renderers and produce inconsistent
styling. That may be acceptable if the runtime always provides document
helpers, but this skill is less deterministic than the current wording implies.

Recommended rewrite:

- Either keep it tool-agnostic and add a stricter output checklist, or bundle a
  small Markdown-to-HTML template and a known print path.
- Add an outcome fixture: Markdown with headings, a table, and a fenced code
  block; expected proof is generated HTML plus a PDF smoke/open check.

## Keep As Pattern

### `apple-hig`

`apple-hig` is the best current example of balanced deterministic support.

Evidence:

- It defines a progressive loading path and says review findings are done when
  they state the HIG rule, violated location, and concrete fix
  (`apple-hig/SKILL.md:17-28`).
- Review mode runs a mechanical pass and explicitly scopes the script as a
  smoke test, not a final verdict (`apple-hig/SKILL.md:100-107`).
- It then requires a judgment pass and says done means mechanical and judgment
  findings are reconciled (`apple-hig/SKILL.md:114-119`).

Why it works:

The script improves predictability without pretending to solve the subjective
parts. This is the right shape for skills that combine mechanical checks with
human/agent judgment.

### `training-models`

`training-models` has strong checkable diagnostic criteria.

Evidence:

- Its top-level completion criterion requires minimal repro, key sanity-check
  results, matched pitfall and fix, or a clear statement of the first failing
  step (`training-models/SKILL.md:14`).
- It uses binary-ish gates such as init loss near `log(n)` and overfitting one
  batch (`training-models/SKILL.md:39-43`).
- It includes runnable sample code under `training-models/sample_codes/`.

Recommended follow-up:

- Add a tiny smoke target for the sample code if this skill is edited, but the
  completion model itself is sound.

### `writing-resumes`

`writing-resumes` has a good content-layer completion criterion.

Evidence:

- It declares itself the content layer, excluding layout/PDF work.
- Its self-check points to checklist/layout/verb/method references.
- Done means every edited bullet is honest, non-duplicative, role-relevant, and
  quantified or explicitly left unquantified because no defensible metric exists
  (`writing-resumes/SKILL.md:86-92`).

Recommended follow-up:

- Add outcome fixtures only if the skill is rewritten substantially.

### Runtime architecture skills

`agent-loops`, `agent-evals`, `tool-policies`, `persisting-traces`,
`bridging-legacy`, and `spec-first` generally have usable done criteria:

- `agent-loops`: bounded turn cap, explicit terminal state, cheap intents skip
  retrieval/tools.
- `agent-evals`: non-blocking scoring path, lifecycle statuses, golden export
  matching sample.
- `tool-policies`: low/medium/high/closed policy outcomes covered by tests or
  fixtures.
- `persisting-traces`: structured storage and JSON fallback round-trip
  representative session state.
- `bridging-legacy`: adapter path and fallback path tested or explicitly
  verified.
- `spec-first`: governing docs and code describe the same behavior and
  vocabulary.

These are codebase-specific skills, so deterministic support should live in the
target codebase tests rather than this skill repo.

## Defer

### `adversarial-review`

The completion criterion is narrow and appropriate: unresolved P0/P1 findings
block completion unless fixed, explicitly accepted by the user, or still listed
as blocking. No script is needed.

### `importing-skills`

The adoption checklist is mostly judgment plus provenance/license verification.
Completion is adequate: license/provenance/attribution/adaptation decision are
recorded. Add outcome fixtures only if the skill starts making repeated bad
import decisions.

## Script Smoke Result

The following syntax-level smoke passed:

```bash
env UV_CACHE_DIR=.cache/uv uv run python -m py_compile \
  scripts/evaluate_skill_triggers.py scripts/route_with_llm.py scripts/validate_skills.py \
  apple-hig/scripts/hig_audit.py drawing-figures/scripts/*.py \
  elsevier-submissions/scripts/md_to_docx.py mining-sessions/scan_sessions.py \
  training-models/sample_codes/**/*.py
```

This proves the Python files are syntactically loadable. It does not prove
behavioral correctness for script-heavy skills.

## Decision

Prioritize completion/determinism fixes in this order:

1. `elsevier-submissions`: repair missing final-check authority and make the
   final packet checklist executable.
2. `drawing-figures`: add script-level smoke fixtures and evidence requirements
   for final figures.
3. `writing-papers`: add outcome eval fixtures and mode-specific output
   contracts.
4. `mining-sessions`: normalize or explicitly document the helper script path
   and make the final report schema explicit.
5. `markdown-pdf`: decide whether to bundle a deterministic render path or make
   the tool-agnostic output checklist stricter.

