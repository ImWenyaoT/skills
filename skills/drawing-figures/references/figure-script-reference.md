# Figure Script Reference

Write thin per-paper callers around these reusable scripts. Keep paper-specific coordinates,
labels, data, and model construction outside the shared modules.

## Running these scripts in your environment

The commands below use `uv run --with …`, which fetches the dependency per run and
needs nothing installed. That is the zero-setup path, and it is what the examples
show.

**If you already have an environment with these packages — conda, a virtualenv,
anything — run the script with your own Python instead:** `python scripts/<name>.py …`.
Prefer that when the script has to see your data, your checkpoints, or anything else
your environment resolves, because `uv run --with` builds a *separate* ephemeral
environment: it will not see what your conda env sees.

Whichever way you run it, a missing package stops the script with exit code 2 and a
message naming the package and the uv, pip, and conda commands that install it. Exit 2
means the work is blocked, never that a check failed.

## Analytical plots

Use `with_modules` from `figkit.palette_base` for paper-specific semantic colours and
`style_axes`, `scatter_ours_vs_base`, and `save_fig` from `figkit.plot_helpers`.

```python
import sys

import matplotlib.pyplot as plt

# Set SCRIPTS_DIR to this skill's own scripts/ directory, wherever the skill is installed,
# so that `figkit` is importable from your paper's caller script.
sys.path.insert(0, SCRIPTS_DIR)

from figkit.plot_helpers import save_fig, scatter_ours_vs_base, style_axes

fig, ax = plt.subplots(figsize=(5, 4))
scatter_ours_vs_base(
    ax,
    ours_xy=(60.3, 85.4),
    base_xy=[(42.1, 78.2), (55.0, 81.5)],
    base_labels=["MethodA", "MethodB"],
)
style_axes(ax, xlabel="FPS", ylabel="Precision Rate (%)")
save_fig(fig, "figures/speed_accuracy.pdf", dpi=600)
```

Run with `uv run --with matplotlib python your_paper/draw_scatter.py`. The PDF is canonical for
vector-native plots; DPI applies to rasterized content or raster exports.

## Qualitative result stitching

```bash
uv run --with pillow scripts/stitch.py \
  --images a.png b.png c.png --out figures/qualitative_row.png \
  --labels "GT" "Ours" "Baseline" --gap 8 --label-h 40
```

As a library, call `stitch_row(images, labels=..., gap=..., label_h=...)`. Panels are normalized
to the first image's height and placed on a white background.

## Efficiency measurement

Import `count_params`, `measure_runtime`, and optionally `measure_flops` from `measure_model.py`.
The caller owns model creation.

```bash
uv run --with torch --with numpy --with thop python your_paper/measure.py
```

`count_params` returns millions in `total_M` and `trainable_M`; `measure_runtime` returns mean
latency in milliseconds; `measure_flops` returns GMACs or `None` when `thop` is unavailable.

## Render QA annotation

Create a JSON object keyed by image filename. Each value may contain `title`, `anchors` as
`[x_fraction, y_fraction, label]`, and `fixes` as `[label, severity, description]`. Supported
severity keys are `blocker`, `verify`, `label`, `caption`, `style`, and `scope`; an
unrecognised key raises rather than painting a grey badge nobody notices.

```bash
uv run --with pillow --with matplotlib scripts/annotate_renders.py \
  --config spec.json --renders renders --out annotated
```

Resolve every `blocker` item and recheck the clean final artifact. Annotated images are QA evidence,
not manuscript figures.
