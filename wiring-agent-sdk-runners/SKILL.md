---
name: wiring-agent-sdk-runners
description: Wires a vendor agent SDK behind an abstraction boundary — single import site, bounded turns, feature-flagged opt-in, dual/multi-provider config, and mapping SDK output onto your loop's step contract. Use when integrating or modifying a vendor agent SDK (e.g. the OpenAI Agents SDK); triggers on agent SDK integration, runner wiring, or provider config.
---

# Wiring Agent SDK Runners

Integrate a vendor agent SDK **behind a boundary** so product code never imports it directly, the
SDK loop stays bounded, and the lane is opt-in until validated.

## Core constraints

1. **Import the SDK in ONE place.** Only your model/provider package imports the vendor SDK; product
   code depends on a `Runner` interface in shared types, never on the SDK directly. Verify: no SDK
   import outside that one package.
2. **Bounded turns.** The runner must cap its internal loop (e.g. `maxTurns`, default small) so one
   request never runs an unbounded agent loop. Call `runner.run()` once per step, not in a loop.
3. **Feature-flagged, never default.** Gate the SDK lane behind an env flag; when unset, fall back to
   the legacy/LLM path. Don't make it the default until the runtime is validated end-to-end.
4. **Provider-agnostic config.** Let SDK-specific env fall back to shared provider vars so a single
   provider works in dev. The SDK lane can target a premium endpoint while classification/eval stay
   on a cheaper one.

## Action routing

- Route only the intents that need tool/handoff loop semantics through the SDK; cheap intents skip it.
- To add an intent: add it to the routing set AND confirm the SDK's tool set supports it.

## Output mapping

Map the SDK result onto your step contract: final output → reply; a handoff (the active agent
changed) → `handoff_and_wait` + waiting-for-human; otherwise → `reply_and_wait` + waiting-for-user.

## Workflow

1. Read your loop/integration spec and the adapter source first.
2. TDD via an injectable runner (a `...FromFunction()` constructor); add type-level coverage. Don't
   write tests that hit the real paid API.
3. **Version-check the SDK** before changing usage — agent SDK APIs drift across 0.x releases.
4. Verify the provider package tests + typecheck; if you touched the loop, test that too.

## Don't

- Don't enable trace export by default in an MVP — keep local runs local.
- Don't assume non-flagship endpoints support every SDK feature; tool-calling is the baseline,
  handoff/tracing may not work off every provider.
