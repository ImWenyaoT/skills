---
name: adopting-open-source-skills
description: Vets and imports external skills into your own library — checking provenance and license, deciding use-as-is vs adapt vs clean-room rewrite, and recording attribution. Use when considering external, community, open-source, copied, forked, or upgraded skills for your workflows, when importing or forking a skill, or when adapting someone else's workflow into your own.
---

# Adopting Open Source Skills

Bring an external skill into your own library deliberately: prefer **adapting a focused workflow**
over copying a broad skill, and never blur provenance.

## Rules

- Prefer adapting a focused workflow over copying a broad skill wholesale.
- Record **provenance** for every external idea used: source URL/path, license, version/commit,
  license compatibility, required notices, and your local changes.
- Keep imported workflow skills in your skills directory; don't mix them with runtime/product code.
- Strip vendor-specific assumptions that don't apply to you.
- If license or provenance is unclear, **do not copy, paraphrase, or closely adapt** the source —
  write a clean-room skill from independently stated needs.
- Preserve required copyright / attribution / NOTICE text when the license demands it.

## Adoption checklist

1. Identify the repeated workflow the skill should improve.
2. Inspect the source skill and its license.
3. Decide: use as-is, adapt, or clean-room rewrite.
4. Keep the `SKILL.md` concise and scoped to your need.
5. Add a `## Provenance` section for any external idea, copy, fork, or adaptation.
6. Run an adversarial review (see the `running-adversarial-subagent-reviews` skill) before accepting it.
