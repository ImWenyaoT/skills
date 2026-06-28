---
name: bridging-legacy-services
description: Use when integrating a legacy service or module behind a compatibility adapter instead of rewriting it — preserving old sanitization, templates, memory, or behavior while a new path is built. Triggers on legacy adapters, compatibility lanes, build-before-import ordering, or keeping a fallback alive during migration.
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
5. If loop behavior changes, also apply the `building-bounded-agent-loops` skill.
