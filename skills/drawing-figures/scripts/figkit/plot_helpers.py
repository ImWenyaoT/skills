"""figkit.plot_helpers — matplotlib helpers shared across every experiment: one
export DPI and format, one axis style, and the recurring "Ours (red) vs
baselines (teal)" scatter.

Every paper's figures/scripts/draw_*.py imports the same three:
    from figkit.plot_helpers import save_fig, style_axes, scatter_ours_vs_base
which is what keeps the figures of different papers looking like one set.
"""
from __future__ import annotations

import matplotlib.pyplot as plt

from figkit.palette_base import (
    BG, PANEL, TEXT, MUTED, RULE,
    POINT_OURS_FILL, POINT_OURS_STROKE, POINT_BASE_FILL, POINT_BASE_STROKE,
    FONT_AXIS, FONT_TICK, FONT_LEGEND,
)


def save_fig(fig, out_path, dpi=600):
    """Save at 600 DPI with tight margins and the page backdrop.

    The suffix of out_path picks the format (png, pdf, eps).
    """
    fig.patch.set_facecolor(BG)
    fig.savefig(out_path, dpi=dpi, bbox_inches="tight", facecolor=BG)
    plt.close(fig)


def style_axes(ax, xlabel="", ylabel="", title=""):
    """Apply the shared axis look: panel backdrop, faint grid, no top or right
    spine, one font size.
    """
    ax.set_facecolor(PANEL)
    ax.grid(True, color=RULE, linewidth=0.6, alpha=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.tick_params(colors=TEXT, labelsize=FONT_TICK)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=FONT_AXIS, color=TEXT)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=FONT_AXIS, color=TEXT)
    if title:
        ax.set_title(title, fontsize=FONT_AXIS + 1, color=TEXT)
    return ax


def scatter_ours_vs_base(ax, ours_xy, base_xy, ours_label="Ours",
                         base_labels=None, annotate=True):
    """Draw the "ours vs baselines" scatter: ours in solid red, baselines in teal.

    ours_xy:     a single (x, y) point
    base_xy:     [(x, y), ...] for the baselines
    base_labels: names matching base_xy, used when annotate is on
    """
    bx = [p[0] for p in base_xy]
    by = [p[1] for p in base_xy]
    ax.scatter(bx, by, s=70, c=POINT_BASE_FILL, edgecolors=POINT_BASE_STROKE,
               linewidths=1.0, zorder=3, label="Baselines")
    ax.scatter([ours_xy[0]], [ours_xy[1]], s=130, marker="*",
               c=POINT_OURS_FILL, edgecolors=POINT_OURS_STROKE,
               linewidths=1.2, zorder=4, label=ours_label)
    if annotate and base_labels:
        for (x, y), name in zip(base_xy, base_labels):
            ax.annotate(name, (x, y), fontsize=FONT_LEGEND, color=MUTED,
                        xytext=(4, 4), textcoords="offset points")
    ax.legend(fontsize=FONT_LEGEND, frameon=False)
    return ax
