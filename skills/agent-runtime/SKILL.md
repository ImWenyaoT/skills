---
name: agent-runtime
description: 'Agent runtime work in a product codebase: bounded per-request agent loops, terminality and handoff states, vendor agent SDK behind a provider seam, runtime tool registries with risk-tiered approval gates, async turn scoring with golden and failure-case lifecycles, session/memory/trace persistence and transcript hydration, and compatibility adapters plus fallback deletion gates for legacy lanes. Use when a loop contract, tool policy, evaluator wiring, storage or hydration path, or legacy migration lane changes. Do not use for training or fine-tuning a model.'
---

# Engineering the Agent Runtime

The runtime of a product agent has five moving parts — the request loop, the tool policy
layer, the eval loop, the persistence layer, and the legacy lane being migrated away.
They are one task domain: they share a package graph, a bounded-step rule, a TDD rhythm,
a migration gate, and one shape of completion criteria. Changing one of them almost
always means verifying another, so they are handled and verified together.

This skill owns that runtime. It does not cover training or fine-tuning a model, and it
does not perform an independent review of a finished deliverable.

## Route to the part you are changing

| You are changing | Read |
|---|---|
| Loop contract, terminality, handoff, intent routing, vendor agent SDK wiring | [references/loop-contract.md](references/loop-contract.md) |
| Tool interface, registry, risk tiers, approval gates, playbooks | [references/tool-policy.md](references/tool-policy.md) |
| Evaluator wiring, scoring, thresholds, golden export, failure cases | [references/eval-loop.md](references/eval-loop.md) |
| Session/memory/trace storage, repositories, transcript hydration | [references/persistence.md](references/persistence.md) |
| Compatibility adapter, dual lanes, fallback deletion | [references/legacy-lane.md](references/legacy-lane.md) |

Most real changes touch two of these. Read both files, and verify both packages — the
common pairs and what each one costs if you verify only one side:

| Change | Why it couples | Verify on both sides |
|---|---|---|
| A step returns `handoff_and_wait` | The human who takes over reads the trace, not the loop | The step declares the state **and** the trace or memory patch carries enough context |
| A tool gains a real adapter | The stub was what made tests DB-free | The policy tiers still gate it **and** core still does not import the DB package |
| The evaluator needs a new signal | Scoring reads what persistence wrote | The eval core still returns plain shapes **and** the row is written by the storage layer |
| The legacy fallback is deleted | The flag that selected it also selected a loop path | The replacement passes without the fallback **and** the step is still bounded |

The spine below is what keeps those pairs consistent.

## The spine

### 1. One bounded step per request

An agent loop embedded in a stateless request handler must advance **one bounded step per
request**, never run an open-ended conversation loop that could spin unbounded.

- One request-handler call = one bounded step. Cap any internal model/tool loop (e.g.
  `maxTurns`) so a single request cannot run forever.
- Every step declares what happens next. An explicit terminal state is what makes the
  bound observable from outside the loop.
- Side effects are bounded the same way: an approval-required tool is a hard stop, not
  something to retry around.
- Work that must not extend the step runs detached, and its failure cannot fail the turn.
- Reads are bounded too: a history read asks for one row beyond the visible limit and
  reports "there is more" instead of silently truncating or returning everything.
- Deletions are bounded: a proven-dead lane leaves in one bounded change, not in a drip.

The unbounded trap is always the same move — calling the inner runner in a loop "to finish
the conversation". Whenever a change makes a step longer, ask what caps it.

### 2. Package layering: core, storage, web

The layering exists so that any single implementation can be swapped without touching
callers. Each rule below protects one swap.

- **Core** (loop, tools, policies, scoring logic) depends on **interfaces**, not on
  implementations: a model/provider boundary, an `Evaluator`, a `RuntimeTool`. It must not
  import the DB package, and it must not import a vendor agent SDK.
- **A vendor SDK is imported in exactly one place** — your provider package. Product code
  depends on a `Runner` interface. Verify by searching for SDK imports outside that package.
- **Core returns plain shapes; storage maps them onto rows** (adding ids). Repository APIs
  stay small and package-local, and route handlers never write raw SQL.
- **Do not add a dependency to core to read a config format.** A loader validates a plain
  object; the caller does the file-format conversion.
- **Stubs and adapters swap behind the same interface.** Deterministic tool stubs today,
  real adapters later; a legacy service behind a compatibility adapter. The interface is
  the thing that must stay stable.
- Add coverage in the package where the behavior changes, not in the topmost package that
  happens to notice.

### 3. TDD discipline

1. Write or update the test for the new behavior **first**, and watch it fail for the
   right reason. A test that passes before the change proves nothing about the change.
2. Implement the smallest change that makes it pass.
3. Reuse check before adding: confirm the behavior is not already implemented in the
   legacy service or an existing module.
4. Tests must not hit a real paid API. Inject the runner or evaluator so the loop is
   exercised without spending.
5. Tests must leave nothing behind in the worktree. Development gets a durable default
   store; tests opt into an in-memory or temporary store explicitly.
6. Separate deterministic assertions from anything that depends on model output. The
   deterministic lane must be able to fail the build on its own.

### 4. Migration gates

Two lanes exist at once during any migration — the proven one and the replacement.

- **Keep the legacy fallback readable and working until the new write path is proven
  stable.** This is one rule, and it applies equally to a legacy service adapter and to a
  legacy JSON memory snapshot.
- **Feature-flag the new lane; never make it the default before end-to-end validation.**
  When the flag is unset, the proven lane runs.
- **Do not over-normalize early.** During migration, storing a structured row plus a
  JSON-shaped blob is the cheaper reversible choice.
- **Define the deletion gate before comparing lanes, not after.** The concrete gate and
  the removal procedure are in the legacy-lane reference.
- A compatibility lane without callers is sediment. Once the gate passes, it goes.

### 5. Verification and done

Every part of this runtime completes in the same shape, in this order:

1. **Package-level tests** for each package you changed (core, storage, and any other).
2. **Typecheck.**
3. **The smallest integration build that exercises the change** — a route handler, a
   public-boundary contract test, the web build only if you touched the web layer.

Add coverage and the production build for the layers changed when the project requires
them. Each reference states what "done" means for its own part; the generic bar is that
the behavior you claimed is proven by a check someone else can re-run, at the lowest layer
that can prove it.
