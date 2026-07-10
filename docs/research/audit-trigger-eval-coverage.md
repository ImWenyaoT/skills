# Trigger Eval Coverage Audit

## Purpose

Answer GitHub issue #5: using the shared skill quality rubric, identify where
`evals/trigger_cases.json` is weak for the skills themselves.

This audit does not add or edit cases. It decides which trigger eval additions
are needed before later `description` and `SKILL.md` edits can be trusted.

## Rubric Used

The source rubric is `docs/research/skill-quality-rubric.md`, especially
"Eval Coverage":

- Each skill should have realistic positive prompts.
- Each skill should have forbidden prompts and adjacent hard negatives.
- Path-specific skills should include path, repository, or unique site signals
  in positives.
- Abstain cases should exist for broad neighboring domains.
- Description edits should be followed by route evals.
- Outcome evals are separate from route-level trigger evals and belong to the
  later completion/determinism audit.

## Method

Checks performed:

- Read `evals/trigger_cases.json` and grouped every case by `expected_skills`
  and `forbidden_skills`.
- Counted positives, forbidden cases, Chinese positives, Chinese forbidden
  cases, abstain negatives, and adjacent hard-negative pairings per skill.
- Compared coverage against the prior invocation/description audit in
  `docs/research/audit-invocation-descriptions.md`.
- Read `scripts/evaluate_skill_triggers.py` and `scripts/route_with_llm.py` to
  separate offline contract coverage from model-in-the-loop routing evidence.
- Ran the current trigger contract with the repo-preferred `uv run` command.

## Current Coverage Snapshot

The offline contract is structurally healthy:

- 16 skills are loaded.
- 69 trigger cases exist.
- Every skill has at least 2 positive cases.
- Every skill has at least 2 forbidden cases.
- There are 9 abstain cases where no skill should fire.

Notable strong areas:

- `writing-papers` has broad coverage: 12 positives, 9 forbidden cases, 5
  Chinese positives, and hard negatives against `drawing-figures`,
  `elsevier-submissions`, and `writing-resumes`.
- `agent-loops` and `tool-policies` are mutually well protected with multiple
  hard negatives.
- `agent-evals`, `persisting-traces`, and `training-models` have useful
  neighboring negatives.
- `importing-skills` and `mining-sessions` are well separated around external
  adoption versus local session mining.

The main weakness is not minimum coverage. The main weakness is that the cases
do not yet protect several description edits recommended by the invocation
audit.

## Must Add Before Description Edits

### `drawing-figures`: Chinese figure-production positives

Current state:

- 3 positives.
- 0 Chinese positives.
- Strong forbidden coverage against `writing-papers`, `elsevier-submissions`,
  and `apple-hig`.

Why this matters:

The invocation audit recommends adding Chinese trigger phrasing to the
`drawing-figures` description. That edit cannot be trusted without at least one
Chinese positive and one nearby Chinese hard negative.

Add cases like:

- Positive: `帮我给这篇 CVPR 论文画 600 dpi 架构图、结果拼图和效率图。`
  Expected: `drawing-figures`; forbidden: `writing-papers`.
- Negative/hard negative: `帮我改写 Figure 3 的 caption，并检查图文表是否自洽。`
  Expected: `writing-papers`; forbidden: `drawing-figures`.

### `writing-resumes`: PDF/layout-only forbidden cases

Current state:

- 3 positives, including 1 Chinese positive.
- 6 forbidden cases.
- No direct case for the explicit anti-scope: "PDF-only export/layout".

Why this matters:

The description says not to use `writing-resumes` for PDF-only export/layout,
but the trigger suite only tests generic Markdown-to-PDF work. It does not test
the high-risk prompt shape: resume + PDF/layout wording.

Add cases like:

- Negative/abstain: `把我的简历 PDF 排版调紧一点，不改内容。`
  Expected: none; forbidden: `writing-resumes`.
- Negative/hard negative: `Convert this Markdown resume into a printable PDF
  without changing the resume wording.`
  Expected: `markdown-pdf` if the source is Markdown and output is PDF;
  forbidden: `writing-resumes`.

### `elsevier-submissions`: generic cover-letter and non-packet negatives

Current state:

- 4 positives, including 1 Chinese positive.
- 4 forbidden cases.
- "Cover letter" appears only in Elsevier-positive contexts.

Why this matters:

The invocation audit recommends adding anti-scope around generic cover-letter
writing and manuscript language review. Before changing the description, the
suite should prove that generic cover-letter prompts do not trigger the
Elsevier packaging skill.

Add cases like:

- Negative/abstain: `Write a job application cover letter for this software
  engineering role.`
  Expected: none; forbidden: `elsevier-submissions`.
- Negative/hard negative: `Draft a non-Elsevier conference submission cover
  letter, but do not package an Editorial Manager submission.`
  Expected: none or `writing-papers` only if framed as manuscript prose;
  forbidden: `elsevier-submissions`.

### `writing-papers`: non-paper LaTeX and generic academic-adjacent negatives

Current state:

- 12 positives and 9 forbidden cases.
- Good coverage of drafting, review, AI-tone cleanup, figure/table linkage,
  rebuttal, and Chinese paper-writing prompts.
- Existing abstain cases cover generic English editing and blog/README
  drafting.

Why this matters:

The `writing-papers` description is the broadest description in the repo and
contains words like `LaTeX polish`, `citations`, and `captions`. The existing
negatives do not directly cover non-paper LaTeX or generic academic-adjacent
tasks.

Add cases like:

- Negative/abstain: `Fix the LaTeX formatting in this resume template without
  changing content.`
  Expected: none; forbidden: `writing-papers`.
- Negative/abstain: `Write a short academic bio for a conference website.`
  Expected: none; forbidden: `writing-papers`.

## Worth Adding

### `markdown-pdf`: Chinese Markdown-to-PDF positive

Current state:

- 2 positives.
- 0 Chinese positives.
- Strong source/output gate in the description.

Add a Chinese positive such as:

- `把这个 Markdown 报告导出成带目录、代码高亮和页码的 PDF。`
  Expected: `markdown-pdf`; forbidden: `writing-resumes`.

### `apple-hig`: generic frontend abstain case

Current state:

- 3 positives, including 1 Chinese positive.
- 2 forbidden cases: publication figure drawing and Android Material.

Why this matters:

`apple-hig` is intentionally broad across web apps, blogs, dashboards, and
agent/chat UI. The suite should include one generic frontend prompt that should
not fire HIG unless Apple/HIG/native-quality language is present.

Add a case like:

- Negative/abstain: `Make this dashboard cleaner and improve the spacing and
  colors.`
  Expected: none; forbidden: `apple-hig`.

### `spec-first`: Chinese docs-backed positive

Current state:

- 2 positives.
- 0 Chinese positives.

Add a Chinese positive if this skill remains important in Chinese repo work:

- `这个 docs-backed codebase 要改 package boundary，先更新 governing spec 再改代码。`
  Expected: `spec-first`; forbidden: `bridging-legacy`.

### `adversarial-review`: Chinese explicit-review positive

Current state:

- 2 positives.
- 0 Chinese positives.
- Good abstain negatives for ordinary implementation and summaries.

Add only if user prompts commonly ask in Chinese:

- `先别说完成，找一个独立 reviewer 做只读 adversarial review，专门挑 blocker。`
  Expected: `adversarial-review`; forbidden: `agent-evals`.

### `importing-skills` and `mining-sessions`: Chinese meta-workflow positives

Current state:

- Both have adequate English coverage and clean hard negatives against each
  other.
- Neither has Chinese positives.

Add Chinese positives only if these meta-workflows are commonly invoked in
Chinese:

- `帮我评估这个 GitHub 上的 skill 能不能导入，检查 license、出处和 attribution。`
  Expected: `importing-skills`; forbidden: `mining-sessions`.
- `扫描我过去的 Codex 会话，把重复出现的问题整理成应该新增或改进的 skill。`
  Expected: `mining-sessions`; forbidden: `importing-skills`.

## Defer

### `agent-loops` and `tool-policies`

Coverage is strong enough for the recommended `agent-loops` metadata dedupe:

- `agent-loops` has 6 positives and 5 forbidden cases.
- `tool-policies` has 4 positives and 4 forbidden cases.
- They directly test SDK/runner/step-contract work versus approval gates,
  deterministic stubs, and tool registry policy.

Do not add cases before the small description dedupe unless a route trace shows
confusion.

### `agent-evals`, `persisting-traces`, and `training-models`

Coverage is acceptable for route-level triggering:

- `training-models` already has 6 positives, including 2 Chinese positives.
- `agent-evals` is protected against `training-models` and
  `persisting-traces`.
- `persisting-traces` is protected against evaluator lifecycle and tool policy
  prompts.

The next work for these skills is not more trigger cases by default; it is
outcome/determinism coverage, which belongs to issue #6.

### `bridging-legacy`

Coverage is minimal but sufficient:

- 2 positives.
- 2 forbidden cases.
- The positives include legacy adapter and build-before-import bridge signals.
- The negatives cover greenfield agent loops and spec-first architecture work.

Add cases only if this skill is edited.

## Router Evidence Gap

`scripts/route_with_llm.py` exists, and `scripts/evaluate_skill_triggers.py`
supports `--predictions` for per-skill precision/recall/F1, abstain false
trigger rate, confusion matrix, and pass@k/pass^k.

No predictions JSONL is currently present in the repo. That means current
verification proves the offline contract and metadata smoke test, but not
actual model routing behavior.

Before accepting broad description rewrites, run an LLM-router pass and score
it, for example:

```bash
env UV_CACHE_DIR=.cache/uv uv run python scripts/route_with_llm.py \
  --model <model> --trials 3 --out .cache/trigger-predictions.jsonl

env UV_CACHE_DIR=.cache/uv uv run python scripts/evaluate_skill_triggers.py \
  --predictions .cache/trigger-predictions.jsonl
```

Keep `.cache/trigger-predictions.jsonl` out of the repository unless the team
decides to version route snapshots.

## Decision

Prioritize trigger eval additions in this order:

1. Add Chinese `drawing-figures` positive and Chinese caption-only hard
   negative.
2. Add resume PDF/layout-only forbidden cases for `writing-resumes`.
3. Add generic cover-letter and non-packet negatives for
   `elsevier-submissions`.
4. Add non-paper LaTeX / academic-adjacent abstain negatives for
   `writing-papers`.
5. Add Chinese positive coverage for `markdown-pdf`, then optionally
   `spec-first`, `adversarial-review`, `importing-skills`, and
   `mining-sessions`.
6. Run the LLM router before and after broad description edits; do not rely on
   the offline contract alone for those changes.

