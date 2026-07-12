---
name: bridging-legacy
description: 'Compatibility adapters for legacy services during migration: preserve old sanitization, templates, memory, behavior, build-before-import ordering, and fallback lanes while a new path is built. Do not use for greenfield rewrites.'
---

# Bridging Legacy Services

Wrap a legacy service behind a **compatibility adapter** rather than rewriting it mid-migration.
The old code is the proven lane until the new path is fully validated.

## Rules

- Treat the legacy service as a **compatibility lane, not code to rewrite** during feature work.
- Go through the existing adapter boundary before bypassing old sanitization, templates, memory, or
  action selection.
- **Build the legacy package before** anything imports its compiled output.
- Keep the legacy fallback readable and working until the new write path is proven stable.

## Workflow

1. Read the legacy module and the adapter that wraps it.
2. Decide whether the change touches only legacy behavior or also the new path.
3. Add regression coverage in the package where behavior changes.
4. Build the legacy package; if a new-path layer imports or wraps it, build that too.
5. If the change also alters the agent loop's behavior, re-verify that bounded-step design separately.
   Done means the adapter path and fallback path are both tested or explicitly verified.
