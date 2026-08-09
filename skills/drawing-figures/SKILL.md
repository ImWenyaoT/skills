---
name: drawing-figures
description: 'Publication figure budgeting and production for academic papers, including 论文绘图/画图/架构图/结果图: reference-derived budgets, Elsevier/CVPR/ICCV/NeurIPS figures, diagrams, plots, result stitches, and publication-ready exports. Covers scatter plots, 600 dpi exports, and baseline-comparison panels. Do not use for language review, caption-only edits, or submission packaging.'
license: MIT
compatibility: Requires Python 3 with matplotlib and Pillow.
---

# drawing-figures

Produce publication figures through two independently usable phases. This skill owns figure
budgeting and figure artifacts; it does not own manuscript prose review, caption-only rewriting,
or submission packaging.

## Route the work

1. **Phase A — Budget**: use when a reference corpus is available and the paper still needs
   evidence-based targets for section length, figure/table count, palette, or caption patterns.
   Follow [references/budget-workflow.md](references/budget-workflow.md).
2. **Phase B — Draw**: use when producing or revising architecture diagrams, analytical plots,
   qualitative panels, efficiency figures, or render-QA annotations. Follow
   [references/figure-script-reference.md](references/figure-script-reference.md).
3. Run both phases when planning and producing a new paper's figure set. Skip Phase A when the
   venue requirements and figure plan are already settled.

Export by the default in [references/publication-artwork.md](references/publication-artwork.md) —
vector wherever the figure can be vector, 600 dpi otherwise, designed at final column width. That
covers CVPR, ICCV, NeurIPS, and an ordinary Elsevier or IEEE submission. Read a venue's artwork
guide only when that venue raises one of the four things that actually vary: separate artwork
files, a stated DPI above 600, CMYK, or a physical size limit in millimetres.

## Figure design system

- White background (`#FFFFFF`); no dark theme, grey panel, gradient, 3D bar, or chartjunk. One
  figure carries one message.
- Use distinct, saturated, colour-blind-safe colours from `scripts/figkit/palette_base.py`, never
  matplotlib's default cycle.
- Use Arial or Helvetica for sans-serif elements and Times New Roman for serif annotations.
  Final figures must not depend on DejaVu or Computer Modern.
- Prefer PDF/EPS/SVG for vector-native plots and diagrams; 600 dpi for raster work.
- Design at final column size. Keep text at least 8 pt and strokes/symbols legible; use a compact
  canvas instead of shrinking text on an oversized canvas.
- Encode meaning with colour plus marker shape, line style, label, or another redundant cue, so the
  figure still reads in greyscale print.
- Use honest axes and a chart type appropriate to the data shape. Do not truncate an axis to
  exaggerate a gap; label a non-zero origin explicitly, and share one scale across subplots that
  plot the same quantity.
- Name every axis, legend entry, and annotation after the real method or metric. Ship no
  `Module A` / `X` / `Y` placeholders.
- Open each caption with the finding rather than "Fig. X shows …", so the figure is understandable
  away from the body text.
- Preserve the data and caller script behind analytical figures. Never synthesize missing
  experimental or observed-image evidence.

## References

- [Budget workflow](references/budget-workflow.md): commands, dependencies, outputs, and Phase A
  completion criteria.
- [Chart selection](references/chart-selection.md): which chart form fits which data shape, what to
  do when values span orders of magnitude, and the five things an architecture diagram must specify
  before it is drawn.
- [Figure script reference](references/figure-script-reference.md): diagram, plot, stitch,
  measurement, and annotation APIs with runnable examples.
- [Publication artwork](references/publication-artwork.md): artwork classification and export QA.

## Completion criteria

Phase A is complete only when its budget records section word counts, figure/table counts,
palette, and caption patterns, or explicitly records which corpus artifact was unavailable.

For **every final figure**, report this evidence contract:

1. **Artifact path** — the canonical output and retained source/data/caller path.
   For comparison figures, trace the "Ours" panel to the checkpoint or run that produced
   its pixels — read the generator script's data paths, not the panel label. A label
   is a claim, not evidence: panels inherited from a related project, an earlier model,
   or an unversioned asset directory can carry your method's name over another model's
   output, and the tables and figures then report different models without any visible
   error. If a panel's pixels cannot be traced to your own run, regenerate it; if its
   numbers must match a table, generate both from the same checkpoint.
2. **Format evidence** — vector status for PDF/EPS/SVG, or raster format, physical dimensions,
   pixel dimensions, and effective DPI against the venue artwork class.
3. **Design-system check** — font family/size and palette/contrast/dual-encoding result.
4. **Paper linkage** — figure number, manuscript section or paragraph that cites it, and caption
   path/text status; confirm the caption's stated finding matches the figure and manuscript text.

Done means every item above is concrete and checked, the manuscript rendering is legible at final
size, each symbol/abbreviation is explained, and no unresolved render-QA blocker remains.
