---
name: building-bounded-agent-loops
description: Guides designing an agent loop inside a stateless request handler so it advances one bounded step per request — capping internal turns, modeling terminality and handoff states, continuing after tools, and routing which intents trigger retrieval vs cheap paths. Use when implementing or modifying such a loop, or facing agent loop contracts, "one step per request", terminality, or handoff semantics in a stateless server.
---

# Building Bounded Agent Loops

An agent loop embedded in a stateless request handler must advance **one bounded step per request**,
never run an open-ended conversation loop that could spin unbounded.

## Constraints

- One request-handler call = one bounded step. Cap any internal model/tool loop (e.g. `maxTurns`)
  so a single request can't run forever.
- Model terminality explicitly. A useful state set: `reply_and_wait`, `tool_then_continue`,
  `schedule_and_wait`, `handoff_and_wait`, `close`. The step result declares what happens next.
- Route by intent: cheap intents (small talk, canned info) skip retrieval/tools; only the
  "needs-info" intent consults retrieval, tools, or an LLM fallback.
- A handoff step must carry enough context (via trace or a memory patch) for a human to take over.
- Keep the loop core depending on **interfaces** (your model/provider boundary), not on a vendor
  SDK's internals.

## Workflow

1. Write or update the loop test for the new behavior first; watch it fail for the right reason (TDD).
2. Implement the smallest loop change that passes.
3. Keep the loop package depending on provider *interfaces*, not SDK internals.
4. Verify at the package level, then the smallest integration build that exercises a route handler.

## Don't

- Don't call the inner runner in a loop "to finish the conversation" — that's the unbounded trap.
- Don't let cheap intents trigger expensive retrieval/tool paths.
