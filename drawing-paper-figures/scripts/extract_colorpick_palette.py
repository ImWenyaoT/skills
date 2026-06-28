#!/usr/bin/env python3
"""从参考图像素提取"出现过的所有颜色", 形成通用取色库。

口径: 把指定目录的参考图里出现过的所有颜色(含渐变范围内的中间色)纳入取色范围,
渐变只是提供"可取的范围"而非作图用渐变。做法: 每图自适应量化到较多颜色 ->
跨图汇总 -> 近似色聚类去重 -> 按色相分组输出 hex(供 layout 色彩系统与作图取色)。
黑/白单独保留。
"""

from __future__ import annotations

import colorsys
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image

# 默认超参 —— 可通过命令行覆盖
QUANT_PER_IMG = 32      # 每图量化色数(取多, 覆盖渐变)
MIN_SHARE = 0.004       # 单图内占比阈值(滤噪点)
MERGE_DIST = 22         # 跨图近似色合并的欧氏距离阈值


def parse_args():
    """命令行:取色图源目录与输出 md 必填;量化色数/合并距离可调。"""
    import argparse
    p = argparse.ArgumentParser(description="从参考图像素提取取色库")
    p.add_argument("--src", type=Path, required=True, help="color_pick 图源目录")
    p.add_argument("--out", type=Path, required=True, help="输出取色 md 路径")
    p.add_argument("--n-colors", dest="n_colors", type=int, default=32, help="每图量化色数")
    p.add_argument("--merge-dist", dest="merge_dist", type=float, default=22.0, help="近似色合并欧氏距离")
    return p.parse_args()


def image_colors(path: Path, n_colors: int = QUANT_PER_IMG,
                 min_share: float = MIN_SHARE) -> list[tuple[tuple[int, int, int], float]]:
    """对单图自适应量化, 返回 [(rgb, 占比)], 已滤掉低占比噪点。"""
    im = Image.open(path).convert("RGB")
    im.thumbnail((400, 400))  # 降采样提速
    q = im.quantize(colors=n_colors, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()
    counts = Counter(q.getdata())
    total = sum(counts.values())
    out = []
    for idx, cnt in counts.items():
        share = cnt / total
        if share < min_share:
            continue
        rgb = (pal[idx * 3], pal[idx * 3 + 1], pal[idx * 3 + 2])
        out.append((rgb, share))
    return out


def merge_colors(colors: list[tuple], dist: float) -> list[tuple]:
    """把颜色列表按欧氏距离聚类去重, 返回代表色列表(不含权重)。

    参数:
        colors: [(r, g, b), ...] 形式的颜色列表。
        dist:   合并阈值, 欧氏距离小于此值的颜色视为同簇。

    返回:
        去重后代表色列表, 每项为 (r, g, b) 整型元组。
    """
    if not colors:
        return []

    # 统一权重为 1.0, 贪心从头聚类
    reps: list[list] = []  # [sum_rgb*w, w]
    for rgb in colors:
        arr = np.array(rgb, dtype=float)
        placed = False
        for r in reps:
            center = r[0] / r[1]
            if np.linalg.norm(center - arr) < dist:
                r[0] += arr
                r[1] += 1
                placed = True
                break
        if not placed:
            reps.append([arr.copy(), 1.0])

    return [tuple(int(v) for v in np.round(r[0] / r[1]).astype(int)) for r in reps]


def merge(colors: list[tuple[tuple[int, int, int], float]],
          merge_dist: float = MERGE_DIST) -> list[tuple[tuple[int, int, int], float]]:
    """把所有图的颜色(含权重)按欧氏距离聚类去重, 代表色取簇内加权均值, 权重累加。"""
    reps: list[list] = []  # [sum_rgb*w, w]
    for rgb, w in sorted(colors, key=lambda c: -c[1]):
        arr = np.array(rgb, dtype=float)
        placed = False
        for r in reps:
            center = r[0] / r[1]
            if np.linalg.norm(center - arr) < merge_dist:
                r[0] += arr * w
                r[1] += w
                placed = True
                break
        if not placed:
            reps.append([arr * w, w])
    merged = [(tuple(np.round(r[0] / r[1]).astype(int)), r[1]) for r in reps]
    return sorted(merged, key=lambda c: -c[1])


def family(rgb: tuple[int, int, int]) -> str:
    """按 HSV 把颜色归到色族, 便于 layout 语义映射。"""
    r, g, b = (v / 255 for v in rgb)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    if v >= 0.93 and s <= 0.06:
        return "white/near-white"
    if v <= 0.18:
        return "black/ink"
    if s <= 0.12:
        return "neutral/gray"
    hd = h * 360
    if hd < 18 or hd >= 345:
        return "red"
    if hd < 45:
        return "coral/orange"
    if hd < 70:
        return "yellow/amber"
    if hd < 170:
        return "green/teal"
    if hd < 200:
        return "cyan"
    if hd < 255:
        return "blue"
    if hd < 290:
        return "violet/periwinkle"
    return "magenta/pink"


def hexof(rgb: tuple[int, int, int]) -> str:
    """RGB -> #RRGGBB(大写)。"""
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def main() -> None:
    """主流程: 逐图量化 -> 汇总合并 -> 分族 -> 写 markdown 取色库 + 控制台打印。"""
    args = parse_args()
    src: Path = args.src
    out: Path = args.out
    n_colors: int = args.n_colors
    merge_dist: float = args.merge_dist

    imgs = sorted(p for p in src.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg"})
    allc: list[tuple[tuple[int, int, int], float]] = []
    for p in imgs:
        allc.extend(image_colors(p, n_colors=n_colors))
    merged = merge(allc, merge_dist=merge_dist)

    fam_order = ["blue", "cyan", "green/teal", "yellow/amber", "coral/orange",
                 "red", "violet/periwinkle", "magenta/pink", "neutral/gray",
                 "white/near-white", "black/ink"]
    by_fam: dict[str, list] = {f: [] for f in fam_order}
    for rgb, w in merged:
        by_fam.setdefault(family(rgb), []).append((rgb, w))

    lines = ["# color_pick 取色库（像素提取）", "",
             f"自适应量化每图 {n_colors} 色、跨图合并(dist<{merge_dist})、滤占比<{MIN_SHARE}。",
             "渐变=可取范围；下列为离散代表色。", ""]
    print(f"{'family':<20}{'hex':<10}{'weight%':>8}")
    for f in fam_order:
        items = sorted(by_fam.get(f, []), key=lambda c: -c[1])
        if not items:
            continue
        lines.append(f"## {f}")
        for rgb, w in items:
            lines.append(f"- {hexof(rgb)}  (w={w*100:.1f}%)")
            print(f"{f:<20}{hexof(rgb):<10}{w*100:>7.1f}")
        lines.append("")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n写出: {out}  (共 {len(merged)} 个代表色)")


if __name__ == "__main__":
    main()
