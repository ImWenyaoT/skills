# Chart selection and architecture-diagram specification

What to draw once the message is settled: which chart form carries which data shape, and what an
architecture diagram has to specify before anyone opens a drawing script.

## Contents

- [Pick the form from the data shape](#pick-the-form-from-the-data-shape)
- [When the values span too wide a range](#when-the-values-span-too-wide-a-range)
- [Specify an architecture diagram before drawing it](#specify-an-architecture-diagram-before-drawing-it)

## Pick the form from the data shape

| Form | Use it for |
|---|---|
| Vertical grouped bars | The standard comparison against the state of the art, with a moderate number of entries and short labels. |
| Horizontal bars | Long method names, or many entries. |
| Pareto front | Two metrics that trade against each other. |
| Radar | Multi-dimensional capability at a glance. |
| Stacked bars | How one overall metric decomposes. |
| Line with a confidence band | Training curves: loss, accuracy. |
| Line with an inset zoom | Small differences late in convergence. |
| Scatter with a fit | A trend across discrete measurements. |
| ROC curve | Binary classification with reasonably balanced classes. |
| Precision-recall curve | Binary classification under class imbalance — prefer this over ROC there. |
| Heatmap | Matrix data, confusion matrices, multi-task performance grids. |
| Scatter | The relationship between two continuous variables. |
| Bubble | A scatter carrying a third dimension, such as parameter count or compute cost. |
| Violin | The shape of a distribution. |
| Box | Median, outliers, and range. |
| Donut or pie | Category shares — prefer the donut. |
| Dual y-axis | Two variables on different scales. |
| Bar plus line | Foreground performance against background context such as sample counts. |
| Facet grid | Too many variables for one panel; split into small multiples. |

## When the values span too wide a range

- Keep the raw visual impression → break the axis, and label the break.
- The values cross orders of magnitude → log scale.
- The relative gain is the point → normalise.

Whichever you choose, the axis stays honest: no truncation that exaggerates a gap, and a non-zero
origin is labelled explicitly.

## Specify an architecture diagram before drawing it

Write these five out before touching a drawing script. The specification is what makes the diagram
reviewable while it is still cheap to change.

1. **Layout** — module arrangement left-to-right or top-to-bottom, with the trunk flow and the
   branches identified.
2. **Each module** — name, fill colour, stroke colour, the key operators inside it, and the tensor
   shape from input to output.
3. **Arrow semantics** — forward flow, conditional injection, `no_grad` or routing, gradient or
   emphasis flow. Distinguish them by solid against dashed, and by line width.
4. **Annotations** — where tensor shapes, key hyperparameters, and operator symbols (⊙, ⊕, concat)
   are placed.
5. **Acceptance** — white background, still legible after scaling into a two-column layout, no
   decoration that carries no meaning, and a palette consistent with the paper's other figures.

Draw only the structure the paper actually has; invent no module. One diagram carries one thing —
keep the overall architecture and a module's internals in separate figures.
