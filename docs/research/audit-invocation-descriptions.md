# Invocation And Description Audit

## Purpose

Answer GitHub issue #4: using the shared skill quality rubric, identify which
skills have weak invocation mode or description boundaries.

This audit does not edit descriptions. It decides which descriptions should be
rewritten later and what kind of rewrite each one needs.

## Rubric Used

The source rubric is `docs/research/skill-quality-rubric.md`, especially
"Invocation And Description":

- Invocation mode should be intentional.
- Model-invoked skills should earn their context load because the agent, or
  another skill, needs to discover them autonomously.
- `description` should front-load the main trigger words.
- Each distinct trigger branch should appear once.
- Anti-scope should be clear enough to prevent broad accidental firing.
- Chinese trigger phrasing should appear when real users are likely to ask in
  Chinese.

The local reference `writing-great-skills` adds the sharper test: a
model-invoked description is a trigger budget, not a miniature manual. Branch
synonyms should collapse; every word spends context load.

## Method

Checks performed:

- Extracted every skill's `name`, `description`, and `disable-model-invocation`
  flag.
- Measured description lengths and whether descriptions contain Chinese trigger
  phrasing.
- Compared descriptions against `evals/trigger_cases.json` positives,
  forbidden cases, and Chinese positives.
- Ran the trigger contract with the repo-preferred `uv run` command.

## Invocation Mode Decision

No immediate `disable-model-invocation` changes are recommended.

All 16 repo skills are currently model-invoked. That is defensible for this
library because each skill names a capability the agent may need to discover
from ordinary user phrasing: paper writing, resume editing, Markdown PDF export,
agent loops, trace persistence, skill imports, session mining, etc.

Two skills looked most suspicious at first:

- `adversarial-review`, because it only runs on explicitly requested
  independent verification.
- `mining-sessions`, because it is a meta-workflow over local transcripts.

Both should stay model-invoked for now. `adversarial-review` has concrete
natural-language triggers such as "is this actually done" and "read-only
adversarial review". `mining-sessions` has user-realistic triggers such as
"scan my past sessions" and protects itself with an evidence requirement.

Revisit invocation mode only if route traces show these skills firing without
explicit user intent.

## Must Fix

### `writing-papers`

`writing-papers/SKILL.md` has the longest description in the repo at 637
characters. The capability is valuable and should remain model-invoked, but the
description is doing too many jobs at once:

- drafting branch;
- review branch;
- language/AI-tone branch;
- figure-text-table linkage branch;
- LaTeX/caption/rebuttal/redline branch;
- Chinese triggers.

The current description is not merely long; it risks making broad academic-ish
words such as `citations`, `LaTeX polish`, `captions`, and `rebuttals` feel
equally central. The anti-scope only excludes 600 dpi figure production and
Elsevier packaging, leaving generic academic copy-editing and non-paper LaTeX
work less clearly excluded.

Recommended rewrite:

- Keep it model-invoked.
- Front-load "academic paper drafting/review" and the Chinese equivalents.
- Collapse duplicated drafting/review synonyms into one trigger per branch.
- Keep only branches that truly belong:
  - structure/draft;
  - argument/evidence consistency;
  - AI-tone/language polish for papers;
  - rebuttal/redline for manuscripts.
- Add clearer anti-scope for generic English editing, blog/README drafting,
  standalone figure production, and submission packaging.

### `elsevier-submissions`

`elsevier-submissions/SKILL.md` has clear English scope, but the description
lacks anti-scope and lacks Chinese trigger phrasing despite the trigger suite
having a Chinese positive case.

The risky branch is "cover letter" / "defensive-writing/self-citation checks":
without anti-scope, those words can blur into paper-writing or prose-review
work. The skill should trigger only once the manuscript is mature enough for
Editorial Manager packaging.

Recommended rewrite:

- Keep it model-invoked.
- Add Chinese trigger terms such as `Elsevier 投稿`, `修回稿`, `投稿材料`,
  `Editorial Manager`, `源码 zip`.
- Front-load "finished LaTeX manuscript" and "submission packet".
- Add anti-scope for drafting, manuscript language review, figure production,
  and generic cover-letter writing outside an Elsevier submission packet.

## Worth Fixing

### `training-models`

`training-models/SKILL.md` has strong English triggers and good forbidden
coverage against agent evals and generic data pipelines. It is still missing
Chinese trigger phrasing, even though two positive eval cases are Chinese.

Recommended rewrite:

- Keep it model-invoked.
- Add Chinese trigger phrases for `loss 不下降`, `acc 卡住`, `过拟合单 batch`,
  `训练循环`, `train/eval`, `zero_grad`, and `logits`.
- Shorten the stack note in the description if needed; stack details are less
  important for invocation than failure symptoms and discipline triggers.

### `writing-resumes`

`writing-resumes/SKILL.md` is well-bounded in English and has useful anti-scope,
but it lacks Chinese trigger phrasing despite a Chinese positive eval case.

Recommended rewrite:

- Keep it model-invoked.
- Add Chinese trigger terms such as `简历`, `经历 bullet`, `量化成果`,
  `匹配 JD`, `一页`, and `技能栏`.
- Preserve the anti-scope against academic bios, Elsevier cover letters, and
  PDF-only export/layout.

### `drawing-figures`

`drawing-figures/SKILL.md` has good English boundaries against paper writing and
submission packaging. It has no Chinese trigger phrasing and no Chinese trigger
goldens, even though the repo is commonly used through Chinese prompts.

Recommended rewrite:

- Keep it model-invoked.
- Add compact Chinese trigger terms for `论文图`, `架构图`, `600 dpi`,
  `结果拼图`, `效率图`, and `图表预算`.
- Preserve the anti-scope for caption-only edits and submission packaging.

### `agent-loops`

`agent-loops/SKILL.md` is correctly model-invoked, but the description repeats
the same branch shape in two passes: first listing loop concepts, then saying
"Use for" with much of the same vocabulary. That is mild duplication in the
most expensive place: metadata loaded every turn.

Recommended rewrite:

- Keep it model-invoked.
- Collapse the second sentence into only the extra trigger branches not already
  covered by the first.
- Keep the boundary against `tool-policies` sharp because the trigger suite has
  multiple hard negatives in that neighborhood.

## Defer

### `apple-hig`

`apple-hig/SKILL.md` is long, but the length is justified by diverse user-real
triggers: Apple HIG, Chinese phrasing, component names, state names, and
HTML/CSS/ARIA mapping. Keep as-is unless route traces show over-triggering on
generic frontend work.

### `adversarial-review`

Keep model-invoked and keep the "explicitly requested independent verification"
boundary. The description is narrow enough and the forbidden cases protect
ordinary implementation and completion summaries.

### `agent-evals`

Keep model-invoked. The description is clear enough against `persisting-traces`
and `training-models`. No rewrite needed before the eval-coverage audit.

### `bridging-legacy`

Keep model-invoked. The legacy/migration boundary is concise and the greenfield
anti-scope is clear.

### `importing-skills`

Keep model-invoked. The description cleanly separates external skill adoption
from session mining and from brand-new skill authoring.

### `markdown-pdf`

Keep model-invoked. The description has a strong source/output gate: only
Markdown source and PDF output. This is the right boundary.

### `mining-sessions`

Keep model-invoked. It has a narrow evidence gate: past Codex/Claude sessions
or transcript history. Add Chinese triggers only if real prompts start missing
it.

### `persisting-traces`

Keep model-invoked. The description is clear against evaluator scoring and
golden-case lifecycle work.

### `spec-first`

Keep model-invoked. The docs-backed and governing-spec gates are useful and
well-scoped.

### `tool-policies`

Keep model-invoked. The description is adjacent to `agent-loops`, but the
approval-gate/tool-registry vocabulary is distinct enough for now.

## Trigger Eval Observations

The current trigger suite already protects many important boundaries:

- `writing-papers` versus `drawing-figures`, `elsevier-submissions`, and
  `writing-resumes`.
- `agent-loops` versus `tool-policies`.
- `agent-evals` versus `persisting-traces` and `training-models`.
- `importing-skills` versus `mining-sessions`.

The biggest description/eval mismatch is Chinese trigger coverage:

- Chinese positive prompts exist for `training-models`, `elsevier-submissions`,
  `writing-papers`, `writing-resumes`, and `apple-hig`.
- Only `writing-papers` and `apple-hig` currently have Chinese trigger phrasing
  in the description.

Description rewrites should add Chinese phrasing before adding broad English
synonyms. If a description changes, rerun both the offline contract and the LLM
router before accepting the edit.

## Decision

Prioritize invocation/description fixes in this order:

1. `writing-papers`: prune and sharpen the longest, broadest description.
2. `elsevier-submissions`: add anti-scope and Chinese submission triggers.
3. `training-models`: add Chinese failure/training-loop triggers and shorten
   non-trigger stack detail.
4. `writing-resumes`: add Chinese resume/JD/bullet triggers.
5. `drawing-figures`: add Chinese figure-production triggers.
6. `agent-loops`: remove duplicate metadata wording while preserving hard
   negative boundaries.

Do not change model/user invocation mode yet.

