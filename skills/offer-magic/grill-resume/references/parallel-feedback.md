# Parallel Feedback

Use one standard under different information exposure. The external HR reader is a fresh instance of the same skill, not a separate rubric.

## Route review-only requests

When the user asks only to review, audit, or critique a resume, keep judgment outside the parent session:

1. Let the parent locate inputs and create the frozen packet.
2. Spawn one fresh-context HR subagent. Use `fork_turns="none"` in Codex or the equivalent fresh subagent in Claude Code.
3. Instruct it to apply `SKILL.md` and `references/offer-loop.md`, read only the frozen packet, and write the structured report.
4. Validate the report with `scripts/validate-review-report.py`.
5. Return the validated HR report. The parent may format or summarize it, but must not add an independent review or edit the resume.

Use this bounded task prompt, replacing paths only:

> Use `$grill-resume` to review the frozen resume packet at `<packet>`. Read content inputs before the visual preview. Do not inspect the parent conversation, project repositories, prior drafts, sibling skills, or files outside the packet and `grill-resume`. Do not modify the resume. Write the required JSON report to `<report>` and return only success or failure plus its path.

If no JD exists, continue with general screening quality and mark role-specific hard requirements as unavailable. Do not block a generic “review my resume” request on a missing JD.

Calibrate the review to the declared application type and candidate stage. For a first-internship candidate, evaluate whether projects and research prove readiness; do not downgrade the resume merely for lacking prior internships unless the target role makes that a real gate. As professional evidence accumulates, expect internships and full-time work to take increasing priority.

## Freeze one candidate version

Build the candidate artifact before review. Create a compact packet with `scripts/prepare-review-packet.py`; never send raw PDF bytes or a CSS-heavy HTML file when normalized text and a preview suffice.

The packet may contain:

- JD text;
- semantic resume text extracted from HTML;
- delivered text extracted from the PDF when `pdftotext` is available;
- section order, bold anchors, and links extracted from HTML;
- a downscaled redacted preview for visual review;
- objective constraints such as application type, language, page limit, and minimum font size;
- hashes tying every file to the frozen candidate version.

Exclude editing history, parent conclusions, evidence matrices, prior drafts, desired findings, and project repositories. The parent retains those for fact checking.

## Run an acyclic edit review

For edit or tailor requests, use this DAG for each candidate version:

```text
frozen candidate
  ├─ internal review: full context and evidence
  ├─ deterministic artifact checks
  └─ external review: isolated packet, fork_turns="none"
             ↓
       parent synthesis
```

Run the three branches independently where possible. Let each report only to the parent. Do not pass one reviewer’s conclusions to another reviewer. For review-only requests, omit the internal-review branch: the parent is an orchestrator, not a reviewer.

The external reader first assesses normalized text for ATS parsing, hard-condition match, evidence visibility, clarity, and overfitting. It then uses the preview and structural metadata to assess hierarchy, density, emphasis, and scan path. This is one review task with two ordered passes, not two competing standards.

## Use one report contract

Both feedback lanes return schema version 2 with `five_second_profile`, `recommendation`, `confidence`, `material_findings`, and `clarification_requests`. The profile contains `status`, `text`, `resume_quotes`, and `jd_quotes`. Its text uses at most two sentences and 100 non-whitespace characters to state who the candidate is, the strongest visible proof, and—when a JD exists—the direct role fit. A `clear` profile cites distinct resume evidence for identity and strongest proof. A `partial` or `unclear` profile preserves the communication failure instead of filling it with inference.

Read [hr-screening-lenses.md](hr-screening-lenses.md) before writing the report. Apply its four lenses internally; do not create mandatory lens scores. Put only material, actionable judgments in `material_findings`; each item contains `category`, `finding`, `why_it_matters`, and an exact `resume_quote` or `jd_quote` from the frozen packet. The report covers:

- five-second candidate profile and direct role fit;
- advance / hold / reject recommendation with confidence;
- hard requirements met, adjacent, missing, or irrelevant;
- whether evidence strength and section priority fit the application and candidate stage;
- strongest visible evidence;
- confusing or weak claims;
- over-attribution, success theater, or claims whose validation boundary is hidden;
- whether failure handling, evaluation, and stated limits make the strongest project evidence solid;
- whether project relevance, contribution, remaining gap, and learning are credible interview hooks;
- suspected keyword stuffing or single-JD overfitting;
- structure and layout findings;
- exact frozen-text grounding for every material claim.

Use `distinctiveness`, `selection`, or `narrative_alignment` only when those lenses reveal a material problem or editing decision. Put positive evidence under `strongest_evidence` or `interview_hook`. Do not emit one finding for each lens by default.

The external lane writes JSON matching the keys enforced by `scripts/validate-review-report.py`. Validate it against both `content/resume-semantic.txt` and `content/jd.txt` before synthesis.

When the reviewer cannot make a material judgment from the packet, require a `clarification_requests` entry instead of a guess. Each entry identifies the blocked judgment, known evidence, exact unknown, why it changes the outcome, and one candidate-facing question. The reviewer never interviews the user directly. The parent resolves these entries through [hr-clarification-grill.md](hr-clarification-grill.md), then freezes a new packet if the answer changes resume content or review context.

## Synthesize once

Use repository evidence to resolve factual disputes. Give isolated-reader confusion high weight because it measures communication failure, even when the underlying fact is correct. Reject advice that violates truth, user constraints, or verified layout behavior.

Record each material finding as accepted or rejected with one reason. If accepted changes create a new candidate version, render it and start a fresh DAG. Never reopen the previous reviewer for argument.
