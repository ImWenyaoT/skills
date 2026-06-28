---
name: persisting-agent-memory-and-traces
description: Persists agent session state, memory snapshots, and trace rows via a migration-safe structured store with a JSON fallback. Use when modifying storage schemas, SQLite/DB repositories, session state, memory snapshots, trace persistence, JSON-fallback migration, or debug/eval trace fields as stored data. Do not use for evaluator scoring, golden export, or failure-case lifecycle design.
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

## Workflow

1. Write or update the repository test before changing repositories (TDD).
2. Verify the JSON fallback still works for legacy memory snapshots.
3. Keep repository APIs small and package-local; route handlers must not write raw SQL.
4. Verify the storage package tests + typecheck; if route persistence changed, build the web layer.
