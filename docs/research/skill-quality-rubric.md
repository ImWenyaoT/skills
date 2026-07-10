# Skill Quality Rubric

Source ticket: [Synthesize the skill quality rubric](https://github.com/ImWenyaoT/skills/issues/7)

## Purpose

Use this rubric to audit this repo's skills before making broad edits. The goal is not prettier prose. The goal is predictable agent behavior: the right skill triggers, the loaded instructions drive the same process each run, and changes are protected by trigger and outcome evals.

## Sources

- Local reference: `writing-great-skills`
- Repo policy: `AGENTS.md`
- Anthropic: [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Anthropic: [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- OpenAI: [Agent Skills - Codex](https://developers.openai.com/codex/skills)
- OpenAI: [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills)

## Rubric

### 1. Self-Contained Boundary

Passes when:

- The skill is a single discoverable capability, not a catch-all.
- `SKILL.md` is shareable on its own and does not require another skill to make sense.
- Boundaries describe behavior, not sibling skill names.
- The deletion test is clear: if removed, a distinct capability disappears.

Repo mapping:

- `AGENTS.md` requires each skill to be self-contained and forbids depending on sibling skills.
- `AGENTS.md` also requires one skill to equal one discoverable capability.

### 2. Invocation And Description

Passes when:

- Invocation mode is intentional: model-invoked only when the agent or another skill must discover it autonomously; user-invoked when manual routing is enough.
- `name` is concrete, short, lowercase, and matches the directory.
- `description` front-loads the main trigger words.
- Each distinct trigger branch appears once; synonyms are not repeated as fake coverage.
- The scope and anti-scope are clear enough to avoid broad accidental firing.
- Chinese trigger phrasing is present when real users are likely to ask in Chinese.

Source rationale:

- OpenAI Codex docs state that implicit invocation depends on `description`, so descriptions need clear scope and front-loaded trigger words.
- OpenAI's eval article emphasizes that `name` and `description` are primary signals for whether the skill is invoked.
- `writing-great-skills` treats descriptions as trigger branches with a strict context-load budget.

### 3. Information Hierarchy And Progressive Disclosure

Passes when:

- `SKILL.md` contains only what every relevant run needs immediately.
- Branch-specific or heavy reference material sits behind a reliable context pointer.
- References are one level deep from `SKILL.md`.
- Long references include a `## Contents` section.
- The pointer wording tells the agent when to open the file.
- Related definitions, caveats, and rules are co-located.

Source rationale:

- Anthropic describes skills as progressively disclosed folders where metadata loads first, `SKILL.md` loads when relevant, and linked files load only as needed.
- OpenAI Codex docs describe the same progressive loading pattern and the optional `scripts/`, `references/`, and `assets/` folders.
- `writing-great-skills` frames this as an information hierarchy: in-skill steps, in-skill reference, external reference.

### 4. Steps And Completion Criteria

Passes when:

- Complex skills have ordered steps or clear branches.
- Each step ends in a checkable completion criterion.
- Critical criteria are exhaustive enough to prevent premature completion.
- The skill says what evidence proves the work is done.
- The skill hides post-completion work only when visible future steps make the agent rush the current step.

Source rationale:

- OpenAI's eval article uses a clear definition of done so success can be measured.
- `writing-great-skills` identifies vague completion criteria as the main cause of premature completion.

### 5. Concision, Pruning, And Leading Words

Passes when:

- Every sentence changes behavior versus the model default.
- Repeated meanings have one source of truth.
- No-op prose, stale sediment, and duplicated branches are removed.
- Prohibitions are expressed as positive target behavior where possible.
- Strong leading words carry repeated concepts instead of restating them repeatedly.

Source rationale:

- Anthropic's best-practices guide treats context as scarce and recommends adding only information the model actually needs.
- `writing-great-skills` names the recurring failure modes: duplication, sediment, sprawl, no-op, negation, and premature completion.

### 6. Specificity And Determinism

Passes when:

- The skill uses flexible prose for heuristic work and scripts/templates for fragile or repetitive work.
- Scripts solve concrete deterministic subproblems instead of pushing work back to the model.
- Script dependencies and expected runtime assumptions are explicit.
- Intermediate outputs are verifiable when quality or safety depends on them.
- Errors from scripts are useful enough to repair the workflow.

Source rationale:

- Anthropic recommends matching specificity to task fragility and using executable code where deterministic reliability matters.
- Anthropic also warns not to assume tools or packages are installed.
- This repo's `AGENTS.md` prefers reusable scripts, standard library where reasonable, and validation before push.

### 7. Eval Coverage

Passes when:

- Each skill has realistic positive prompts.
- Each skill has forbidden prompts and adjacent hard negatives.
- Path-specific skills include path, repository, or unique site signals in positives.
- Abstain cases exist for broad neighboring domains.
- Description edits are followed by route evals.
- Outcome evals exist or are planned for skills whose success is more than correct invocation.

Source rationale:

- OpenAI recommends starting from measurable success, then checking process, outcome, style, and efficiency.
- OpenAI recommends small targeted prompt sets and turning real failures into eval cases.
- This repo already defines the two-layer contract: route-level trigger evals plus result-level graders.

### 8. Safety, Portability, And Trust

Passes when:

- The skill does not quietly expand permissions, network use, or filesystem writes.
- External dependencies, scripts, and assets are auditable.
- The skill remains portable across Codex and Claude where the repo claims dual-runtime support.
- Platform-specific behavior is called out explicitly.

Source rationale:

- Anthropic's engineering article notes that skills may include executable code, which increases power and risk.
- This repo's `AGENTS.md` treats the repository as the source for both Codex and Claude local mirrors.

## How To Use This Rubric

For each audit ticket:

1. Score only the dimensions in that ticket's question.
2. Quote the exact file and line evidence.
3. Classify findings as `must fix`, `worth fixing`, or `defer`.
4. Separate skill-content findings from infrastructure findings.
5. Do not implement rewrites during the audit.

The final prioritization ticket should combine the audit outputs into:

- small description edits,
- `SKILL.md` pruning,
- reference restructuring,
- eval additions,
- script/example improvements,
- deferred or out-of-scope work.
