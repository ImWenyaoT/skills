---
name: offer-magic
description: Turn a job into a resume that can win an interview, then prepare answers that hold up. Use for end-to-end job applications that need both resume and interview work.
disable-model-invocation: true
---

# Offer Magic

Route work to the smallest sufficient skill. Read that skill completely and leave the other skill unloaded unless a handoff is required.

## Route the request

- For a job, apply decision, job-only interview-topic prediction, resume, layout, or export, read [grill-resume/SKILL.md](grill-resume/SKILL.md).
- For project explanations, question-bank analysis, interview answers, or mock interviews, read [grill-interview/SKILL.md](grill-interview/SKILL.md).
- For an end-to-end application, run `grill-resume` first and pass only its frozen outputs to `grill-interview`.

Routing is complete when one skill owns the next action.

## Compose a DAG

```text
JD -> grill-resume workspace
        |- main-agent role report
        |- main-only candidate profile
        |- verified resume
        `- HR subagent report
                    \
                     -> frozen handoff -> grill-interview workspace
                                         `- Interviewer subagent report
```

The bundle has exactly two business subagents: `grill-resume` owns the HR Reviewer and `grill-interview` owns the Interviewer. Each reads only its frozen packet and owner skill, returns one structured result to the main agent, and never debates the other.

The main agent may see both workspaces. It owns JD decoding, the main-only candidate profile, sequencing, frozen handoffs, and final synthesis. It never puts `candidate-profile.json` or parent conclusions into a subagent packet.

Composition is complete when:

- every subagent result is validated by its owner skill;
- downstream work consumes frozen artifacts, not chat summaries;
- unresolved facts remain explicit;
- resume claims and interview answers use the same facts and responsibility boundaries.

## Attribution

Adapted from `yanliudesign/offer-toolkit-skill` commit `0889e54` under MIT. See [LICENSE](LICENSE).
