"""annotate_renders.py（参数化版）

将修改任务卡标注叠加到渲染图上，生成带红色编号锚点 + 严重度色块修改清单的标注图。

与原版的区别：写死的 SPECS dict 已外置为 --config JSON，
通过 load_specs(config_path) 读取。SEVERITY 色映射与 CJK 字体注册保持不变。

运行方式:
    uv run python annotate_renders.py --config my_specs.json --renders renders/ --out out/
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
from matplotlib import gridspec
from matplotlib.patches import Circle, FancyBboxPatch


# --- CJK 字体注册 -------------------------------------------------------

def register_cjk_font() -> Optional[str]:
    """注册系统 CJK .ttc 字体到 matplotlib，并配置 sans-serif 列表。

    遍历已知 Noto CJK 字体路径，找到则调用 fontManager.addfont 注册；
    找不到字体时静默返回 None，不抛出异常。

    Returns:
        找到并注册的字体路径字符串；若无字体则返回 None。
    """
    _ttc_candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    ]
    registered: Optional[str] = None
    for ttc in _ttc_candidates:
        if Path(ttc).exists():
            try:
                _fm.fontManager.addfont(ttc)
                registered = ttc
            except Exception:
                pass

    plt.rcParams["font.sans-serif"] = [
        "Noto Sans CJK SC",
        "Noto Sans CJK JP",
        "DejaVu Sans",
    ]
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False

    return registered


# 模块加载时执行一次字体注册
register_cjk_font()


# --- 配色 ---------------------------------------------------------------

ANCHOR_FILL = "#B94A48"
ANCHOR_TXT = "#FFFFFF"
BG = "#FAFAF8"
TEXT = "#1F1F1F"

# 严重度色块（与 palette.py 保持同色系）
SEVERITY = {
    "必改":    "#B94A48",  # 阻塞项，不修不能交
    "复核":    "#C49A3C",  # 人眼复核（颜色/连线落点等）
    "标签":    "#2A6478",  # 在图上加/改文字标签
    "题注":    "#4F7A4C",  # caption / LaTeX 端文案
    "样式":    "#7952B3",  # 线型/颜色/粗细
    "范围":    "#777777",  # 决定该图替换范围
}


# --- 外部配置加载 -------------------------------------------------------

def load_specs(config_path: str) -> dict:
    """从外部 JSON 文件读取图注规格（取代原版写死的 SPECS dict）。

    JSON 格式示例:
        {
            "fig1.png": {
                "title": "Fig 1 标题",
                "anchors": [[0.5, 0.5, "1"], ...],
                "fixes":   [["1", "必改", "描述"], ...]
            }
        }

    也支持 brief 测试用的简化格式（anchors 用 4 元素列表
    [x, y, severity, desc]，没有 title/fixes）。

    Args:
        config_path: JSON 配置文件的路径字符串。

    Returns:
        以图名为键的规格字典。

    Raises:
        FileNotFoundError: 文件不存在时。
        json.JSONDecodeError: JSON 解析失败时。
    """
    path = Path(config_path)
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


# --- 绘制辅助函数 -------------------------------------------------------

def _draw_anchor(ax, x: float, y: float, label: str, r: float) -> None:
    """在图像坐标轴上绘制红底白字的编号圆圈锚点。

    Args:
        ax: matplotlib Axes 对象（图像区域）。
        x: 锚点中心的像素 x 坐标。
        y: 锚点中心的像素 y 坐标。
        label: 圆圈内显示的文字（通常为数字字符串）。
        r: 圆圈半径（像素）。
    """
    ax.add_patch(Circle(
        (x, y), r,
        facecolor=ANCHOR_FILL, edgecolor="white", linewidth=2.0, zorder=20,
    ))
    ax.text(
        x, y, label,
        ha="center", va="center",
        color=ANCHOR_TXT, fontsize=11, fontweight="bold", zorder=21,
    )


def _draw_legend_row(ax, y: float, label: str, severity: str, desc: str) -> None:
    """在 legend 区域绘制一行修改记录：编号圈 + 严重度色块 + 描述文字。

    Args:
        ax: matplotlib Axes 对象（legend 区域）。
        y: 在 transAxes 坐标系中的纵向位置（0~1）。
        label: 编号字符串，与图上锚点对应。
        severity: 严重度键，必须在 SEVERITY 中有对应颜色。
        desc: 修改描述文字。
    """
    # 编号圈
    ax.add_patch(Circle(
        (0.022, y), 0.014,
        facecolor=ANCHOR_FILL, edgecolor="white", linewidth=1.2,
        transform=ax.transAxes,
    ))
    ax.text(
        0.022, y, label,
        ha="center", va="center", color="white",
        fontsize=9, fontweight="bold",
        transform=ax.transAxes,
    )
    # 严重度色块
    badge_x, badge_w = 0.050, 0.060
    ax.add_patch(FancyBboxPatch(
        (badge_x, y - 0.022), badge_w, 0.044,
        boxstyle="round,pad=0.005",
        facecolor=SEVERITY.get(severity, "#999999"), edgecolor="none",
        transform=ax.transAxes,
    ))
    ax.text(
        badge_x + badge_w / 2, y, severity,
        ha="center", va="center", color="white",
        fontsize=9, fontweight="bold",
        transform=ax.transAxes,
    )
    # 描述文字
    ax.text(
        badge_x + badge_w + 0.014, y, desc,
        ha="left", va="center", color=TEXT, fontsize=9.5,
        transform=ax.transAxes,
    )


# --- 核心标注函数 -------------------------------------------------------

def annotate_image(img_path: str, spec: dict, out_path: str) -> Path:
    """将标注信息叠加到图像上并保存为 PNG。

    spec 支持两种 anchors 格式：
    - 3 元素 (x_frac, y_frac, label)：仅画锚点圆圈
    - 4 元素 (x_frac, y_frac, severity, desc)：画锚点并在 legend 区渲染修改行

    spec 字段说明：
        title   (可选): 顶部标题文字。
        anchors (必须): 锚点列表，坐标为相对图像尺寸的小数。
        fixes   (可选): 修改清单 [(label, severity, desc), ...]。

    Args:
        img_path: 源图像文件路径。
        spec: 该图的标注规格字典。
        out_path: 输出 PNG 文件路径。

    Returns:
        输出文件的 Path 对象。
    """
    img = mpimg.imread(str(img_path))
    h, w = img.shape[:2]

    anchors = spec.get("anchors", [])
    fixes = spec.get("fixes", [])
    title = spec.get("title", "")

    # 兼容 4 元素 anchors（x, y, severity, desc）→ 自动生成编号锚点 + fixes
    if anchors and len(anchors[0]) == 4:
        auto_fixes = []
        auto_anchors = []
        for i, entry in enumerate(anchors):
            xf, yf, sev, desc = entry
            lbl = str(i + 1)
            auto_anchors.append((xf, yf, lbl))
            auto_fixes.append((lbl, sev, desc))
        anchors = auto_anchors
        if not fixes:
            fixes = auto_fixes

    n_fixes = len(fixes)

    # 画布几何
    page_w_in = 13.0
    img_h_in = page_w_in * (h / w)
    title_h_in = 0.45 if title else 0.0
    row_h_in = 0.38
    legend_h_in = max(1.6, n_fixes * row_h_in + 0.6) if n_fixes else 0.0
    total_h_in = title_h_in + img_h_in + legend_h_in

    fig = plt.figure(figsize=(page_w_in, total_h_in), facecolor=BG)

    # 动态构建 gridspec 行
    height_ratios = []
    subplot_order = []
    if title:
        height_ratios.append(title_h_in)
        subplot_order.append("title")
    height_ratios.append(img_h_in)
    subplot_order.append("img")
    if n_fixes:
        height_ratios.append(legend_h_in)
        subplot_order.append("legend")

    gs = gridspec.GridSpec(
        len(height_ratios), 1, figure=fig,
        height_ratios=height_ratios,
        hspace=0.03,
        left=0.02, right=0.98, top=0.99, bottom=0.01,
    )

    axes = {name: fig.add_subplot(gs[i]) for i, name in enumerate(subplot_order)}

    # 标题
    if "title" in axes:
        ax_t = axes["title"]
        ax_t.axis("off")
        ax_t.set_xlim(0, 1)
        ax_t.set_ylim(0, 1)
        ax_t.text(0.5, 0.5, title, ha="center", va="center",
                  fontsize=14, fontweight="bold", color=TEXT)

    # 图像 + 锚点
    ax_i = axes["img"]
    ax_i.imshow(img)
    ax_i.set_xlim(0, w)
    ax_i.set_ylim(h, 0)
    ax_i.axis("off")

    radius = min(w, h) * 0.024
    for anchor in anchors:
        xf, yf, label = anchor[0], anchor[1], anchor[2]
        _draw_anchor(ax_i, xf * w, yf * h, str(label), radius)

    # legend 区
    if "legend" in axes and n_fixes:
        ax_l = axes["legend"]
        ax_l.axis("off")
        ax_l.set_xlim(0, 1)
        ax_l.set_ylim(0, 1)

        ax_l.add_patch(FancyBboxPatch(
            (0.005, 0.02), 0.99, 0.96,
            boxstyle="round,pad=0.005",
            facecolor="white", edgecolor="#CCCCCC", linewidth=0.8,
            transform=ax_l.transAxes,
        ))

        top_pad, bot_pad = 0.08, 0.08
        row_span = 1.0 - top_pad - bot_pad
        for i, fix in enumerate(fixes):
            label, severity, desc = fix[0], fix[1], fix[2]
            y = 1.0 - top_pad - row_span * (i + 0.5) / n_fixes
            _draw_legend_row(ax_l, y, str(label), severity, desc)

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(out), dpi=140, facecolor=BG)
    plt.close(fig)
    return out


# --- CLI 入口 -----------------------------------------------------------

def main() -> None:
    """命令行入口：从 --config JSON 读取 SPECS，批量生成标注图。"""
    parser = argparse.ArgumentParser(description="为渲染图生成修改任务卡标注")
    parser.add_argument("--config", required=True,
                        help="包含 SPECS 的 JSON 配置文件路径")
    parser.add_argument("--renders", default=".",
                        help="源渲染图所在目录（默认当前目录）")
    parser.add_argument("--out", default="annotated",
                        help="输出目录（默认 ./annotated）")
    args = parser.parse_args()

    specs = load_specs(args.config)
    renders_dir = Path(args.renders)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    written = []
    for img_name, spec in specs.items():
        img_path = renders_dir / img_name
        if not img_path.exists():
            print(f"[跳过] {img_name} 在 {renders_dir} 下不存在")
            continue
        stem = Path(img_name).stem
        out_path = out_dir / f"{stem}_spec.png"
        annotate_image(str(img_path), spec, str(out_path))
        written.append(out_path)
        print(f"[完成] {out_path}")

    if written:
        print(f"\n共生成 {len(written)} 张标注图，输出目录：{out_dir}")


if __name__ == "__main__":
    main()
