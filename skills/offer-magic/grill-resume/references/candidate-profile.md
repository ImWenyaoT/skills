# Candidate Profile

Use this main-only model to preserve a stable understanding of the candidate across resume edits. It is not a default resume section and never enters an HR or Interviewer packet.

## Build three slots

1. **Recognition** — universal external signals such as publication, award, promotion, level, selection, or real adoption. A normal project result is not recognition.
2. **Character** — what makes the candidate dependable or likely to grow. Ground every trait in repeated behavior; labels such as “curious” or “fast learner” are conclusions, not evidence.
3. **Trajectory** — who the candidate intends to become and the actions already pointing there. Separate an explicit user goal from the main agent's inference.

Mark every source as `external_artifact`, `candidate_material`, or `user_statement`. Use `verified_fact` only for facts supported by an external artifact, `user_statement` for facts or goals stated by the user, `inference` for a bounded interpretation of behavior, and `missing` when the slot has no defensible content.

## Update adaptively

Read the current resume, workspace profile, evidence, and existing candidate profile before asking anything. Merge duplicate evidence and keep unchanged slots byte-stable.

Grill only when a missing answer can change positioning, ordering, claim strength, or the candidate's long-term direction. Ask one highest-leverage question and state the affected decision. Stop when the user has no such evidence, the remaining gap cannot change the work, or the next question would only improve prose.

The readable abstract is optional even when all slots are supported. Generate it only when it helps the main agent reason about the candidate. Use omitted-subject resume language: recognition, character plus proof, then trajectory plus current action. If recognition is missing, keep the abstract incomplete instead of substituting project delivery.

## Keep it private

Store the model at `.offer-magic/grill-resume/candidate-profile.json` with `visibility: main_only`. The main agent may use it to guide edits and detect narrative drift. Subagents receive only their normal frozen artifacts. A profile sentence becomes visible to them only after the user explicitly chooses to put it in the final resume; before setting `resume_projection` to `drafted` or `included`, register the user statement as a hashed source and save its exact `source` and `quote` as authorization evidence.
