---
name: grill-resume
description: Grill a resume against the job before a recruiter does. Use when the user wants to clean or structure a pasted .txt or .md job description, understand a job, decide whether to apply, build a candidate profile from a resume, predict interview topics from a job alone, or write, review, change, format, or export a resume.
---

# Grill Resume

Grill the application before a recruiter does. Own the path from job understanding to a verified resume. Keep private run state in `.offer-magic/grill-resume/`, user-readable normalized JDs in `docs/offer/`, and never put either inside this installed skill.

## Route the request

- **Job or apply decision** — decode the job and return a validated role report. A resume is optional. Include likely interview themes when the request is based on the job alone.
- **Normalize a pasted JD** — remove copied-page noise and save one readable Markdown file per role under `docs/offer/` before analysis.
- **Candidate profile** — extract or update the main-only candidate model; grill one material gap at a time.
- **Review only** — freeze the current resume and use the HR reviewer. Do not edit.
- **Write or change** — decode the job when present, verify evidence, edit the resume, then run artifact checks and HR review.
- **Format or export only** — preserve approved content and read [references/artifact-pipeline.md](references/artifact-pipeline.md).

The only subagent owned by this skill is the HR Reviewer. Use it with no parent transcript: `fork_turns="none"` in Codex or an equivalent fresh subagent in Claude Code. If fresh delegation is unavailable, disclose that limit instead of presenting a parent review as isolated.

Routing is complete when exactly one branch owns the next action and its required inputs are known.

## Discover the contract

Locate the JD, resume, application type, career stage, authoritative content source, evidence sources, existing build path, and requested outputs. Read optional workspace rules from `resume-profile.md`, `docs/resume-profile.md`, or `.resume/resume-profile.md`.

A JD is required only for job-specific analysis. If a link cannot be read, ask for the text. Ask one focused question only when the answer can change the decision or wording.

Calibrate proof to career stage. For a first internship, projects, research, coursework, and open source can be primary evidence; missing prior internships is a hard gap only when the job explicitly requires them. As professional experience grows, give relevant internships and full-time work more weight without mechanically deleting useful projects.

Discovery is complete when the application type, career stage, evidence boundary, authoritative source, and deliverables are explicit.

## Freeze the job before matching

Normalize a pasted `.txt` or `.md` JD before decoding it. Create `docs/offer/` when absent and save each role as `docs/offer/<job title>.md`; sanitize path separators and append a numeric suffix instead of overwriting an existing different role. If one input contains several roles, split them into separate files and never merge their content.

Use exactly one H1 job title and these three H2 sections: `职位描述`, `任职要求`, and `加分项`. Map `主要职责` or `岗位职责` to `职位描述`. Preserve the effective source wording and only normalize numbering, blank lines, and basic punctuation. Remove company introductions, navigation, contact details, location, update time, privacy notices, and other copied-page chrome. Keep “优先” clauses where they originally appear; when the source has no explicit bonus section, write `无` under `加分项`. Do not summarize, polish, add facts, or mix roles.

For job-specific work, the main agent decodes the JD from a candidate-blind input and writes the role report. Validate it with `scripts/validate-role-report.py`; do not create another business subagent for JD analysis.

The report separates hard requirements, real work, preferences, and environment signals; every important signal cites the JD and labels inference. Read [prompts/jd-decoder.md](prompts/jd-decoder.md) for the decode path, [frameworks/decode-patterns.md](frameworks/decode-patterns.md) only for ambiguous wording, and [frameworks/match-rubric.md](frameworks/match-rubric.md) only when a score is explicitly requested.

For an apply decision, map each hard signal to `strong`, `adjacent`, `none`, or `irrelevant`. Judge hard conditions, desired work, environment fit, evidence gaps, and opportunity cost. Do not invent an interview probability.

This stage is complete when the validated role report is frozen and every hard requirement has a cited status or an explicit absence.

## Establish truth before wording

Verify claims against code, tests, artifacts, publications, records, and explicit user statements. Label inference. Verify every number and ownership verb. Separate project outcome from personal contribution: relevance, decisions, mechanisms, boundaries, and learning matter more than implying one person caused the project to succeed.

For substantive work, read [references/offer-loop.md](references/offer-loop.md). Build one evidence map from the frozen role report. An unknown stays absent or becomes one focused question; it never becomes a stronger claim.

Evidence work is complete when every proposed high-value claim has a source and every emphasis has a screening or interview reason.

## Maintain the main-only candidate profile

Read [references/candidate-profile.md](references/candidate-profile.md). Build or incrementally update `.offer-magic/grill-resume/candidate-profile.json` from the resume, evidence, profile, and explicit user statements. Validate it with `scripts/validate-candidate-profile.py --profile <profile> --workspace <workspace>`.

Keep three stable slots: external recognition, character with behavioral evidence, and trajectory with current action. Separate verified facts, user statements, inference, and missing information. Search existing evidence first; grill only when one missing fact can change resume direction, and ask one question at a time.

The profile is for the main agent only. It guides positioning, ordering, overstatement checks, missing questions, and narrative-drift checks. It does not change with each JD. Update only affected slots when evidence, career stage, or the user's direction changes.

Profile work is complete when the file validates, uncertainty remains explicit, and no subagent packet contains it.

## Write the resume as arguments

Maintain one structured content source using [schema/resume-data.md](schema/resume-data.md) or the workspace's existing model. Edit only claims supported by the evidence map and preserve approved content outside the requested scope.

Read [guides/writing-tips.md](guides/writing-tips.md) before substantive writing. It is the single source of truth for thesis-led bullets, AI-native framing, ATS vocabulary, mixed-language terms, summary use, visual line rhythm, and interview-drawer boundaries. Use [prompts/interview.md](prompts/interview.md) only to elicit missing facts and [prompts/linkedin-import.md](prompts/linkedin-import.md) only for imported profile text.

Writing is complete when wording, order, numbers, and emphasis are confirmed and every high-signal claim can survive a likely follow-up.

## Render and verify

Prefer the workspace's existing template and build path. Use bundled templates only when building from scratch or changing style. Read [prompts/beautify.md](prompts/beautify.md) for visual cleanup and [prompts/editable-version.md](prompts/editable-version.md) for browser editing.

Follow [references/artifact-pipeline.md](references/artifact-pipeline.md). When the authoritative resume is HTML or CSS, treat it as a print-constrained frontend and read [references/frontend-resume-layout.md](references/frontend-resume-layout.md); use an available frontend testing or debugging skill for rendered QA, and use the PDF skill for the delivered page. Use bundled scripts through `scripts/run-python.sh`.

Rendering is complete when the structured source and every delivered format agree and deterministic plus visual checks pass.

## Freeze the resume before HR review

Read [references/parallel-feedback.md](references/parallel-feedback.md). Create a frozen packet with `scripts/prepare-review-packet.py`, then run [subagents/hr-reviewer.md](subagents/hr-reviewer.md) in fresh context. The packet contains the JD, resume, constraints, and visual artifact only—never `candidate-profile.json`. Validate its JSON with `scripts/validate-review-report.py --report <report> --resume-text <packet>/content/resume-semantic.txt --jd-text <packet>/content/jd.txt`.

Require the isolated reviewer to reconstruct a five-second profile from the packet. After validation, compare its stable candidate image with the main-only candidate abstract and its role-fit clause with the frozen role report. A mismatch is a communication or selection failure in the resume; never fix it by leaking either internal artifact into the reviewer packet.

For review-only work, return the validated HR judgment without adding a parent first-pass review. For edit work, synthesize internal evidence checks, artifact checks, and isolated HR feedback once. If material information is missing, use [references/hr-clarification-grill.md](references/hr-clarification-grill.md). A changed candidate version starts a fresh acyclic review.

When the user asks whether to keep editing, freeze, or make one last micro-adjustment, read [references/final-pass.md](references/final-pass.md) after the validated review. Stop when no must-fix remains; do not turn an evidence gap into a wording exercise.

The skill is complete when the requested output exists, reports validate, accepted and rejected findings have reasons, and resume hooks passed to `grill-interview` match the final resume.

## Attribution

Adapted from `yanliudesign/offer-toolkit-skill` commit `0889e54` under MIT. See [../LICENSE](../LICENSE).
