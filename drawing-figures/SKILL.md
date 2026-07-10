---
name: drawing-figures
description: Publication figure budgeting and production for academic papers, including 论文绘图/画图/架构图/结果图: reference-derived budgets, Elsevier/CVPR/ICCV/NeurIPS figures, diagrams, plots, result stitches, and publication-ready exports. Do not use for language review, caption-only edits, or submission packaging.
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

When a venue or journal is named, read its current artwork guide first and record its file type,
physical size, resolution, colour-mode, and font requirements. Use
[references/publication-artwork.md](references/publication-artwork.md) to classify and validate
the output; do not transplant one venue's requirements into another.

## Figure design system

- White background (`#FFFFFF`); no dark theme, grey panel, gradient, 3D bar, or chartjunk.
- Use distinct, saturated colours from `scripts/figkit/palette_base.py`, never matplotlib's
  default cycle. For the CARE-Track look, use `CARETRACK_COLORPICK` from
  `scripts/figkit/caretrack_palette.py`.
- Use Arial or Helvetica for sans-serif elements and Times New Roman for serif annotations.
  Final figures must not depend on DejaVu or Computer Modern.
- Prefer PDF/EPS/SVG for vector-native plots and diagrams. For raster work, the target venue's
  artwork class controls DPI; 600 dpi is only the fallback when no stronger rule is known.
- Design at final column size. Keep text at least 8 pt and strokes/symbols legible; use a compact
  canvas instead of shrinking text on an oversized canvas.
- Encode meaning with colour plus marker shape, line style, label, or another redundant cue.
- Use honest axes and a chart type appropriate to the data shape.
- Preserve the data and caller script behind analytical figures. Never synthesize missing
  experimental or observed-image evidence.

## References

- [Budget workflow](references/budget-workflow.md): commands, dependencies, outputs, and Phase A
  completion criteria.
- [Figure script reference](references/figure-script-reference.md): diagram, plot, stitch,
  measurement, and annotation APIs with runnable examples.
- [Publication artwork](references/publication-artwork.md): artwork classification and export QA.
- [RGB-T common patterns](references/rgbt_journal_common_fig_table_patterns.md): distilled figure
  set and visual conventions from journal papers.
- [RGB-T caption audit](references/rgbt_journal_fig_table_captions.md): auto-extracted caption
  evidence; verify against the source PDF before citing.

## Completion criteria

Phase A is complete only when its budget records section word counts, figure/table counts,
palette, and caption patterns, or explicitly records which corpus artifact was unavailable.

For **every final figure**, report this evidence contract:

1. **Artifact path** — the canonical output and retained source/data/caller path.
2. **Format evidence** — vector status for PDF/EPS/SVG, or raster format, physical dimensions,
   pixel dimensions, and effective DPI against the venue artwork class.
3. **Design-system check** — font family/size and palette/contrast/dual-encoding result.
4. **Paper linkage** — figure number, manuscript section or paragraph that cites it, and caption
   path/text status; confirm the caption's stated finding matches the figure and manuscript text.

Done means every item above is concrete and checked, the manuscript rendering is legible at final
size, each symbol/abbreviation is explained, and no unresolved render-QA blocker remains.
