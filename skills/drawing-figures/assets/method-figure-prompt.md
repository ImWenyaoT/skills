<!--
Prompt template for one method figure. This file is the source of truth for the
figure: it accumulates across rounds rather than being retyped, and the two
sections at the bottom exist only because earlier rounds failed.

Keep one of these per figure, beside the mermaid of the model. Derive the topology
in `## Layout` and `## Data-flow constraints` from the mermaid; everything else is
about this figure's composition, which the mermaid does not carry.

Delete the guidance comments once the section is filled.
-->

# <Figure name>: <what it is a figure of>

Draw a <wide landscape / 4:3 / …> figure (about <16:7>) on a pure white background at 600 dpi.
The figure shows <one paragraph: the path through the figure, entry to exit, in words>.

## Style

<!-- Composition, and what must NOT frame it. Negative style constraints belong here:
     "no large outer container", "no panel-card framing", "never a bottom thumbnail strip". -->

- Continuous <left-to-right / top-down> composition; no large outer container, no panel-card framing.
- <Which lane holds what, if the figure has lanes.>
- <What an operator looks like: slab, chip, glyph. What a gate looks like. What an activation looks like.>
- Format: PNG, 600 dpi, white background. Aspect about <16:7>. Clean sans-serif font, horizontal text only.

## Palette

<!-- A hex per element role and a weight in points per arrow kind. State BOTH the colour and
     the dash pattern: image models honour "dashed" far more reliably than a colour name. -->

- <Role> slab: `#RRGGBB`. <Role> slab: `#RRGGBB`.
- <Edge kind> arrow: `#RRGGBB`, solid <1.4> pt. <Edge kind> arrow: `#RRGGBB`, dashed <1.0> pt.
- Main data-flow arrow: dark gray `#3A3A3A`, 1.4 pt solid.

## Layout

<!-- An ASCII diagram of this figure's composition. Its topology comes from the mermaid;
     what it adds is where things sit on the canvas. -->

```
<ascii layout>
```

## Region rules

### <Region name>

- <What this region contains, in the order it contains it.>

## Embedded visual effects

<!-- Where real image tiles go. Inline at flow nodes, never collected into a strip. -->

- <Which node carries which real tile, and roughly how wide.>

## Allowed text

<!-- An exhaustive whitelist: these strings and no others. Not a length limit — an enumeration.
     It stops the model inventing plausible labels, and it is the exact list the person tracing
     the figure retypes, because the model's rendered text is always nonsense. -->

`<label>`, `<label>`, `<shape>`, `⊕`, `⊙`, `σ`, `❄`.

## Data-flow constraints

<!-- The topology in prose, as absolutes. This is where the figure is made correct rather than
     pretty. Say exact orders, where each branch starts and ends, and what a line must never touch. -->

- Main flow order: `<A → B → C → D>`.
- <Module> sits after <X> and before <Y>.
- The <branch> starts only at <exact node>, not at <the plausible wrong one>, and ends at <node>.
- <Which lines never touch which regions.>

## Negative prompt

<!-- Enumerated failure modes, one phrase each, added every time a round fails. This section only
     grows, and it is the main reason a fifth-round prompt beats a carefully written first one. -->

`<observed failure>, <observed failure>, panel-card layout, large outer container frame, bottom
thumbnail strip, legend box, figure title banner, bottom caption paragraph, photorealistic,
hand-drawn, sketch, watermark, vertical text, hex color codes shown as text`
