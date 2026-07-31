# Loop contract

## Contents

- [Step states and terminality](#step-states-and-terminality)
- [Intent routing](#intent-routing)
- [Workflow](#workflow)
- [Wiring a vendor agent SDK behind the loop](#wiring-a-vendor-agent-sdk-behind-the-loop)
- [Don't](#dont)
- [Done](#done)

## Step states and terminality

Model terminality explicitly. A useful state set:

| State | Meaning |
|---|---|
| `reply_and_wait` | The step produced a reply; the loop waits for the user. |
| `tool_then_continue` | A tool ran and the model continues **within the same bounded step**, still counted against the turn cap. |
| `schedule_and_wait` | Work was scheduled; nothing further happens in this request. |
| `handoff_and_wait` | A human or another agent now owns the conversation. |
| `close` | The session is finished. |

The step result declares what happens next. Without an explicit state, the only way to
know whether the loop is done is to run it again — which is how unbounded loops start.

A handoff step must carry enough context for a human to take over, via the trace or a
memory patch. A `handoff_and_wait` that leaves no readable record is a dead end for the
person who inherits it.

Keep the loop core depending on **interfaces** (your model/provider boundary), not on a
vendor SDK's internals.

## Intent routing

Route by intent: cheap intents (small talk, canned info) skip retrieval and tools; only
the "needs-info" intent consults retrieval, tools, or an LLM fallback. This is a cost and
latency boundary, so adding an intent to the expensive set is a deliberate decision.

## Workflow

1. Write or update the loop test for the new behavior first; watch it fail for the right
   reason.
2. Implement the smallest loop change that passes.
3. Keep the loop package depending on provider *interfaces*, not SDK internals.
4. Verify at the package level, then the smallest integration build that exercises a route
   handler.

## Wiring a vendor agent SDK behind the loop

When a concrete provider is a vendor agent SDK (e.g. the OpenAI Agents SDK), keep it
**behind the provider boundary** so product code never imports it directly and the loop
stays bounded.

- **Import the SDK in ONE place.** Only your model/provider package imports the vendor SDK;
  product code depends on a `Runner` interface, never on the SDK directly. Verify: no SDK
  import outside that package.
- **Honor the one-bounded-step rule.** The vendor runner has its own loop limit (e.g.
  `maxTurns`, default small) — set it small and call `runner.run()` **once per step**,
  never loop it to "finish the conversation".
- **Feature-flagged, never default.** Gate the SDK lane behind an env flag; when unset,
  fall back to the legacy/LLM path. Don't default to it until validated end-to-end.
- **Provider-agnostic config.** Let SDK-specific env fall back to shared provider vars so a
  single provider works in dev; the SDK lane can target a premium endpoint while
  classification and eval stay cheaper.
- **Route only loop-semantics intents through the SDK**; cheap intents skip it. To add an
  intent, add it to the routing set AND confirm the SDK's tool set supports it.
- **Map the SDK result onto the step contract above:** final output → `reply_and_wait`; a
  handoff (active agent changed) → `handoff_and_wait`; otherwise → `reply_and_wait`
  waiting-for-user.
- **Version-check the SDK** before changing usage — agent-SDK APIs drift across 0.x
  releases. TDD via an injectable runner (`...FromFunction()`); don't write tests that hit
  the real paid API, and don't enable trace export by default in an MVP.

## Don't

- Don't call the inner runner in a loop "to finish the conversation" — that's the
  unbounded trap.
- Don't let cheap intents trigger expensive retrieval/tool paths.

## Done

One request cannot exceed the configured turn cap, every step returns an explicit terminal
state, and cheap intents skip retrieval and tools.
