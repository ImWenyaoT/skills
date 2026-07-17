# Answer the Evaluation

Interview answers must be both correct and responsive. First infer what capability the question is evaluating; then choose the answer shape.

## Classify before answering

| Question type | Evaluation intent | Answer shape |
|---|---|---|
| Fundamentals or boundaries | mental model and conceptual precision | definition → boundary → trade-off → brief example |
| Failure diagnosis | fault taxonomy, localization, recovery | clarify symptom → lifecycle stage → likely causes → handling → verification |
| Project evidence | whether the candidate really did the work | concrete incident → diagnosis → decision → fix → evidence → limit or learning |
| System design or transfer | decomposition under new constraints | requirements → constraints → architecture → trade-offs → failure handling → validation |
| Behavioral | judgment and conduct in a real event | STAR or CAR from verified facts |

Ask one disambiguating question only when plausible interpretations require materially different answers. State the likely branches so the question helps the interviewer rather than delaying the answer. Lead with the direct answer; add a project example only after satisfying the requested layer.

## Diagnose Tool Use by lifecycle

“Tool Use failed” is ambiguous. In a live interview, default to one opening clarification:

> “您指的是模型没有发起 Tool Call，还是调用已经发起但执行报错，或者工具返回了结果但 Agent 没有正确使用？”

Ask that clarification aloud and wait for the branch when the interviewer narrows it. A rehearsal answer that merely says “我会先确认” without actually posing the question is incomplete. If the interviewer wants the full picture or declines to narrow it, state the lifecycle briefly and then choose one branch to demonstrate depth. Do not silently answer a preferred interpretation.

For a rehearsal deliverable, output two explicit blocks:

1. **先问面试官：** one direct clarification ending as a question;
2. **如果对方要全景回答：** the concise lifecycle answer.

Distinguish at least these symptoms:

1. **Exposure:** the tool or useful description never reached the model context because discovery, routing, permissions, or schema construction failed.
2. **Selection and call generation:** the model did not choose the tool, chose the wrong tool, or emitted invalid arguments. This is the Model–Harness seam: instructions and schemas shape the model decision; structured validation and bounded retry live in the harness.
3. **Execution:** the call reached the harness but failed through authentication, authorization, transport, timeout, dependency, backend, side-effect, or idempotency problems.
4. **Observation return:** execution occurred, but the result was empty, malformed, truncated, misclassified, or injected into context incorrectly.
5. **Post-tool reasoning and completion:** the model ignored the observation, repeated the call, drew an unsupported conclusion, or stopped without satisfying the task contract.

Use `Agent = model + harness` as a decomposition, not a wall. The harness exposes tool definitions and returns observations; the model selects and emits a structured call; the harness validates and executes it. Failures often occur at this seam.

For the clarified stage, explain observable signals, likely causes, recovery policy, and the check that proves recovery. Tests and traces verify the handling; they do not replace the diagnosis or recovery mechanism.

## Prevent answer hijacking

- Do not pivot to the candidate's favorite project before answering the conceptual or diagnostic core.
- Do not dump every known failure mode when one clarified branch is enough.
- Do not treat a framework name as an explanation; expose state, control flow, and boundary.
- If the interviewer asks for an experienced failure, use one verified incident. If none exists, give the system-level answer and label the missing personal example.
