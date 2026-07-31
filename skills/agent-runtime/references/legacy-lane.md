# Legacy lane and deletion gate

## Contents

- [Rules](#rules)
- [Workflow](#workflow)
- [Done](#done)

Wrap a legacy service behind a **compatibility adapter** rather than rewriting it
mid-migration. The old code is the proven lane until the new path is fully validated.
This is a migration technique, not a way to run a greenfield rewrite.

## Rules

- Treat the legacy service as a **compatibility lane, not code to rewrite** during feature
  work.
- Go through the existing adapter boundary before bypassing old sanitization, templates,
  memory, or action selection.
- **Build the legacy package before** anything imports its compiled output.
- Once the replacement owns production and meets the declared baseline, delete the
  fallback, its parser, switches, and legacy-only fixtures in one bounded change. Migrate
  behavior contracts that still apply to the replacement; a compatibility lane without
  callers is sediment.

## Workflow

1. Read the legacy module and the adapter that wraps it.
2. Decide whether the change touches only legacy behavior or also the new path.
3. Add regression coverage in the package where behavior changes.
4. Define the deletion gate before comparing lanes: production caller moved, deterministic
   contracts pass, representative integration/eval baseline met, and the project's
   deployment/data rollback plan is explicit and exercised in proportion to risk.
5. Build the legacy package; if a new-path layer imports or wraps it, build that too.
6. When the gate passes, migrate still-valid behavior tests, remove legacy-only tests and
   the old lane, then search manifests, docs, env switches, and source for leftovers.
   Re-run the replacement without the fallback present.
7. If the change also alters the agent loop's behavior — for example because the legacy
   lane was the fallback a feature flag pointed at — re-verify the bounded-step design
   against the loop contract, which `SKILL.md` routes to.

## Done

Either both lanes remain intentionally supported, or the proven legacy lane is absent and
the replacement passes without it.
