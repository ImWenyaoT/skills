"""annotate_renders.py (parameterised)

Overlay a fix-list onto a rendered figure, producing an annotated image with red numbered
anchors and a severity-coloured list of the fixes.

Unlike the original, the hard-coded SPECS dict now lives in a --config JSON read by
load_specs(config_path). The SEVERITY colour map and the CJK font registration are unchanged.

Usage:
    uv run python annotate_renders.py --config my_specs.json --renders renders/ --out out/
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import matplotlib.image as mpimg
    import matplotlib.pyplot as plt
    from matplotlib import font_manager as _fm
    from matplotlib import gridspec
    from matplotlib.patches import Circle, FancyBboxPatch
except ImportError as exc:  # pragma: no cover - environment, not logic
    sys.stderr.write(
        f"{exc.name or 'matplotlib'} is needed by this script and is not importable here.\n"
        "Install it whichever way suits your environment:\n"
        "    uv run --with matplotlib python <this script>\n"
        "    pip install matplotlib\n"
        "    conda install matplotlib\n"
        "Exit code 2 means the check is blocked, not that it failed.\n"
    )
    raise SystemExit(2) from exc

# --- CJK font registration ----------------------------------------------


def register_cjk_font() -> str | None:
    """Register a system CJK .ttc font with matplotlib and set the sans-serif list.

    Walk the known Noto CJK font paths and register the first one found through
    fontManager.addfont. Return None quietly when no font is present — a figure with no
    CJK text in it does not need one.

    Returns:
        The path of the font that was registered, or None when none was found.
    """
    _ttc_candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    ]
    registered: str | None = None
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


# Register once, at import time
register_cjk_font()


# --- Colours ------------------------------------------------------------

ANCHOR_FILL = "#B94A48"
ANCHOR_TXT = "#FFFFFF"
BG = "#FAFAF8"
TEXT = "#1F1F1F"

# Severity badges, in the same hues as palette.py
SEVERITY = {
    "blocker": "#B94A48",  # must be fixed before the figure ships
    "verify": "#C49A3C",  # a human has to look (colour, where a line lands)
    "label": "#2A6478",  # add or change text on the figure itself
    "caption": "#4F7A4C",  # caption or LaTeX-side wording
    "style": "#7952B3",  # line style, colour, weight
    "scope": "#777777",  # decides how much of this figure gets replaced
}


# --- External config ----------------------------------------------------


def load_specs(config_path: str) -> dict:
    """Read the annotation specs from an external JSON file.

    Example JSON:
        {
            "fig1.png": {
                "title": "Fig 1 title",
                "anchors": [[0.5, 0.5, "1"], ...],
                "fixes":   [["1", "blocker", "description"], ...]
            }
        }

    A short form is also accepted, for tests: anchors as four-element lists
    [x, y, severity, desc], with no title or fixes.

    Args:
        config_path: path to the JSON config file.

    Returns:
        The spec dict, keyed by figure name.

    Raises:
        FileNotFoundError: when the file is absent.
        json.JSONDecodeError: when the JSON does not parse.
    """
    path = Path(config_path)
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


# --- Drawing helpers ----------------------------------------------------


def _draw_anchor(ax, x: float, y: float, label: str, r: float) -> None:
    """Draw a numbered anchor — white on red — on the image axes.

    Args:
        ax: the matplotlib Axes holding the image.
        x: anchor centre, in pixels.
        y: anchor centre, in pixels.
        label: the text inside the circle, usually a number.
        r: circle radius, in pixels.
    """
    ax.add_patch(
        Circle(
            (x, y),
            r,
            facecolor=ANCHOR_FILL,
            edgecolor="white",
            linewidth=2.0,
            zorder=20,
        )
    )
    ax.text(
        x,
        y,
        label,
        ha="center",
        va="center",
        color=ANCHOR_TXT,
        fontsize=11,
        fontweight="bold",
        zorder=21,
    )


def _draw_legend_row(ax, y: float, label: str, severity: str, desc: str) -> None:
    """Draw one fix row in the legend area: number, severity badge, description.

    Args:
        ax: the matplotlib Axes holding the legend.
        y: vertical position in transAxes coordinates, 0 to 1.
        label: the number, matching the anchor on the image.
        severity: a SEVERITY key; an unknown one is an error, not a grey badge.
        desc: what has to change.
    """
    # Numbered circle
    ax.add_patch(
        Circle(
            (0.022, y),
            0.014,
            facecolor=ANCHOR_FILL,
            edgecolor="white",
            linewidth=1.2,
            transform=ax.transAxes,
        )
    )
    ax.text(
        0.022,
        y,
        label,
        ha="center",
        va="center",
        color="white",
        fontsize=9,
        fontweight="bold",
        transform=ax.transAxes,
    )
    # Severity badge
    badge_x, badge_w = 0.050, 0.060
    ax.add_patch(
        FancyBboxPatch(
            (badge_x, y - 0.022),
            badge_w,
            0.044,
            boxstyle="round,pad=0.005",
            facecolor=SEVERITY[severity],
            edgecolor="none",
            transform=ax.transAxes,
        )
    )
    ax.text(
        badge_x + badge_w / 2,
        y,
        severity,
        ha="center",
        va="center",
        color="white",
        fontsize=9,
        fontweight="bold",
        transform=ax.transAxes,
    )
    # Description text
    ax.text(
        badge_x + badge_w + 0.014,
        y,
        desc,
        ha="left",
        va="center",
        color=TEXT,
        fontsize=9.5,
        transform=ax.transAxes,
    )


# --- The annotation itself ----------------------------------------------


def annotate_image(img_path: str, spec: dict, out_path: str) -> Path:
    """Overlay the annotations onto an image and save it as a PNG.

    Anchors come in two shapes:
    - three elements (x_frac, y_frac, label): draw the anchor circle only
    - four elements (x_frac, y_frac, severity, desc): draw the anchor and render a fix row
      in the legend area

    Spec fields:
        title   (optional): the heading across the top.
        anchors (required): the anchors, in coordinates relative to the image size.
        fixes   (optional): the fix list, [(label, severity, desc), ...].

    Args:
        img_path: the source image.
        spec: the annotation spec for this figure.
        out_path: where the PNG goes.

    Returns:
        The Path of the file written.
    """
    img = mpimg.imread(str(img_path))
    h, w = img.shape[:2]

    anchors = spec.get("anchors", [])
    fixes = spec.get("fixes", [])
    title = spec.get("title", "")

    # Four-element anchors (x, y, severity, desc) generate their own numbers and fixes
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

    # Canvas geometry
    page_w_in = 13.0
    img_h_in = page_w_in * (h / w)
    title_h_in = 0.45 if title else 0.0
    row_h_in = 0.38
    legend_h_in = max(1.6, n_fixes * row_h_in + 0.6) if n_fixes else 0.0
    total_h_in = title_h_in + img_h_in + legend_h_in

    fig = plt.figure(figsize=(page_w_in, total_h_in), facecolor=BG)

    # Build the gridspec rows
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
        len(height_ratios),
        1,
        figure=fig,
        height_ratios=height_ratios,
        hspace=0.03,
        left=0.02,
        right=0.98,
        top=0.99,
        bottom=0.01,
    )

    axes = {name: fig.add_subplot(gs[i]) for i, name in enumerate(subplot_order)}

    # Title
    if "title" in axes:
        ax_t = axes["title"]
        ax_t.axis("off")
        ax_t.set_xlim(0, 1)
        ax_t.set_ylim(0, 1)
        ax_t.text(
            0.5, 0.5, title, ha="center", va="center", fontsize=14, fontweight="bold", color=TEXT
        )

    # Image and anchors
    ax_i = axes["img"]
    ax_i.imshow(img)
    ax_i.set_xlim(0, w)
    ax_i.set_ylim(h, 0)
    ax_i.axis("off")

    radius = min(w, h) * 0.024
    for anchor in anchors:
        xf, yf, label = anchor[0], anchor[1], anchor[2]
        _draw_anchor(ax_i, xf * w, yf * h, str(label), radius)

    # Legend area
    if "legend" in axes and n_fixes:
        ax_l = axes["legend"]
        ax_l.axis("off")
        ax_l.set_xlim(0, 1)
        ax_l.set_ylim(0, 1)

        ax_l.add_patch(
            FancyBboxPatch(
                (0.005, 0.02),
                0.99,
                0.96,
                boxstyle="round,pad=0.005",
                facecolor="white",
                edgecolor="#CCCCCC",
                linewidth=0.8,
                transform=ax_l.transAxes,
            )
        )

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


# --- CLI ----------------------------------------------------------------


def main() -> None:
    """Read SPECS from the --config JSON and annotate every figure it names."""
    parser = argparse.ArgumentParser(description="Annotate rendered figures with a fix list")
    parser.add_argument("--config", required=True, help="path to the JSON config holding SPECS")
    parser.add_argument(
        "--renders",
        default=".",
        help="directory holding the source renders (default: current directory)",
    )
    parser.add_argument(
        "--out", default="annotated", help="output directory (default: ./annotated)"
    )
    args = parser.parse_args()

    specs = load_specs(args.config)
    renders_dir = Path(args.renders)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    written = []
    for img_name, spec in specs.items():
        img_path = renders_dir / img_name
        if not img_path.exists():
            print(f"[skip] {img_name} is not present under {renders_dir}")
            continue
        stem = Path(img_name).stem
        out_path = out_dir / f"{stem}_spec.png"
        annotate_image(str(img_path), spec, str(out_path))
        written.append(out_path)
        print(f"[done] {out_path}")

    if written:
        print(f"\nwrote {len(written)} annotated figures to {out_dir}")


if __name__ == "__main__":
    main()
