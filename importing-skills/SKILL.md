---
name: importing-skills
description: External skill adoption: vet community/open-source/copied/forked skills, check provenance and license, choose use-as-is vs adapt vs clean-room rewrite, and record attribution. Do not use for mining your own sessions or authoring a brand-new skill from scratch.
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
6. Run an independent, read-only adversarial review before accepting it. Done means license,
   provenance, local changes, and attribution requirements are recorded or the skill is rejected.
