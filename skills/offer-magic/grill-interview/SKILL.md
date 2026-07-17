---
name: grill-interview
description: Grill an interview answer before an interviewer does. Use when the user wants to explain a project, improve an answer, prepare for technical or past-experience questions, or run a mock interview.
---

# Grill Interview

Grill answers before an interviewer does. Own interview preparation and keep run state in `.offer-magic/grill-interview/`, never inside this installed skill.

## Route the request

- Mine a real story: read [prompts/story-mining.md](prompts/story-mining.md).
- Structure an existing answer: read [prompts/structuring.md](prompts/structuring.md).
- Prepare from a job and resume: read [prompts/jd-driven-prep.md](prompts/jd-driven-prep.md).
- Analyze question banks, interview records, or resume follow-ups: read [references/resume-question-graph.md](references/resume-question-graph.md).
- Diagnose or answer a technical, project, scenario, or past-experience question: read [references/answer-the-evaluation.md](references/answer-the-evaluation.md).
- Run a mock interview: use [subagents/interviewer.md](subagents/interviewer.md) and relay one question at a time.

Read optional workspace rules from `resume-profile.md`, `docs/resume-profile.md`, or `.resume/resume-profile.md`. Routing is complete when the target role or capability, available evidence, and output are known.

## Keep every answer true

Use only real events supplied by the user or supported by artifacts. Verify numbers and ownership. Ask one focused question at a time. Missing facts remain missing.

For a first internship, projects, research, coursework, competitions, and sustained personal practice are valid evidence when their scope is explicit. As professional evidence grows, prefer relevant workplace stories while keeping projects that show distinct technical judgment or learning.

Store full events with STAR by default. Read [frameworks/star-car.md](frameworks/star-car.md) only when another shape is needed. Keep context brief, make personal decisions and actions explicit, and include result, limit, and learning when known.

A story is ready only when responsibility, decisions, actions, result, and uncertainty are distinguishable.

## Turn the resume into a question map

Use the final resume and frozen role report from `grill-resume` when available. Every emphasized mechanism, number, trade-off, failure, or result is a possible hook. Separate observed interview questions, repeated patterns, and inference.

Treat the resume as the interviewer's menu, not the candidate's archive. Do not reward more bullets or density for its own sake. Prefer fewer, sharper hooks: each project bullet should open with one visible thesis and include enough mechanism plus validation for the interviewer to understand why the claim is credible. A bullet may occupy one to two visual lines; do not call it overloaded merely because it is long. Reserve secondary implementation detail, alternatives, failures, limits, and learning for follow-up. A compact early-career resume normally needs fewer than ten project bullets; do not invent extra hooks to reach a quota.

For each important hook, map the likely question, capability tested, real supporting event, missing evidence, and other questions the event can answer. Build a project defense from [assets/project-defense-template.md](assets/project-defense-template.md). Keep its three-minute spine in resume order and make each bullet a standalone thesis that expands into matching evidence, boundaries, failures, and learning.

Mark hooks green, yellow, or red. Correct red resume claims through `grill-resume`; grill the user one material fact at a time for yellow hooks; keep green hooks in the defense.

Mark a bullet `overloaded` only when it contains multiple independent theses or spends secondary interview-drawer evidence without making its primary claim more credible. Mechanism and validation that directly support the same thesis are not overload. Return the exact weaker clause to remove or defer. The goal is a one-to-one map from visible thesis to likely evaluation, not maximal question count.

Mapping is complete when every high-signal hook either has a defensible answer or is an explicit gap.

## Answer what is being tested

Relevance is a gate before correctness. Identify whether the interviewer is testing fundamentals, diagnosis, project evidence, system design, or past behavior. Clarify one material ambiguity, answer that layer directly, then add project evidence.

Use [references/answer-the-evaluation.md](references/answer-the-evaluation.md). For failure diagnosis, separate observable symptom, likely cause, recovery, and verification. Testing proves the handling; it does not replace fault localization or recovery.

An answer is ready only when it addresses the requested layer, uses supported evidence, and states material limits.

## Use the isolated interviewer

Freeze the role report, final resume, relevant evidence, observed questions, and candidate answer in `.offer-magic/grill-interview/`. Exclude the parent transcript, desired findings, earlier reviewer conclusions, and `.offer-magic/grill-resume/candidate-profile.json`. If profile language was explicitly added to the final resume, the Interviewer sees only that ordinary resume text.

Run a fresh Interviewer subagent from [subagents/interviewer.md](subagents/interviewer.md). It may read only the frozen packet and this skill. Validate its report and quoted evidence with `scripts/validate-interview-report.py --report <report> --packet <packet>`. The main agent resolves factual disputes from evidence and may grill the user when a missing fact changes the answer.

For a mock interview, the main agent relays one question and one answer at a time. Each evaluation consumes the frozen state and returns only to the main agent; it never contacts `grill-resume` or its subagents.

## Save only requested state

Persist stories or defenses only when requested or configured. Use the profile path or `.offer-magic/grill-interview/`. Initialize from [assets/story-template.md](assets/story-template.md), [assets/story-index.md](assets/story-index.md), and [assets/project-defense-template.md](assets/project-defense-template.md). Update the workspace index whenever an artifact changes.

Default output is a concise spoken answer plus preparation notes in the requested language. Generate HTML only when requested.

The skill is complete when the requested answer or artifact exists, its facts match the frozen resume, and isolated interviewer findings are validated or explicitly unavailable.

## Attribution

Adapted from `yanliudesign/offer-toolkit-skill` commit `0889e54` under MIT. See [../LICENSE](../LICENSE).
