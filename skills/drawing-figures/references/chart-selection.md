# Chart selection

Which chart form carries which data shape, once the message is settled.

## Contents

- [Pick the form from the data shape](#pick-the-form-from-the-data-shape)
- [When the values span too wide a range](#when-the-values-span-too-wide-a-range)

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
