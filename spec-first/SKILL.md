---
name: spec-first
description: Spec-first changes in docs-backed codebases: update governing specs, PRDs, or architecture docs before behavior, public-interface, package-boundary, runtime-lane, agent-loop, memory/trace, or domain-vocabulary changes. Do not use for ordinary README edits, typo fixes, or projects without governing docs.
---

# Making Spec-First Changes

In a docs-backed codebase the spec is the source of truth: when a change alters behavior, state,
architecture, or vocabulary, **update the docs before the code.**

## Workflow

1. Read the governing design docs and the nearest source files for the target package.
2. Classify the change into exactly one lane/package — don't let one change sprawl across boundaries.
3. If it alters behavior, state, architecture, or vocabulary → update the spec/docs first, then code.
4. Keep domain vocabulary stable; don't rename established runtime concepts casually.
5. Add or update focused tests for the package you changed.
6. Verify package-level first, then the smallest root-level check that proves integration. Done means
   the governing doc and code describe the same behavior and vocabulary.

## Don't

- Don't ship a behavior/architecture change with stale docs — the next reader, human or agent,
  trusts the spec over the code.
- Don't smear one change across multiple package boundaries to dodge a real interface decision.
