---
name: tool-policies
description: 'Runtime tool policies for agents: uniform tool interface, tool registry, risk-tiered policy gates, approval-required hard stops, deterministic stubs, and POJO-validated playbooks. Use when adding or changing runtime tools, policies, approval gates, or playbooks.'
---

# Designing Agent Tool Policies

Give an agent a runtime vocabulary of **tools, policies, and playbooks** with risk-tiered gating, so
side effects stay controlled and high-risk actions can't fire unapproved.

## Core constraints

1. **One uniform tool interface.** Tools share a `RuntimeTool` type: input is a loose JSON record
   (the model describes it), and the tool's own `execute()` validates. Keep the interface stable so
   real adapters can later replace stubs without changing callers.
2. **Risk drives policy; an approval flag is the hard stop.**
   - `low` → allowed automatically (read-only, internal note, follow-up).
   - `medium` → requires approval (customer-facing).
   - `high` → `approvalRequired: true` and policy requires approval; `execute()` throws
     "not implemented" until a real adapter exists.
   - `closed` session → deny all side effects.
3. **Two gates, no duplication.** A raw `invoke()` is the hard gate (approval-required throws);
   `invokeWithPolicy()` consults the policy first (session status / risk tier). Don't duplicate the
   gate logic across both.
4. **Deterministic stubs.** Tool stubs return hardcoded data with fixed ids/timestamps so tests need
   no DB. Real inventory/order/finance adapters swap in behind the SAME interface later.
5. **Playbooks load from a POJO, not YAML.** The loader validates a plain object (e.g. with zod); the
   caller does the yaml→object conversion, so the core gains no new parser dependency.

## Workflow

1. Read your tools/knowledge spec and the tool-interface type first.
2. TDD: register a tool, invoke a read-only one, assert a high-risk tool throws approval-required.
3. Register the tool in the default registry and export it.
4. Verify the core package tests + typecheck. Done means low/medium/high/closed policy outcomes are
   covered by tests or explicit fixtures.

## Don't

- Don't implement high-risk execution bodies early — schema + `approvalRequired: true` +
  "not implemented" is the deliverable until a real adapter exists.
- Don't couple tools to the DB package — stubs are self-contained; real adapters are injected.
