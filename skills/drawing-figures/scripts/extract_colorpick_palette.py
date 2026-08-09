#!/usr/bin/env python3
"""Pull "every colour that ever appears" out of the reference-image pixels, as a general palette.

Scope: every colour present in the reference images under the given directory (including the
in-between colours inside a gradient) counts as pickable; a gradient only supplies a "range you
may pick from", it is not a gradient to draw with. Method: quantize each image adaptively to a
generous number of colours -> pool across images -> cluster near-duplicates away -> emit hex
grouped by hue (for the layout colour system and for picking while drawing).
Black and white are kept on their own.
"""

from __future__ import annotations

import colorsys
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image

# Default hyper-parameters —— overridable from the command line
QUANT_PER_IMG = 32      # quantized colours per image (generous, to cover gradients)
MIN_SHARE = 0.004       # share threshold within one image (filters noise pixels)
MERGE_DIST = 22         # Euclidean distance at which near-duplicate colours merge across images


def parse_args():
    """CLI: source directory and output md are required; quantized colour count / merge distance are tunable."""
    import argparse
    p = argparse.ArgumentParser(description="Extract a palette from reference-image pixels")
    p.add_argument("--src", type=Path, required=True, help="color_pick source image directory")
    p.add_argument("--out", type=Path, required=True, help="output palette md path")
    p.add_argument("--n-colors", dest="n_colors", type=int, default=32, help="quantized colours per image")
    p.add_argument("--merge-dist", dest="merge_dist", type=float, default=22.0, help="Euclidean distance for merging near-duplicate colours")
    return p.parse_args()


def image_colors(path: Path, n_colors: int = QUANT_PER_IMG,
                 min_share: float = MIN_SHARE) -> list[tuple[tuple[int, int, int], float]]:
    """Quantize a single image adaptively, returning [(rgb, share)] with low-share noise already dropped."""
    im = Image.open(path).convert("RGB")
    im.thumbnail((400, 400))  # downsample for speed
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
    """Cluster a colour list by Euclidean distance, returning the representative colours (no weights).

    Args:
        colors: colour list in the form [(r, g, b), ...].
        dist:   merge threshold; colours closer than this count as one cluster.

    Returns:
        Deduplicated representative colours, each an (r, g, b) int tuple.
    """
    if not colors:
        return []

    # weight everything at 1.0, then cluster greedily from the top
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
    """Cluster the colours from every image (weights included) by Euclidean distance; each representative is the weighted mean of its cluster, and weights accumulate."""
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
    """Bucket a colour into a family by HSV, so layout can map families onto semantics."""
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
    """RGB -> #RRGGBB (uppercase)."""
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def main() -> None:
    """Main flow: quantize image by image -> pool and merge -> group into families -> write the markdown palette + print to console."""
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

    lines = ["# color_pick palette (extracted from pixels)", "",
             f"Adaptive quantization to {n_colors} colours per image, merged across images (dist<{merge_dist}), shares<{MIN_SHARE} filtered out.",
             "A gradient = a range you may pick from; below are the discrete representative colours.", ""]
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
    print(f"\nwrote: {out}  ({len(merged)} representative colours)")


if __name__ == "__main__":
    main()
