"""CARE-Track color_pick 取色表的结构化单一事实源。

颜色按原取色表的色族与权重顺序保存。权重来自像素提取流程，用于排序而不是
概率归一化；白色背景跨多张图累计后可大于 100%。
"""

from __future__ import annotations


CARETRACK_COLORPICK: dict[str, tuple[tuple[str, float], ...]] = {
    "blue": (
        ("#4C80EC", 9.3), ("#BBE1FE", 4.1), ("#398DFE", 4.1),
        ("#7474FD", 3.5), ("#92A0FC", 3.5), ("#5A98FB", 2.9),
        ("#5746E4", 2.7), ("#2D91F0", 2.1), ("#75A1F5", 2.0),
        ("#9CABEE", 1.9), ("#4E91C6", 1.8), ("#566EE5", 1.6),
        ("#B8C0FF", 1.1), ("#94D1F6", 0.8), ("#B2B3DD", 0.6),
        ("#8B82AE", 0.6),
    ),
    "cyan": (
        ("#7CCAF0", 2.0), ("#62C3D6", 1.3), ("#08ABAA", 1.2),
        ("#829EAA", 0.9), ("#4C988C", 0.7), ("#4AC1BB", 0.7),
    ),
    "green/teal": (
        ("#0EBA5F", 10.2), ("#65C466", 8.0), ("#59A758", 5.0),
        ("#7AB380", 1.8), ("#1EB779", 1.8), ("#4FCA73", 1.3),
        ("#26C29B", 1.1), ("#3EB89C", 0.7), ("#5DA582", 0.7),
        ("#ADDEAE", 0.5), ("#47B848", 0.4), ("#9EC6B6", 0.4),
    ),
    "yellow/amber": (
        ("#FFDC14", 6.9), ("#FDC204", 6.2), ("#B1BE6B", 1.2),
        ("#FBD85E", 1.0), ("#FFD42F", 0.9), ("#D4CFAB", 0.7),
        ("#FFBD16", 0.6), ("#FBE049", 0.4),
    ),
    "coral/orange": (
        ("#F2C644", 12.6), ("#E6A64B", 2.5), ("#F7E5D8", 1.9),
        ("#F6CCA4", 1.2), ("#FE921C", 0.9), ("#C2A46E", 0.8),
        ("#F8AA0C", 0.8), ("#F3CB6E", 0.6), ("#CCA38C", 0.6),
        ("#F9E7B8", 0.4),
    ),
    "red": (
        ("#F17060", 17.8), ("#D9513F", 5.2), ("#FD423D", 3.2),
        ("#CE5F5B", 2.3), ("#F78D75", 1.1), ("#D3815F", 0.8),
        ("#F3CBC6", 0.5), ("#EBB3AC", 0.4), ("#E19288", 0.4),
        ("#FE5562", 0.4),
    ),
    "violet/periwinkle": (("#915E9F", 1.1), ("#886CAF", 1.0)),
    "magenta/pink": (("#FE608B", 1.1), ("#FEB9D8", 0.9)),
    "neutral/gray": (
        ("#D4E6E8", 3.1), ("#DEE5CA", 0.7), ("#B1B1B5", 0.7),
        ("#C8D5D3", 0.6), ("#5E5D5E", 0.5),
    ),
    "white/near-white": (("#FEFEFE", 807.5), ("#ECF0F1", 3.1)),
}


def family_colors(family: str) -> tuple[str, ...]:
    """返回指定色族的 HEX，保持原始像素权重由高到低的顺序。"""
    try:
        return tuple(hex_color for hex_color, _weight in CARETRACK_COLORPICK[family])
    except KeyError as exc:
        known = ", ".join(CARETRACK_COLORPICK)
        raise ValueError(f"unknown CARE-Track color family {family!r}; choose: {known}") from exc


def top_color(family: str) -> str:
    """返回指定色族在原取色表中权重最高的代表色。"""
    return family_colors(family)[0]
