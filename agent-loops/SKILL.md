---
name: agent-loops
description: Designing an agent loop inside a stateless request handler that advances one bounded step per request — capping internal turns, modeling terminality/handoff states, continuing after tools, intent-routing retrieval vs cheap paths — and wiring a vendor agent SDK (e.g. the OpenAI Agents SDK) behind the loop's provider boundary. Use when implementing or modifying such a loop or its step contract, facing "one step per request" / terminality / handoff semantics, or integrating an agent-SDK runner / multi-provider config behind a single import site.
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

## Wiring a vendor agent SDK behind the loop

When a concrete provider is a vendor agent SDK (e.g. the OpenAI Agents SDK), keep it **behind the
provider boundary above** so product code never imports it directly and the loop stays bounded.

- **Import the SDK in ONE place.** Only your model/provider package imports the vendor SDK; product
  code depends on a `Runner` interface, never on the SDK directly. Verify: no SDK import outside that package.
- **Honor the one-bounded-step rule.** The vendor runner has its own loop limit (e.g. `maxTurns`,
  default small) — set it small and call `runner.run()` **once per step**, never loop it to "finish
  the conversation" (the unbounded trap above).
- **Feature-flagged, never default.** Gate the SDK lane behind an env flag; when unset, fall back to
  the legacy/LLM path. Don't default to it until validated end-to-end.
- **Provider-agnostic config.** Let SDK-specific env fall back to shared provider vars so a single
  provider works in dev; the SDK lane can target a premium endpoint while classification/eval stay cheaper.
- **Route only loop-semantics intents through the SDK**; cheap intents skip it. To add an intent, add
  it to the routing set AND confirm the SDK's tool set supports it.
- **Map the SDK result onto the step contract above:** final output → `reply_and_wait`; a handoff
  (active agent changed) → `handoff_and_wait`; otherwise → `reply_and_wait` waiting-for-user.
- **Version-check the SDK** before changing usage — agent-SDK APIs drift across 0.x releases. TDD via
  an injectable runner (`...FromFunction()`); don't write tests that hit the real paid API, and don't
  enable trace export by default in an MVP.
