---
name: agent-evals
description: Builds or modifies an agent evaluation/regression loop — evaluator interface, async fire-and-forget turn scoring, golden-case export, failure-case lifecycle, regression harness, score thresholds, and review of low-scoring turns. Use for agent scoring/eval workflows. Do not use for storage schema or persistence-only trace fields — that is a storage concern, not eval.
---

# Running Agent Eval Loops

Score agent turns continuously, capture low-scoring turns as failure cases, and promote real
regressions into a golden set — **without slowing or breaking the user-facing turn.**

## Constraints

- **Don't fork the canonical scorer.** Wrap the existing evaluator behind an `Evaluator` interface;
  to change strategy, add a new implementation, not a forked prompt.
- **Keep layering clean.** The eval core returns plain shapes; the persistence layer maps them onto
  DB rows (adding ids). The core must not depend on the DB package.
- **Async eval is fire-and-forget.** In the request handler, run scoring detached (`void ...catch()`)
  so it never blocks or fails the user turn; only run it when both storage and an evaluator exist.
- **Golden export is zero-dependency and schema-stable.** Hand-write the golden format and match the
  existing golden schema exactly — compare against a known-good sample before changing it.

## Failure-case lifecycle

`open` (low score) → `promoted` (exported to golden) or `dismissed` (reviewed, not a regression).
Status flips via a simple UPDATE; no auto-archival. Pick an explicit score threshold
(score < threshold → candidate).

## Workflow

1. Read the eval plan/spec and the existing evaluator + golden samples first.
2. TDD: extend the matching test, run it red, then implement.
3. Reuse check: confirm the scoring/extraction isn't already in the legacy service before adding it.
4. Verify at package level (storage, core), then typecheck; if you touched the web layer, build it.

## Don't

- Don't add heavy eval frameworks unless the plan approves the runtime complexity — a regression
  script plus a review-summary aggregate is enough for an MVP.
- Don't store `score`/`evaluatorModel` on the trace row — they belong in a one-to-many reviews table
  (a trace may be re-evaluated).
