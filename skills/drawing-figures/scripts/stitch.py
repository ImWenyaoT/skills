"""
stitch.py — general-purpose horizontal image stitcher

The shared pattern (distilled from 10+ stitch_*.py in pace_net):
  read a list of PIL.Image → scale to equal height → stitch horizontally (gap filled with the
  background colour) → optional label strip along the top

Usage:
  python stitch.py --images a.png b.png c.png --labels A B C --out out.png --gap 8
"""

from __future__ import annotations

import argparse

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont


def stitch_row(
    images: list,
    labels: list | None = None,
    gap: int = 8,
    bg: tuple = (255, 255, 255),
    label_h: int = 0,
) -> Image.Image:
    """Stitch a set of PIL.Image side by side at equal height, optionally with a label strip on top.

    Parameters
    ----------
    images  : list of PIL.Image; the caller may scale them to equal height beforehand, and any that
              differ are scaled to the first image's height.
    labels  : list of strings as long as images (used when label_h > 0); None means no labels.
    gap     : pixel spacing between neighbouring images, filled with the background colour.
    bg      : background/gap fill colour, an RGB triple, white by default.
    label_h : height of the top label strip in pixels; 0 means no label strip.

    Returns
    -------
    PIL.Image, sized
        width  = sum(column widths) + gap * (n - 1)
        height = image height + label_h
    """
    if not images:
        raise ValueError("the images list must not be empty")

    n = len(images)

    # Equalize height: take the first image as the reference and scale the others to match
    target_h = images[0].height
    normalized = []
    for img in images:
        if img.height != target_h:
            scale = target_h / img.height
            new_w = max(1, round(img.width * scale))
            img = img.resize((new_w, target_h), Image.Resampling.LANCZOS)
        normalized.append(img)

    # Compute the canvas size
    total_w = sum(img.width for img in normalized) + gap * (n - 1)
    canvas_h = target_h + label_h
    canvas = Image.new("RGB", (total_w, canvas_h), bg)

    # Paste each column (label_h is the top label strip's height, so images sit at that offset)
    x_offset = 0
    for img in normalized:
        canvas.paste(img, (x_offset, label_h))
        x_offset += img.width + gap

    # Draw the text in the top label strip
    if label_h > 0 and labels:
        draw = ImageDraw.Draw(canvas)
        # try a system font, falling back to the default font
        font = _load_font(label_h)
        x_offset = 0
        for i, img in enumerate(normalized):
            col_w = img.width
            text = labels[i] if i < len(labels) else ""
            if text:
                # centre the text
                bbox = draw.textbbox((0, 0), text, font=font)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]
                tx = x_offset + (col_w - text_w) // 2
                ty = (label_h - text_h) // 2
                draw.text((tx, ty), text, fill="black", font=font)
            x_offset += col_w + gap

    return canvas


# truetype() returns FreeTypeFont and load_default() may return either, so the
# annotation is the union rather than the base class alone.
def _load_font(label_h: int) -> ImageFont.ImageFont | FreeTypeFont:
    """Derive a suitable font size from the label strip's height and return a PIL font object.

    Prefers a TrueType font from the common system paths, and uses PIL's built-in default font when
    that fails.
    """
    font_size = max(10, int(label_h * 0.6))
    candidate_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for path in candidate_paths:
        try:
            return ImageFont.truetype(path, font_size)
        except OSError:
            continue
    return ImageFont.load_default()


def main() -> None:
    """Command-line entry point: read images from file paths, stitch them horizontally, and save.

    Example
    -------
    python stitch.py --images a.png b.png c.png --labels A B C --out out.png --gap 8 --label-h 40
    """
    parser = argparse.ArgumentParser(description="Horizontal equal-height image stitcher")
    parser.add_argument("--images", nargs="+", required=True, help="list of input image paths")
    parser.add_argument(
        "--labels", nargs="+", default=None, help="top label for each column (as long as --images)"
    )
    parser.add_argument("--out", required=True, help="output image path")
    parser.add_argument("--gap", type=int, default=8, help="pixels between columns, default 8")
    parser.add_argument(
        "--label-h",
        type=int,
        default=0,
        dest="label_h",
        help="height of the top label strip in pixels, 0 for no labels, default 0",
    )
    args = parser.parse_args()

    imgs = [Image.open(p).convert("RGB") for p in args.images]
    result = stitch_row(imgs, labels=args.labels, gap=args.gap, label_h=args.label_h)
    result.save(args.out)
    print(f"saved the stitched image to {args.out} ({result.width}×{result.height})")


if __name__ == "__main__":
    main()
