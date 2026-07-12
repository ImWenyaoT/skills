---
name: adversarial-review
description: 'Adversarial review for explicitly requested independent verification: read-only reviewer, "is this actually done", high-risk readiness/release checks, blocker hunting, or validation of sub-agent results. Do not use for ordinary implementation, routine tests, or normal completion summaries.'
---

# Running Adversarial Subagent Reviews

Before calling non-trivial work done, dispatch an **independent, read-only sub-agent** to attack
assumptions and surface blockers the doer may have rationalized past.

## Rules

- Keep collaboration **tree-shaped**: sub-agents report only to the controller, and only the
  controller starts a reviewer.
- The reviewer is **read-only**: it must not edit files, spawn its own sub-agents, contact other
  sub-agents, or reimplement the work.
- Task it to hunt **blockers, weak evidence, missed tests, scope drift, and overconfident claims** —
  not to praise.
- Give it concrete artifacts: files changed, commands run, known risks, and the intended acceptance
  criteria.
- The controller decides and integrates; unresolved P0/P1 findings **block completion**. Done means
  every P0/P1 is either fixed, explicitly accepted by the user, or still listed as blocking.
- Don't recursively review the review process itself, unless you are changing this skill's rules.

## Prompt shape

```text
You are a read-only grill reviewer. Do not edit files. Do not contact other sub-agents.
Review: [scope]
Artifacts: [files changed, commands run, outputs]
Challenge assumptions around correctness, CI, cross-platform behavior, tests, docs, and scope.
Return findings by severity. If no blockers, say so and list residual risks.
```
