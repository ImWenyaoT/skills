# HR Screening Lenses

Use these lenses to bound judgment, not as required scores. Surface a lens-specific category in `material_findings` only when it reveals a material problem or editing decision. Record positive evidence under existing categories such as `strongest_evidence` or `interview_hook`; do not emit a positive finding merely to prove that every lens was considered.

## Five-second profile

After reading the frozen resume and JD, describe the candidate in one or two sentences: who they are, the one proof worth remembering, and—when a JD exists—why that proof matters for this role. Reconstruct this from the packet. Never ask for or infer the main-only candidate profile.

An unclear or jargon-only description is a resume communication failure. Mark it `partial` or `unclear`; do not repair it with unsupported interpretation.

## 厉害: credible distinctiveness

Judge the feeling created by evidence, not by adjectives or mandatory senior verbs.

- `design`, `initiate`, `lead`, and `build from scratch` imply more judgment and ownership than `deploy`, `implement`, or `integrate`, but only when the stated scope is true.
- A strong ownership verb names a falsifiable object and boundary: what was designed or started, which decision belonged to the candidate, and how another person could verify or challenge it.
- Look for scarce capability at the candidate's career stage: evidence of a decision, mechanism, result, or learning that most comparable applicants cannot show.
- Treat project success as context unless personal causality is evidenced. Never manufacture seniority by upgrading a verb.
- For a first internship, research, projects, coursework, and open source can be solid evidence. Missing prior internships is not itself a weakness unless the JD makes it a gate.

## 取舍: expose the different twenty percent

Most project work is common execution. Compress that shared eighty percent into enough context for a recruiter to follow the story. Spend bullets on the different twenty percent: a consequential judgment, unusual mechanism, hard trade-off, validation boundary, recovery path, result, or learning.

The intro owns shared context, goal, and project boundary. Each bullet should add a distinct thesis and evidence. Keep common work only when it proves a hard requirement, preserves causality, or makes the claim understandable to a non-specialist.

Apply the deletion test: if removing a sentence loses no distinctiveness, credible evidence, narrative role, JD match, or defensible interview hook, merge or remove it. Concision must not delete the evidence that makes a strong claim falsifiable.

## Align: one personal narrative

State the candidate's apparent long-term target in one sentence, then ask what role each major section plays in proving it. Education, research, projects, and other information may contribute different kinds of evidence—recognition, core capability, differentiated judgment, or sustained action—but they should serve one coherent candidate image.

Align is not keyword overlap with one JD. If each experience is individually good but together resembles several unrelated candidates, the narrative is unclear. Across JD variants, the stable candidate image should remain; only the role-fit clause should change.

## Solid: failure-aware proof

Judge whether the resume proves more than a happy-path demo. Look for explicit completion conditions, evaluation coverage, failed cases, recovery, permissions, safety boundaries, reproducible artifacts, or a stated validation limit. A project feels solid when the reader can see how the candidate knows it worked, what remains unproven, and how failure is contained.

Solid is scope-sensitive. Agent evaluation evidence proves Agent reliability only within the tested scenarios; it does not silently prove production scale, full-stack delivery, product adoption, or maintainability. Record strong failure-aware proof under `strongest_evidence` or `interview_hook`. Use `confusion` when a broad claim hides its validation boundary.

## Material findings

Use these categories only for actionable problems:

- `distinctiveness`: ownership, scarcity, falsifiability, or unsupported seniority;
- `selection`: common work, repetition, filler, or a failed deletion test;
- `narrative_alignment`: an experience cannot be assigned a clear role in the candidate's stable narrative.

Do not emit one finding per lens by default. No material issue means no lens-specific finding. A coherent narrative, concise selection, or credible claim needs no matching positive category.
