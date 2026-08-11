# Method figures

The overall architecture figure and each module mechanism figure. A paper usually has several —
one for the pipeline and one per contributed block.

These are the figures with **no data behind them**. Every other figure is produced by Python
running over experiment artifacts; a method figure's content is the structure of your model, which
lives in the code. It goes through an image model and then through a human tracing the result, and
the agent's work sits on both sides of that handoff.

## Contents

- [The loop, and where the agent is not in it](#the-loop-and-where-the-agent-is-not-in-it)
- [1. Give the agent state](#1-give-the-agent-state)
- [2. Write the prompt](#2-write-the-prompt)
- [3. Review each returned image, dataflow first](#3-review-each-returned-image-dataflow-first)
- [4. Keep a render ledger](#4-keep-a-render-ledger)
- [5. Hand off for tracing](#5-hand-off-for-tracing)
- [6. Correct the traced file](#6-correct-the-traced-file)

## The loop, and where the agent is not in it

1. The agent writes the **model** down once, as mermaid or as prose.
2. The agent writes a **prompt** per figure, deriving its topology from the mermaid.
3. The human runs the prompt through an image model and brings the picture back. The agent marks
   up what is wrong and revises the prompt. Repeat until the dataflow is right.
4. **The human traces the accepted image** into draw.io or PowerPoint. The agent does not
   participate in this step and should not offer to.
5. The human brings the traced file back. The agent lists what still differs.

Two artifacts, not one, and they do different jobs:

- **The mermaid is the model.** One per model, reused by every method figure and every future
  conversation.
- **The prompt is the figure.** One per figure, and it is the source of truth for that figure —
  the accumulated result of every round of review, not a message you retype each time.

## 1. Give the agent state

An agent is stateless across conversations. It starts every one of them knowing nothing about your
model, and the only way it learns the architecture is by reading the code — slowly, at the cost of
a large part of the window, and arriving somewhere slightly different each time. **Write the
architecture down once and that stops.** The file is the state: the next conversation, and the next
agent, loads it in one read.

That is what makes the rest of this loop affordable. Rerolling a prompt is mechanical and
repetitive by nature, and it is only cheap if the expensive part — knowing what connects to what —
was paid once and kept. Without the file, every round of a mechanical loop re-derives the same
understanding before it can do the five minutes of actual work.

**Mermaid is the default form, not the requirement.** It is diffable, it renders, and its edge
kinds line up with the prompt and the palette, so it is what
[`assets/architecture-template.mmd`](assets/architecture-template.mmd) starts you from. A prose
description works too if that is what the architecture wants. What the form has to give you is the
same three things: every module named as the code names it, every connection stated, and a date
saying when it was last checked against the source.

That date is not bookkeeping. A stale file is worse than none — it is a confident wrong answer that
costs nothing to believe, and an agent given one will build on it without ever opening the code
that would have contradicted it. Revise it whenever the architecture changes.

**Writing it also audits the figure you already have.** Reading the forward pass and writing down
what it actually does is the only cheap way to find out that the published figure says something
else. On a real accepted paper this step turned up a conditioning path drawn as one shared vector
broadcast to two consumers where the code has two independent projections fed different inputs, an
operator sitting at the end of the decoder that the figure omits entirely, missing skip
connections, and a block drawn as a lane operator that the code wraps in projections and a global
residual. Some of those are legitimate simplification. Some are the figure claiming a topology the
model does not have, and a reviewer who reads the code finds them.
[`assets/example-hgd-net.mmd`](assets/example-hgd-net.mmd) is that mermaid, for reference on what
the output looks like at real complexity.

Rules that make it usable as state rather than a sketch:

- **Every node carries its tensor shape.** The shape is what a reader checks and what a traced file
  most often gets wrong.
- **Name nodes after the real modules** — the identifiers in the code. No `Module A`.
- **The whole model, not one block's internals.** A module figure gets its own mermaid if it needs
  one, but the overall graph stays one screen.
- **Mark the edge kinds** — `fwd`, `cond`, `no_grad`, emphasis — because those are what the prompt,
  the review, and the traced file all have to agree on.

## 2. Write the prompt

The prompt has nine sections. They are in this order because each one constrains the next, and the
last two exist only because earlier rounds failed.

| Section | What goes in it |
|---|---|
| Title and summary | One line naming the figure, then one paragraph: what it shows, aspect ratio, background. |
| `## Style` | Composition: direction, lanes, what is a slab and what is a glyph, and what must **not** frame the figure. |
| `## Palette` | A hex per element role and a line weight in points per arrow kind. Image models honour "dashed" more reliably than a colour name, so say both. |
| `## Layout` | An ASCII diagram of this figure's composition. Derive its topology from the mermaid; the layout adds where things sit on the canvas, which the mermaid does not carry. |
| `## Region rules` | One `###` per region, spelling out what each contains. |
| `## Embedded visual effects` | Where real image tiles sit — inline at flow nodes, not collected into a strip. |
| `## Allowed text` | **An exhaustive whitelist of every string permitted in the image.** |
| `## Data-flow constraints` | The topology in prose: exact orders, where each branch starts and ends, and what a line must never touch. |
| `## Negative prompt` | Enumerated failure modes seen in earlier rolls. |

Three of those carry most of the weight.

**The allowed-text whitelist is not a length limit.** It is an enumeration: these strings and no
others. It stops the model inventing plausible labels, and it hands the person tracing the figure
the exact strings to retype — which they must, because an image model renders text as
plausible-looking nonsense no matter how carefully it is asked.

**Data-flow constraints are where the topology is enforced**, and they are worth writing as
absolutes: "SRC sits after Stem and before Down1", "the bridge starts only at the last slab, not a
mid-block", "the frozen guidance lines never touch the bridge". The layout ASCII shows the
topology; these sentences make each part of it non-negotiable.

**The negative prompt is the accumulated learning of the loop.** Every round that fails adds a line
to it, phrased as the specific thing that went wrong — `AdaLN1 placed after MSA`, `twelve separate
block expansions`, `bottom thumbnail strip`, `legend box`. It grows monotonically and it is the
main reason a prompt on its fifth round outperforms a prompt written well the first time.

## 3. Review each returned image, dataflow first

Check in this order and stop at the first failure — a picture with the wrong topology does not need
a style comment.

1. **Node inventory.** Every node appears exactly once. Nothing invented, nothing dropped. Image
   models add plausible boxes; a module that is not in the mermaid is not in the paper.
2. **Edge inventory and direction.** Every edge exists, between the right pair, the right way.
3. **Order along the trunk.** The sequence matches the data-flow constraints.
4. **Branch attachment points.** Each branch starts and ends where the constraints say.
5. **Edge style** carries the right semantics: dashed where the model detaches or conditions.
6. **Text against the whitelist.** Anything not on it is a defect, however plausible it looks.
7. **Only now**, legibility and style.

`scripts/annotate_renders.py` produces the review artifact: the render with numbered anchors and a
severity-coloured fix list, one image you can hand back. Severities are `blocker`, `verify`,
`label`, `caption`, `style`, `scope`; an unrecognised one raises rather than painting a grey badge.

Then revise the prompt rather than only reporting the complaint, and **change one thing per round**:
an image model rerolls everything on every request, so a prompt that moved in three places tells
you nothing about which move worked.

## 4. Keep a render ledger

Every returned image gets a row: file, which prompt version produced it, which image model, a score,
a status of `reviewing` / `picked` / `rejected`, and a note. Append; never overwrite a row.

It costs a line and it answers the questions that otherwise get re-litigated: which model produced
the one you kept, whether the last three rounds actually improved anything, and which prompt
version the figure in the manuscript came from.

## 5. Hand off for tracing

When the dataflow passes checks 1–4, say so plainly and stop. The human traces the accepted image.

What carries over is the **layout**: what sits where, how the trunk runs, where branches attach.
What does not carry over is any pixel of text or colour — those come from the whitelist and the
palette. [`assets/architecture-template.drawio`](assets/architecture-template.drawio) starts the
tracing from the palette rather than from draw.io's defaults.

Hand over: the mermaid, the accepted render, the prompt's allowed-text list, and the palette in
`scripts/figkit/palette_base.py`.

## 6. Correct the traced file

Check it against the mermaid and the data-flow constraints, the same list in the same order. Then
the things only a real vector file can get right:

- Every label is real text, spelled correctly, and on the allowed-text list.
- Tensor shapes are present and correct.
- Fills and strokes come from the palette; one hue per semantic role across the whole paper.
- Fonts are Arial or Helvetica, at least 8 pt **after** scaling to column width.
- Arrowheads are consistent, and dashed still means what it meant in the mermaid.
- Export is vector: PDF from draw.io, or PDF from PowerPoint.

Say what to change and where. This is the round where the figure gets finished, so the list is
exhaustive rather than prioritised — the human is doing one editing pass, not five.
