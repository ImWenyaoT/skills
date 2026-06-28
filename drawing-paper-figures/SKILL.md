---
name: drawing-paper-figures
description: Use when budgeting or producing publication-quality academic paper figures, including Elsevier-style journal figures, CVPR/ICCV/NeurIPS appendix figures, architecture diagrams, Ours-vs-baseline scatters, result stitches, and efficiency plots. Can derive word/figure/palette budgets from references and draw with the bundled matplotlib figkit. Do not use for language review, caption-only edits, or submission packaging.
---

# drawing-paper-figures

A two-phase workflow for journal paper figures.

- **Phase A — BUDGET**: run the stats scripts against a reference-paper corpus to learn what word counts / figure counts / palette colours are normal for your venue.
- **Phase B — DRAW**: use figkit + diagram_primitives + stitch + measure_model + annotate_renders to produce publication-ready figures at 600 dpi.

Reference conventions (RGB-T tracking journal papers) live in `references/`.

---

## Figure Design System

All figures produced by this skill follow these non-negotiable rules:

- **White background** (`#ffffff`) — no grey panels, no dark themes.
- **Vivid multi-color palette** — use the `color_pick` palette from `figkit/palette_base.py`. Pick distinct, saturated hues; never use the matplotlib default cycle.
- **Fonts** — Arial or Helvetica for sans-serif elements (axes, labels, legends); Times New Roman for any serif annotation. Never use DejaVu or Computer Modern in final figures.
- **Resolution** — export at 600 dpi, rounded to integer pixel dimensions. Use `save_fig(fig, out, dpi=600)`.
- **High density** — pack information; do not shrink font sizes to fit. Open a small canvas so text is naturally large, then scale in the paper.
- **Journal figure types** — framework diagrams, module-detail diagrams, PR/SR curves, attribute radars, speed-accuracy scatter/bubble charts, qualitative tracking panels, efficiency tables (as figures when trends matter).

---

## Phase A — Budget

Run these four scripts in order against your reference corpus. All scripts use `uv run` with zero or minimal extra deps.

### 1. Section word-count budget

Profiles word counts per section across all PDFs in a corpus directory.

```bash
uv run scripts/section_wordcount.py \
  --corpus <dir-of-pdfs> \
  --out    <output-dir> \
  [--exclude <regex>]  \
  [--prefix  <string>]
```

Requires `pdftotext` (poppler). No pip deps. Outputs median + IQR per section label so you know how many words to allocate to Introduction, Method, Experiments, etc.

### 2. Figure and table count survey

Counts how many figures and tables appear in the Experiments section of each PDF.

```bash
uv run scripts/reference_fig_table_stats.py \
  --corpus    <dir-of-pdfs>  \
  --text-root <dir-of-txt>   \
  --out       <output.csv>
```

No pip deps. The output CSV lets you set a figure budget before you start drawing (e.g., "most papers in this venue have 7–12 figures and 4–8 tables").

### 3. Palette extraction

Extracts dominant colours from existing figures in a corpus so you can match venue conventions or compare against your chosen palette.

```bash
uv run --with numpy --with pillow \
  scripts/extract_colorpick_palette.py \
  --src       <dir-of-pngs-or-pdfs> \
  --out       <palette.md>           \
  [--n-colors 32]                    \
  [--merge-dist 22]
```

Deps: `numpy`, `pillow`. Outputs a markdown file with hex swatches and RGB values.

### 4. Caption audit

Extracts Figure/Table captions from PDFs as a markdown audit log — useful for checking what caption patterns your venue expects.

```bash
uv run scripts/extract_pdf_fig_tables.py \
  --pdf-dir <dir-of-pdfs> \
  --out     <captions.md>
```

No pip deps. See `references/rgbt_journal_fig_table_captions.md` for pre-run output on 41 RGB-T tracking journals; `references/rgbt_journal_common_fig_table_patterns.md` for the distilled patterns.

---

## Phase B — Draw

### Architecture / framework diagrams (`diagram_primitives.py`)

Provides semantic colours, box drawing, and connector primitives for pipeline diagrams. Use as a library — import and configure coordinates + labels for each new paper; do not rewrite the primitives.

Write a thin per-paper caller (e.g. `your_paper/draw_arch.py`) that imports the module, then run it:

```bash
uv run --with matplotlib python your_paper/draw_arch.py
```

Inside `draw_arch.py`:

```python
import sys
sys.path.insert(0, '/path/to/paper-figures/scripts')

import matplotlib.pyplot as plt
from diagram_primitives import SEMANTIC, draw_box, connect, save_diagram

# SEMANTIC is a dict of role -> hex colour, e.g.:
#   SEMANTIC['TEAL_FILL']   -> light teal (backbone/trunk blocks)
#   SEMANTIC['AMBER']       -> amber fill (conditioning blocks)
#   SEMANTIC['GREEN']       -> green fill (output/refinement head)
#   SEMANTIC['IO_FILL']     -> white (input/output tensor boxes)

fig, ax = plt.subplots(figsize=(10, 4))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# Place boxes: draw_box(ax, xy, w, h, label, fill, stroke, fontsize=9.5)
draw_box(ax, (0.1, 0.4), 0.15, 0.2, 'RGB Encoder',
         fill=SEMANTIC['TEAL_FILL'], stroke=SEMANTIC['TEAL_STROKE'])
draw_box(ax, (0.4, 0.4), 0.20, 0.2, 'Fusion Module',
         fill=SEMANTIC['AMBER'],     stroke=SEMANTIC['AMBER_STROKE'])
draw_box(ax, (0.75, 0.4), 0.15, 0.2, 'Head',
         fill=SEMANTIC['GREEN'],     stroke=SEMANTIC['GREEN_STROKE'])

# Connect: connect(ax, src_xy, dst_xy, kind='fwd'|'cond'|'nograd'|'grad')
# Returns None — do not assign the result.
connect(ax, (0.25, 0.5), (0.40, 0.5), kind='fwd')
connect(ax, (0.60, 0.5), (0.75, 0.5), kind='fwd')

# Save as both PDF and PNG at 600 dpi:
save_diagram(fig, 'figures/framework')
# -> figures/framework.pdf + figures/framework.png
```

Deps: `matplotlib`. The `save_diagram` call writes `.pdf` + `.png` (600 dpi) with the same stem.

For a new paper, copy the coordinate layout section from an existing diagram file, replace labels and `SEMANTIC` keys, and call `save_diagram` with a new stem. Never rewrite the primitives themselves.

### Scatter / performance plots (`figkit/`)

`figkit/` is the shared drawing library. Write a thin per-paper caller (e.g. `your_paper/draw_scatter.py`) that imports the module, then run it:

```bash
uv run --with matplotlib python your_paper/draw_scatter.py
```

Key entry points inside the caller:

```python
import sys
sys.path.insert(0, '/path/to/paper-figures/scripts')

import matplotlib.pyplot as plt
from figkit.palette_base import with_modules
from figkit.plot_helpers  import save_fig, style_axes, scatter_ours_vs_base

# Build a per-paper palette (merges shared base colours with paper-specific module colours):
palette = with_modules(GCM_FILL="#D4E8EB", GCM_STROKE="#2A6478")

fig, ax = plt.subplots(figsize=(5, 4))

# Ours-vs-baseline scatter:
# ours_xy: single (x, y) point; base_xy: list of (x, y) points
scatter_ours_vs_base(
    ax,
    ours_xy    = (60.3, 85.4),
    base_xy    = [(42.1, 78.2), (55.0, 81.5), (38.7, 76.9)],
    ours_label = 'Ours',
    base_labels= ['MethodA', 'MethodB', 'MethodC'],
    annotate   = True,
)

style_axes(ax, xlabel='FPS', ylabel='Precision Rate (%)')
save_fig(fig, 'figures/speed_accuracy.pdf', dpi=600)
```

`save_fig(fig, out_path, dpi=600)` exports at the given dpi (default 600). `scatter_ours_vs_base` uses fixed marker sizes — there is no bubble-size or palette parameter.

### Result stitching (`stitch.py`)

Horizontally concatenates PNG panels for qualitative tracking rows or ablation montages.

```bash
uv run --with pillow scripts/stitch.py \
  --images a.png b.png c.png \
  --out    figures/qualitative_row.png \
  [--labels "GT" "Ours" "Baseline"] \
  [--gap    8]
```

`--labels` adds text headers above each panel. `--gap` sets the pixel gap between panels. Background is white.

Can also be used as a library:

```python
from scripts.stitch import stitch_row
combined = stitch_row([img_a, img_b, img_c], labels=['GT', 'Ours', 'Base'], gap=8)
combined.save('figures/qualitative_row.png')
```

### Efficiency measurement (`measure_model.py`)

Used as a library — the caller owns model instantiation; this module provides the measurement helpers. Write a thin per-paper caller (e.g. `your_paper/measure.py`) that imports the module, then run it:

```bash
uv run --with torch --with numpy --with thop python your_paper/measure.py
```

`--with numpy` silences the "Failed to initialize NumPy" warning from torch. `--with thop` is only needed if you call `measure_flops`; omit it if you only need params and FPS.

For FLOPs-only callers (no thop):

```bash
uv run --with torch --with numpy python your_paper/measure.py
```

Inside `measure.py`:

```python
import sys
sys.path.insert(0, '/path/to/paper-figures/scripts')

from measure_model import count_params, measure_runtime, measure_flops

model = MyTracker(config)

r       = count_params(model)                              # -> {"total_M": float, "trainable_M": float}
latency = measure_runtime(model, (1, 3, 256, 256),
                          device='cpu', iters=50, warmup=5)  # -> 延迟 ms（单次前向均值）
gmacs   = measure_flops(model,   (1, 3, 256, 256))         # -> GMACs（thop MAC数/1e9）；thop未装则 None

print(f"Params: {r['total_M']:.1f}M   延迟: {latency:.2f} ms   GMACs: {gmacs:.2f}")
```

Deps: `torch`, `numpy`; `thop` optional (GMACs only). Do not run this script standalone — write a thin per-paper caller that imports it.

Key return-type notes:
- `count_params` returns a dict — access `r["total_M"]` (already in millions, no `/1e6` needed).
- `measure_runtime` returns latency in milliseconds (not FPS — divide 1000 / latency to get FPS if needed).
- `measure_flops` returns GMACs (thop counts multiply-accumulates; FLOPs ≈ 2 × MACs).

### Render QA annotation (`annotate_renders.py`)

Overlays numbered anchor circles with severity-coloured fix lists onto rendered images, for QA review of figures before submission.

`spec.json` format (load_specs) — a dict keyed by image filename:

```json
{
  "frame_042.png": {
    "title": "Fig 3 架构图 — 修改任务",
    "anchors": [
      [0.25, 0.40, "1"],
      [0.60, 0.55, "2"]
    ],
    "fixes": [
      ["1", "必改", "箭头方向画反，需翻转"],
      ["2", "复核", "连线落点请人眼核查"]
    ]
  }
}
```

`anchors` 每项为 `[x_frac, y_frac, label]`（坐标为相对图像宽高的小数）。`fixes` 每项为 `[label, severity, desc]`。`SEVERITY` 键为中文：`必改` / `复核` / `标签` / `题注` / `样式` / `范围`。

Run command (put images in `renders/`, outputs go to `annotated/`):

```bash
uv run --with pillow --with matplotlib scripts/annotate_renders.py --config spec.json
```

---

## Caption Convention Reference

See `references/` for pre-audited data:

- `rgbt_journal_common_fig_table_patterns.md` — distilled common figure/table patterns from 35 RGB-T tracking journal method papers. Minimum viable set: framework fig + module-detail fig + SOTA table + ablation table + result curves/qualitative + efficiency/attribute supplement.
- `rgbt_journal_fig_table_captions.md` — raw caption audit of 41 PDFs (auto-extracted; verify against PDF before citing).

Iron-law checklist before exporting any figure (from `references/rgbt_journal_common_fig_table_patterns.md §六`):

- Vector format (PDF/EPS/SVG) for line art; PNG only for rasterized renders at ≥ 600 dpi.
- Font ≥ 8pt at final column width — open a small canvas, not a large one with small text.
- Color-blind safe + dual encoding (color + marker shape or linestyle).
- Honest y-axis — no truncation to exaggerate gaps.
- Caption first sentence states the finding, not "Fig. X shows…".
- No chartjunk, no 3D bars, no gradient backgrounds.
- Correct chart type for data shape (time series → line; multi-method comparison → grouped bar; speed-accuracy tradeoff → scatter/bubble; attribute breakdown → radar).

---

## Typical Workflow

```
# 1. Budget phase — run once per corpus
uv run scripts/section_wordcount.py       --corpus refs/ --out budget/
uv run scripts/reference_fig_table_stats.py --corpus refs/ --text-root refs-txt/ --out budget/fig_counts.csv
uv run --with numpy --with pillow scripts/extract_colorpick_palette.py --src refs/ --out budget/palette.md
uv run scripts/extract_pdf_fig_tables.py  --pdf-dir refs/ --out budget/captions.md

# 2. Draw phase — per paper (write thin caller scripts, then invoke via uv)
uv run --with matplotlib python your_paper/draw_arch.py     # imports diagram_primitives
uv run --with matplotlib python your_paper/draw_scatter.py  # imports figkit
uv run --with torch --with numpy --with thop python your_paper/measure.py  # imports measure_model

uv run --with pillow scripts/stitch.py \
  --images renders/seq1.png renders/seq2.png \
  --out figures/qualitative.png \
  --labels 'Ours' 'Baseline'

# 3. QA
uv run --with pillow --with matplotlib scripts/annotate_renders.py --config qa_spec.json
```
