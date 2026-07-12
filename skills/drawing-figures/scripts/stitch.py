"""
stitch.py — 通用横向图片拼接工具

公共模式（从 pace_net 10+ stitch_*.py 提炼）：
  读取 PIL.Image 列表 → 等高缩放 → 横向拼接（gap 填背景色）→ 可选顶部标签条

用法：
  python stitch.py --images a.png b.png c.png --labels A B C --out out.png --gap 8
"""

from __future__ import annotations

import argparse
from typing import Optional

from PIL import Image, ImageDraw, ImageFont


def stitch_row(
    images: list,
    labels: Optional[list] = None,
    gap: int = 8,
    bg: tuple = (255, 255, 255),
    label_h: int = 0,
) -> Image.Image:
    """横向等高拼接一组 PIL.Image，可在顶部添加标签条。

    参数
    ----
    images  : PIL.Image 列表，调用方可提前缩放至等高；若高度不一致则统一缩放到首图高度。
    labels  : 与 images 等长的字符串列表（label_h > 0 时使用）；None 表示不添加标签。
    gap     : 相邻图片之间的像素间距，填充背景色。
    bg      : 背景/间距填充色，RGB 三元组，默认白色。
    label_h : 顶部标签条高度（像素）；为 0 时不添加标签条。

    返回
    ----
    PIL.Image，尺寸为
        宽 = sum(各列宽) + gap * (n - 1)
        高 = 图片高 + label_h
    """
    if not images:
        raise ValueError("images 列表不能为空")

    n = len(images)

    # 统一高度：以首图为基准，高度不同的图缩放对齐
    target_h = images[0].height
    normalized = []
    for img in images:
        if img.height != target_h:
            scale = target_h / img.height
            new_w = max(1, round(img.width * scale))
            img = img.resize((new_w, target_h), Image.LANCZOS)
        normalized.append(img)

    # 计算画布尺寸
    total_w = sum(img.width for img in normalized) + gap * (n - 1)
    canvas_h = target_h + label_h
    canvas = Image.new("RGB", (total_w, canvas_h), bg)

    # 粘贴各列图片（label_h 为顶部标签条高度，图片贴在 label_h 偏移处）
    x_offset = 0
    for img in normalized:
        canvas.paste(img, (x_offset, label_h))
        x_offset += img.width + gap

    # 绘制顶部标签条文字
    if label_h > 0 and labels:
        draw = ImageDraw.Draw(canvas)
        # 尝试加载系统字体，失败则退回默认字体
        font = _load_font(label_h)
        x_offset = 0
        for i, img in enumerate(normalized):
            col_w = img.width
            text = labels[i] if i < len(labels) else ""
            if text:
                # 居中对齐文字
                bbox = draw.textbbox((0, 0), text, font=font)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]
                tx = x_offset + (col_w - text_w) // 2
                ty = (label_h - text_h) // 2
                draw.text((tx, ty), text, fill="black", font=font)
            x_offset += col_w + gap

    return canvas


def _load_font(label_h: int) -> ImageFont.ImageFont:
    """根据标签条高度推算合适的字体大小，返回 PIL 字体对象。

    优先从常见系统路径加载 TrueType 字体，失败时使用 PIL 内置默认字体。
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
        except (IOError, OSError):
            continue
    return ImageFont.load_default()


def main() -> None:
    """命令行入口：从文件路径读取图片，横向拼接后保存。

    示例
    ----
    python stitch.py --images a.png b.png c.png --labels A B C --out out.png --gap 8 --label-h 40
    """
    parser = argparse.ArgumentParser(description="横向等高图片拼接工具")
    parser.add_argument("--images", nargs="+", required=True, help="输入图片路径列表")
    parser.add_argument("--labels", nargs="+", default=None, help="每列顶部标签（与 --images 等长）")
    parser.add_argument("--out", required=True, help="输出图片路径")
    parser.add_argument("--gap", type=int, default=8, help="列间距像素数，默认 8")
    parser.add_argument("--label-h", type=int, default=0, dest="label_h",
                        help="顶部标签条高度（像素），0 表示不加标签，默认 0")
    args = parser.parse_args()

    imgs = [Image.open(p).convert("RGB") for p in args.images]
    result = stitch_row(imgs, labels=args.labels, gap=args.gap, label_h=args.label_h)
    result.save(args.out)
    print(f"已保存拼接图至 {args.out}（尺寸 {result.width}×{result.height}）")


if __name__ == "__main__":
    main()
