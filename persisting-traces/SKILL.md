---
name: persisting-traces
description: Trace and memory persistence for agent sessions: migration-safe structured store, JSON fallback, storage schemas, SQLite/DB repositories, session state, memory snapshots, trace rows, and debug/eval fields as stored data. Do not use for evaluator scoring, golden export, or failure-case lifecycle design.
---

# Persisting Agent Memory and Traces

Persist agent session state, memory, and traces with a **migration-safe** path: a structured store
first, a JSON fallback until the new write path is proven.

## Rules

- Store session/state and JSON-shaped memory first; **don't over-normalize** every profile field early.
- Preserve the legacy JSON memory fallback until the structured write path is stable.
- Put evidence and debugging detail in **traces**, not long-term memory — don't promote transient
  retrieval evidence into durable customer memory by default.
- Trace rows should retain event / action / input / output / toolCalls / references when available.
- Scoring/evaluating those traces is a separate concern — this skill owns **storage** only, not the
  evaluator/scoring lifecycle.

## Workflow

1. Write or update the repository test before changing repositories (TDD).
2. Verify the JSON fallback still works for legacy memory snapshots.
3. Keep repository APIs small and package-local; route handlers must not write raw SQL.
4. Verify the storage package tests + typecheck; if route persistence changed, build the web layer.
   Done means structured storage and JSON fallback both round-trip representative session state.
