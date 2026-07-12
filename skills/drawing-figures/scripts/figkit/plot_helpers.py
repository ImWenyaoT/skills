"""figkit.plot_helpers —— 全实验共享的 matplotlib 辅助:统一出图 DPI/格式、
坐标轴样式、以及反复出现的「Ours(红) vs baselines(青)」散点。

各论文 figures/scripts/draw_*.py 统一:
    from figkit.plot_helpers import save_fig, style_axes, scatter_ours_vs_base
保证所有论文图风格一致。
"""
from __future__ import annotations

import matplotlib.pyplot as plt

from figkit.palette_base import (
    BG, PANEL, TEXT, MUTED, RULE,
    POINT_OURS_FILL, POINT_OURS_STROKE, POINT_BASE_FILL, POINT_BASE_STROKE,
    FONT_AXIS, FONT_TICK, FONT_LEGEND,
)


def save_fig(fig, out_path, dpi=600):
    """统一保存:600 DPI、紧边距、页面底色。out_path 后缀决定格式(png/pdf/eps)。"""
    fig.patch.set_facecolor(BG)
    fig.savefig(out_path, dpi=dpi, bbox_inches="tight", facecolor=BG)
    plt.close(fig)


def style_axes(ax, xlabel="", ylabel="", title=""):
    """统一坐标轴外观:绘图区底色、淡网格、去顶右脊、统一字号。"""
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
    """画「我们 vs baseline」散点:Ours 用红色实心强调,baselines 用青色。

    ours_xy:   (x, y) 单点
    base_xy:   [(x, y), ...] baseline 多点
    base_labels: 与 base_xy 对应的名字列表(annotate 时标注)
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
