---
name: persisting-traces
description: 'End-to-end persistence for agent sessions: migration-safe stores, SQLite repositories, durable development defaults, browser transcript hydration, memory snapshots, trace rows, and runtime/test database isolation. Use when session data exists in storage but disappears across UI switches, reloads, or process restarts. Do not use for evaluator scoring or failure-case lifecycle design.'
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
- Persist the **user-visible message**, including attachments. A trace that stores only the model's
  normalized text cannot reconstruct an image-only or text-plus-image turn.
- Treat persistence as a round trip: UI write -> route -> repository -> durable store -> read route ->
  UI hydration. A database row without a hydration path is not a persisted product experience.
- For repository-local file databases, give development a durable default, make tests opt into
  in-memory or temporary stores explicitly, and ignore the database plus its sidecars. External
  mounted paths stay outside repository ignore policy.
- Keep history reads bounded. Fetch one sentinel row beyond the visible limit and expose an explicit
  continuation/earlier-history signal named by the existing contract instead of silently truncating
  or returning an unbounded response.
- Scoring/evaluating those traces is a separate concern — this skill owns **storage** only, not the
  evaluator/scoring lifecycle.

## Workflow

1. Write or update the repository test before changing repositories (TDD).
2. Verify the JSON fallback still works for legacy memory snapshots.
3. Keep repository APIs small and package-local; route handlers must not write raw SQL.
4. If the product has a web/client transcript, add a public-boundary integration test that proves
   store -> API read -> client-safe contract. Include empty, partial, attachment, and history-limit
   cases.
5. If client hydration can overlap selection, key transient state by conversation and cancel stale
   reads so a late response cannot overwrite the newly selected conversation.
6. Verify the applicable storage tests, route/client integration, typecheck, coverage, and production
   build for the layers changed. Done means representative state survives every applicable
   switch/reload/restart boundary, while tests leave no runtime database in the worktree.
