# 2. Method figures are not drawn by a script

- **Status:** accepted
- **Date:** 2026-08-10

## Context

`drawing-figures` shipped `diagram_primitives.py`, 176 lines of matplotlib for laying out
architecture diagrams: semantic colours, `draw_box`, `connect(kind=…)`, `save_diagram`. It was the
hardest part of the skill to test and had no test.

It also was not how the figures get made. The real loop is: an agent writes an image-generation
prompt, a model renders it, the agent checks the picture and revises the prompt until the dataflow
sits right, a human traces the accepted image into draw.io or PowerPoint by hand, and the agent
then lists what still differs. The agent never draws anything, and there is a step in the middle it
cannot perform.

## Decision

Delete `diagram_primitives.py`. Route architecture and module figures through the loop above, in
`references/method-figures.md`.

Write the architecture down once first — mermaid by default, prose if the architecture wants it —
and keep it beside the paper. The reason is not that the image model needs a spec. An agent is
stateless across conversations, and without the file every new conversation re-reads the model code
to recover what connects to what: slowly, and arriving somewhere slightly different each time. The
file is the state, which is what makes a mechanical reroll loop affordable rather than merely
possible.

The prompt is nine sections and lives in a file, accumulating across rounds. Two of those sections
came from prompts that got a paper accepted and are not obvious: an **allowed-text whitelist**,
which enumerates every string permitted in the image rather than asking for less text, and a
**negative prompt**, which grows by one line each time a roll fails and is the main reason a
fifth-round prompt beats a carefully written first one.

## Consequences

Figure production splits in two, and the evidence contract splits with it. A result figure traces
its pixels to a checkpoint; a method figure has no checkpoint, so what it traces is the topology
back to the code, and the retained source is the written-down architecture rather than a caller
script.

The written architecture has to carry a date saying when it was last checked against the code. A
stale one is worse than none: it is a confident wrong answer that costs nothing to believe, and an
agent handed one will build on it without opening the code that would have contradicted it.

Writing it audits the figure you already have. Doing this for a published paper turned up a
conditioning path drawn as one shared vector where the code has two independent projections fed
different inputs, an operator at the end of the decoder absent from the figure entirely, missing
skip connections, and a block drawn as a lane operator that the code wraps in projections and a
global residual. Some of that is legitimate simplification; some of it is a figure claiming a
topology the model does not have.
