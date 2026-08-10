# Spec conformance

Which rules of the Agent Skills specification this repository enforces, and which it
does not. Checked against <https://agentskills.io/specification> as retrieved on
2026-08-09.

This is a conformance record, not a copy of the spec. The spec is the authority; read
it there. What is worth writing down locally is the gap between what it requires and
what CI actually catches — a rule nobody checks is a rule that drifts.

## Frontmatter

| Spec rule | Enforced by |
|---|---|
| `name` required, 1–64 characters | `validate_skills.py` — error |
| `name` lowercase letters, digits, hyphens only | `validate_skills.py` — error |
| `name` must not start or end with a hyphen | `validate_skills.py` — error |
| `name` must not contain `--` | `validate_skills.py` — error |
| `name` must match the parent directory name | `validate_skills.py` — error |
| `description` required, 1–1024 characters | `validate_skills.py` — error |
| `license` optional | set to `MIT` on every skill; not validated |
| `compatibility` optional, ≤500 characters | `validate_skills.py` — error |
| `metadata` optional string map | unused |
| `allowed-tools` optional, experimental | unused — see below |

House rules beyond the spec, enforced the same way: no reserved word (`anthropic`,
`claude`) in a name, and a `description` containing a colon must be YAML-quoted.

## Body and structure

| Spec rule | Enforced by |
|---|---|
| `SKILL.md` has YAML frontmatter followed by Markdown | `validate_skills.py` — error if `name` or `description` cannot be parsed |
| Keep `SKILL.md` under 500 lines | `validate_skills.py` — error |
| Keep `SKILL.md` under ~5000 tokens | `validate_skills.py` — warning, estimated at four characters per token because there is no tokenizer here |
| `scripts/`, `references/`, `assets/` are conventional, not required | not enforced; all four skills that need them follow it |
| File references are relative to the skill root | **not enforced** |
| Keep references one level deep from `SKILL.md` | **not enforced** |

House rule beyond the spec: a `references/` file over 100 lines opens with a
`## Contents` list of anchor links — warning.

## Not enforced, and why

- **Relative-path and depth rules.** A link checker would catch a reference that moved
  and a chain that got too deep. Nothing catches them today; both were found by hand
  during the last restructure, which is not a method.
- **`allowed-tools`.** The spec marks it experimental and says support varies. No skill
  here needs a pre-approved tool list badly enough to depend on a field that clients
  may ignore.
- **Skill output quality.** The spec's companion guide describes an `evals/evals.json`
  of prompts, expected outputs, and assertions, graded with and without the skill. This
  repository has none. It measures whether the right skill is *reached*, not whether the
  work it then does is good. That absence is deliberate: a model-in-the-loop half was
  built here once and deleted after never running, because sending the descriptions to
  an external endpoint was never approved. Rebuilding it is a decision, not an oversight.

## What this repository adds that the spec does not ask for

The spec governs one skill. Everything below governs a *collection*, where the failure
mode is two skills whose descriptions overlap:

- `evals/trigger_cases.json` — golden prompts, split 60/40 into train and validation,
  asserting which skill each should and should not reach.
- `scripts/evaluate_skill_triggers.py` — the contract, anti-scope, and smoke checks over
  those goldens.
- `tests/` — tests for the two checkers above, which never ship to anyone.

Anthropic's own collection at `anthropics/skills` carries none of this. It is a reference
library of examples; this one is used daily and its skills sit close enough together to
collide, which is what the goldens are for.
