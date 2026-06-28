---
name: running-adversarial-subagent-reviews
description: Dispatches an independent, read-only sub-agent to attack a piece of work's assumptions and surface blockers. Use when the user explicitly asks for adversarial verification, an independent reviewer, "is this actually done", high-risk release/readiness checks, or validation of sub-agent results. Do not trigger for ordinary implementation, normal test runs, or routine completion summaries.
---

# Running Adversarial Subagent Reviews

Before calling non-trivial work done, dispatch an **independent, read-only sub-agent to attack the
assumptions** — to surface what the doer rationalized past.

## Rules

- Keep collaboration **tree-shaped**: sub-agents report only to the controller, and only the
  controller starts a reviewer.
- The reviewer is **read-only**: it must not edit files, spawn its own sub-agents, contact other
  sub-agents, or reimplement the work.
- Task it to hunt **blockers, weak evidence, missed tests, scope drift, and overconfident claims** —
  not to praise.
- Give it concrete artifacts: files changed, commands run, known risks, and the intended acceptance
  criteria.
- The controller decides and integrates; unresolved P0/P1 findings **block completion**.
- Don't recursively review the review process itself, unless you are changing this skill's rules.

## Prompt shape

```text
You are a read-only grill reviewer. Do not edit files. Do not contact other sub-agents.
Review: [scope]
Artifacts: [files changed, commands run, outputs]
Challenge assumptions around correctness, CI, cross-platform behavior, tests, docs, and scope.
Return findings by severity. If no blockers, say so and list residual risks.
```
