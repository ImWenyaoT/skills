"""figkit.palette_base —— 全实验共享的绘图底色 / 箭头语法 / 排版 / 散点约定。

每篇论文的 figures/scripts/palette.py 只需:
    from figkit.palette_base import *          # 复用底色、箭头、排版、散点
然后在本文件之外定义本论文专属的「语义模块色」(如某模块填充/描边),
做到「底色一套、模块色各异」,消除两份 palette.py 里重复造的底色与箭头语法。
"""

# ── Backdrop(页面/绘图区底色,所有图统一)─────────────────────────────
BG = "#FAFAF8"      # 页面背景
PANEL = "#FFFFFF"   # 绘图区背景
TEXT = "#333333"    # 主文字
MUTED = "#666666"   # 次级文字
RULE = "#CCCCCC"    # 网格线 / 轻分隔线

# ── IO 张量框(输入/输出,中性)──────────────────────────────────────
IO_FILL = "#FFFFFF"
IO_STROKE = "#333333"

# ── Arrow grammar(箭头语义,所有架构图统一)──────────────────────────
ARROW_FWD = "#3A5A6A"     # 标准前向数据流
ARROW_COND = "#C49A3C"    # 条件注入(conditioning,琥珀)
ARROW_NOGRAD = "#888888"  # no_grad / 离散路由(常虚线)
ARROW_GRAD = "#B94A48"    # 反向梯度 / 强调
ACCENT = "#7952B3"        # 可选强调色

# ── Scatter / 数据点(「Ours vs baseline」散点统一约定)───────────────
POINT_OURS_FILL = "#B94A48"    # 我们的方法:红
POINT_OURS_STROKE = "#7A2A2A"
POINT_BASE_FILL = "#5B9EA6"    # baseline:青
POINT_BASE_STROKE = "#2A6478"

# ── Typography(字号约定)─────────────────────────────────────────────
FONT_TITLE = 12
FONT_AXIS = 10.5
FONT_TICK = 9.5
FONT_LABEL = 9.5
FONT_ANN = 9.0
FONT_LEGEND = 9.5
FONT_FOOTER = 8.5


def with_modules(**module_colors):
    """把本论文专属的语义模块色与共享底色合并成一个 dict。

    用法(在某论文的 palette.py 里):
        from figkit.palette_base import with_modules
        PALETTE = with_modules(GCM_FILL="#D4E8EB", GCM_STROKE="#2A6478", ...)
    返回的 dict 同时含共享底色键(BG/PANEL/.../ARROW_*/FONT_*)与传入的模块色键,
    便于绘图脚本统一按名取色。
    """
    base = {k: v for k, v in globals().items()
            if k.isupper() and isinstance(v, (str, int, float))}
    base.update(module_colors)
    return base
