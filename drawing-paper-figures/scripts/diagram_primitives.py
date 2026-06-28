"""diagram_primitives.py —— 架构图绘制公共原语。

将 hgd_net 与 pace_net 两份 draw_cpm_branch.py 的公共核心抽取为可复用模块:
  - SEMANTIC:  语义颜色字典(填充/描边各 10 个条目,源自 hgd_net/palette.py)
  - draw_box:  带标签的圆角矩形(FancyBboxPatch)
  - connect:   语义箭头(fwd/cond/nograd/grad)
  - save_diagram: 同时落盘 PDF+PNG(600 DPI,复用 figkit.plot_helpers.save_fig)

各论文薄壳调用方只需导入本模块,不再重复实现上述原语;
坐标、标签、连线拓扑等布局细节保留在各论文自己的脚本里。
"""

from __future__ import annotations

from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.pyplot as plt

from figkit.palette_base import ARROW_FWD, ARROW_COND, ARROW_NOGRAD, ARROW_GRAD
from figkit.plot_helpers import save_fig


# ── 语义颜色字典 ─────────────────────────────────────────────────────────────
# 颜色值直接从 hgd_net/paper/figures/scripts/palette.py 逐字提取,
# 每个键名语义化以覆盖架构图最常见的模块类型。
SEMANTIC: dict[str, str] = {
    # 主干/骨干块 (GCM, DSR, PatchEmbed, Unpatchify …)
    "TEAL_FILL":    "#D4E8EB",   # hgd_net palette.py TEAL_FILL
    "TEAL_STROKE":  "#2A6478",   # hgd_net palette.py TEAL_STROKE

    # 条件/软权重块 (AdaLN, CondEmbed, Proj …)
    "AMBER":        "#E8D5B0",   # hgd_net palette.py AMBER_FILL
    "AMBER_STROKE": "#C49A3C",   # hgd_net palette.py AMBER_STROKE

    # 非可微/离散操作 (argmax, sort/unsort, routing …)
    "GRAY":         "#DADADA",   # hgd_net palette.py GRAY_FILL
    "GRAY_STROKE":  "#777777",   # hgd_net palette.py GRAY_STROKE

    # 精化/后处理头 (BAR head, fusion, output smoothing …)
    "GREEN":        "#CBE0C8",   # hgd_net palette.py GREEN_FILL
    "GREEN_STROKE": "#4F7A4C",   # hgd_net palette.py GREEN_STROKE

    # 展开块内部 (MSA, MLP inside G-Block …)
    "SLATE":        "#8DAFC0",   # hgd_net palette.py SLATE_FILL
    "SLATE_STROKE": "#486878",   # hgd_net palette.py SLATE_STROKE

    # 冻结/外部模块 (DA-CLIP encoder, guidance provider …)
    "FROZEN":        "#E0D8CE",  # hgd_net palette.py FROZEN_FILL
    "FROZEN_STROKE": "#A09080",  # hgd_net palette.py FROZEN_STROKE

    # 桥接/结构胶水 (linear 768→144, upsample, skip …)
    "BRIDGE":        "#E8E4D8",  # hgd_net palette.py BRIDGE_FILL
    "BRIDGE_STROKE": "#8A7A5C",  # hgd_net palette.py BRIDGE_STROKE

    # 输入/输出张量框
    "IO_FILL":   "#FFFFFF",      # hgd_net palette.py IO_FILL
    "IO_STROKE": "#333333",      # hgd_net palette.py IO_STROKE
}

# 箭头类型 → (颜色, 是否虚线) 映射表
_ARROW_STYLES: dict[str, tuple[str, bool]] = {
    "fwd":    (ARROW_FWD,    False),   # 标准前向数据流
    "cond":   (ARROW_COND,   False),   # 条件注入
    "nograd": (ARROW_NOGRAD, True),    # no_grad / 离散路由, 虚线
    "grad":   (ARROW_GRAD,   False),   # 反向梯度 / 强调
}


def draw_box(
    ax,
    xy: tuple[float, float],
    w: float,
    h: float,
    label: str,
    fill: str,
    stroke: str,
    fontsize: float = 9.5,
) -> FancyBboxPatch:
    """在 ax 上绘制圆角矩形模块并居中写标签,返回 patch 对象。

    参数
    ----
    ax:       matplotlib Axes
    xy:       左下角坐标 (x, y)
    w, h:     宽度、高度(数据坐标单位)
    label:    模块名称文字
    fill:     填充颜色(hex string)
    stroke:   边框颜色(hex string)
    fontsize: 标签字号,默认 9.5

    返回
    ----
    FancyBboxPatch 对象(已添加到 ax)
    """
    x, y = xy
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.08",
        facecolor=fill,
        edgecolor=stroke,
        linewidth=1.5,
        zorder=2,
    )
    ax.add_patch(box)
    ax.text(
        x + w / 2, y + h / 2,
        label,
        ha="center", va="center",
        fontsize=fontsize,
        fontweight="bold",
        color="#333333",
        zorder=3,
    )
    return box


def connect(
    ax,
    src_xy: tuple[float, float],
    dst_xy: tuple[float, float],
    kind: str = "fwd",
) -> None:
    """在两点之间绘制语义化箭头,按 kind 决定颜色与线型。

    参数
    ----
    ax:      matplotlib Axes
    src_xy:  箭头起点 (x, y)
    dst_xy:  箭头终点 (x, y)
    kind:    箭头类型,可选 "fwd" / "cond" / "nograd" / "grad"
             - fwd:    标准前向数据流(深青蓝,实线)
             - cond:   条件注入(琥珀,实线)
             - nograd: no_grad / 离散路由(灰,虚线)
             - grad:   反向梯度 / 强调(红,实线)

    返回
    ----
    None(注解已添加到 ax)
    """
    if kind not in _ARROW_STYLES:
        raise ValueError(f"connect: kind 必须是 {list(_ARROW_STYLES.keys())}，得到 {kind!r}")

    color, dashed = _ARROW_STYLES[kind]
    ls = "--" if dashed else "-"

    ax.annotate(
        "",
        xy=dst_xy,
        xytext=src_xy,
        arrowprops=dict(
            arrowstyle="->,head_width=0.08,head_length=0.06",
            color=color,
            lw=1.5,
            linestyle=ls,
        ),
        zorder=2,
    )


def save_diagram(fig, out_stem: str) -> None:
    """将架构图同时保存为 PDF 与 PNG(均 600 DPI),复用 figkit.save_fig。

    参数
    ----
    fig:      matplotlib Figure
    out_stem: 输出文件路径(不含后缀),如 "/path/to/diag"
              → 生成 /path/to/diag.pdf 与 /path/to/diag.png

    注意:调用后 fig 会被 plt.close(),不可再用。
    """
    # 先保存 PDF(矢量);save_fig 会 close fig,故 PNG 必须先另存
    # 方案:先手动保存 PNG,再调 save_fig 保存 PDF(其内部 close)
    from figkit.palette_base import BG
    fig.patch.set_facecolor(BG)
    fig.savefig(out_stem + ".png", dpi=600, bbox_inches="tight", facecolor=BG)
    # save_fig 会 close fig
    save_fig(fig, out_stem + ".pdf", dpi=600)
