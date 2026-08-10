# Architecture diagrams

A paper has two kinds of figure. Every other one is made from experiment artifacts by Python that
runs; **this one has no data behind it at all** — its content is the structure of your model, which
lives in the code. It goes through an image model and then through a human tracing the result, and
the agent's work sits on both sides of that handoff.

**Write the mermaid first, and keep it.** Not mainly as a spec for the image model — as the
architecture in a form an agent can load in one read. Without it, every new conversation and every
switched agent starts by reading the model code again to recover what connects to what, which is
slow, and which quietly produces a slightly different understanding each time. The mermaid is that
lookup, cached, in a file you can diff. Everything downstream — the prompt, the review of each
returned image, the pass over the traced file — is cheap only because it starts from a structure
nobody had to re-derive.

## Contents

- [The loop, and where the agent is not in it](#the-loop-and-where-the-agent-is-not-in-it)
- [1. Write the diagram as mermaid](#1-write-the-diagram-as-mermaid)
- [2. Derive the image prompt from the mermaid](#2-derive-the-image-prompt-from-the-mermaid)
- [3. Review each returned image, dataflow first](#3-review-each-returned-image-dataflow-first)
- [4. Hand off for tracing](#4-hand-off-for-tracing)
- [5. Correct the traced file](#5-correct-the-traced-file)

## The loop, and where the agent is not in it

1. The agent writes the diagram as **mermaid**.
2. The agent derives an **image-generation prompt** from it.
3. The human runs the prompt through an image model and brings the picture back. The agent checks
   it against the mermaid and revises the prompt. Repeat until the dataflow is right.
4. **The human traces the accepted image** into draw.io or PowerPoint. The agent does not
   participate in this step and should not offer to.
5. The human brings the traced file back. The agent lists what still differs from the mermaid.

The mermaid is the single source of truth across all five. The generated image is one rendering of
it, the traced file is a second, and both are checked against the same text. That is what makes
"the dataflow is correct" a thing you can verify rather than squint at.

It outlives the figure, too. Keep it in the paper's workspace and revise it whenever the
architecture changes: the next agent to work on this paper reads the mermaid instead of the model
code, and a mermaid that no longer matches the code is worse than none — it is a confident wrong
answer that costs nothing to believe. A traced file whose mermaid was never revised is a figure
nobody can check.

## 1. Write the diagram as mermaid

Start from [`assets/architecture-template.mmd`](assets/architecture-template.mmd). It fixes the
edge vocabulary so the four arrow kinds survive every stage of the loop:

| Edge | Mermaid | Means |
|---|---|---|
| `fwd` | `-->` | Standard forward data flow |
| `cond` | `-. cond .->` | Conditioning injected from the side |
| `nograd` | `-. no_grad .->` | Detached, discrete, or routed — no gradient |
| `grad` | `==>` | Backward gradient, or a path the figure emphasises |

Rules that make the mermaid usable as a spec rather than a sketch:

- **Every node carries its tensor shape** in the label, because the shape is what a reader checks
  and what the traced file most often gets wrong.
- **Name nodes after the real modules.** No `Module A`. If the paper has no name for it, that is a
  gap in the paper, not a placeholder to draw.
- **One diagram, one thing.** The overall architecture and the internals of one block are two
  figures. A mermaid that needs a scrollbar is two mermaids.
- **Declare the direction explicitly** (`flowchart LR` or `TD`) — it is the first thing the image
  model gets wrong and the first thing you will check.

## 2. Derive the image prompt from the mermaid

The prompt is generated from the mermaid, not written freehand, so that what you asked for and
what you check against cannot drift apart. Walk the mermaid and state, in this order:

1. **Canvas and direction** — "a clean architecture diagram on a white background, flowing left to
   right", matching the mermaid's declared direction.
2. **The trunk, in order** — every node along the main path, named, in sequence, with its shape.
3. **The branches** — where each leaves the trunk and where it rejoins.
4. **Edge semantics** — solid for forward, dashed for conditioning and for detached paths, and say
   which arrows are which. Image models honour "dashed" far more reliably than they honour a
   colour name.
5. **Style** — rounded rectangles, a light fill with a darker stroke of the same hue, no gradients,
   no 3D, no drop shadows, no background scenery.
6. **Text** — ask for **minimal text**, or none at all beyond short module names.

That last one is not a style preference. Image models render text as plausible-looking nonsense,
and every label in the generated picture is going to be retyped during tracing anyway. Asking for
less text buys a cleaner layout and removes the temptation to accept a figure whose labels are
subtly wrong.

## 3. Review each returned image, dataflow first

Check in this order and stop at the first failure — a picture with the wrong topology is not worth
a style comment.

1. **Node inventory.** Every mermaid node appears exactly once. Nothing invented, nothing dropped.
   Image models add plausible boxes; a module that is not in the mermaid is not in the paper.
2. **Edge inventory and direction.** Every mermaid edge exists, between the right pair, pointing
   the right way.
3. **Order along the trunk.** The sequence matches. This is the one the user is usually asking
   about, and it is the one that is expensive to fix after tracing.
4. **Branch attachment points.** Each branch leaves and rejoins where the mermaid says.
5. **Edge style** carries the right semantics: dashed where the mermaid says `cond` or `nograd`.
6. **Only now**, legibility and style.

Report what failed and give the **prompt revision**, not just the complaint. Change one thing per
round: an image model rerolls everything on every request, so a prompt that changed in three
places tells you nothing about which change worked.

## 4. Hand off for tracing

When the dataflow passes 1–4, say so plainly and stop. The human traces the accepted image into
draw.io or PowerPoint.

What carries over from the generated image is the **layout**: what sits where, how the trunk runs,
where branches attach. What does not carry over is every pixel of text and every colour — those
come from the mermaid and from the figure design system, not from the model's rendering.

Hand over: the mermaid, the accepted image, and the palette
(`scripts/figkit/palette_base.py`). [`assets/architecture-template.drawio`](assets/architecture-template.drawio)
starts the tracing from the right styles rather than draw.io's defaults.

## 5. Correct the traced file

The traced file is checked against the mermaid, exactly as the generated image was — the same list,
in the same order. Then the things only a real vector file can get right:

- Every label is real text, spelled correctly, matching the mermaid's node names.
- Tensor shapes are present and correct.
- Fills and strokes come from the palette; one hue per semantic role across the whole paper.
- Fonts are Arial or Helvetica, at least 8 pt **after** the figure is scaled to column width.
- Arrowheads are consistent, and dashed still means what it meant in the mermaid.
- Export is vector: PDF from draw.io, or PDF from PowerPoint.

Say what to change and where. This is the round where the figure gets finished, so the list should
be exhaustive rather than prioritised — the human is doing one editing pass, not five.
