"""diagram_primitives.py — the shared primitives for architecture diagrams.

What every diagram script builds on:
  - SEMANTIC:      the semantic colour dict (ten fill and stroke pairs)
  - draw_box:      a labelled rounded rectangle (FancyBboxPatch)
  - connect:       a semantic arrow (fwd, cond, nograd, grad)
  - save_diagram:  writes PDF and PNG at 600 DPI, reusing figkit.plot_helpers

A paper writes a thin script that imports this module rather than reimplementing
the primitives. Layout — coordinates, labels, wiring topology — stays in that
script.
"""

from __future__ import annotations

from figkit.palette_base import ARROW_COND, ARROW_FWD, ARROW_GRAD, ARROW_NOGRAD
from figkit.plot_helpers import save_fig
from matplotlib.patches import FancyBboxPatch

# ── Semantic colour dict ─────────────────────────────────────────────────────
# Light fill against a darker stroke of the same hue. The key names cover the
# module types an architecture diagram needs most often.
SEMANTIC: dict[str, str] = {
    # Trunk and backbone blocks (GCM, DSR, PatchEmbed, Unpatchify …)
    "TEAL_FILL": "#D4E8EB",
    "TEAL_STROKE": "#2A6478",
    # Conditioning and soft-weight blocks (AdaLN, CondEmbed, Proj …)
    "AMBER": "#E8D5B0",
    "AMBER_STROKE": "#C49A3C",
    # Non-differentiable or discrete operations (argmax, sort/unsort, routing …)
    "GRAY": "#DADADA",
    "GRAY_STROKE": "#777777",
    # Refinement and post-processing heads (BAR head, fusion, smoothing …)
    "GREEN": "#CBE0C8",
    "GREEN_STROKE": "#4F7A4C",
    # The inside of an expanded block (MSA, MLP within a G-Block …)
    "SLATE": "#8DAFC0",
    "SLATE_STROKE": "#486878",
    # Frozen or external modules (DA-CLIP encoder, guidance provider …)
    "FROZEN": "#E0D8CE",
    "FROZEN_STROKE": "#A09080",
    # Bridges and structural glue (linear 768->144, upsample, skip …)
    "BRIDGE": "#E8E4D8",
    "BRIDGE_STROKE": "#8A7A5C",
    # Input and output tensor boxes
    "IO_FILL": "#FFFFFF",
    "IO_STROKE": "#333333",
}

# Arrow kind -> (colour, dashed)
_ARROW_STYLES: dict[str, tuple[str, bool]] = {
    "fwd": (ARROW_FWD, False),  # standard forward data flow
    "cond": (ARROW_COND, False),  # conditioning injection
    "nograd": (ARROW_NOGRAD, True),  # no_grad or discrete routing, dashed
    "grad": (ARROW_GRAD, False),  # backward gradient or emphasis
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
    """Draw a rounded-rectangle module on ax with a centred label.

    Parameters
    ----
    ax:       matplotlib Axes
    xy:       lower-left corner (x, y)
    w, h:     width and height, in data coordinates
    label:    the module name
    fill:     fill colour (hex string)
    stroke:   border colour (hex string)
    fontsize: label size, 9.5 by default

    Returns
    ----
    The FancyBboxPatch, already added to ax.
    """
    x, y = xy
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.08",
        facecolor=fill,
        edgecolor=stroke,
        linewidth=1.5,
        zorder=2,
    )
    ax.add_patch(box)
    ax.text(
        x + w / 2,
        y + h / 2,
        label,
        ha="center",
        va="center",
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
    """Draw a semantic arrow between two points; kind picks colour and style.

    Parameters
    ----
    ax:      matplotlib Axes
    src_xy:  arrow tail (x, y)
    dst_xy:  arrow head (x, y)
    kind:    one of "fwd", "cond", "nograd", "grad"
             - fwd:    standard forward data flow (deep teal, solid)
             - cond:   conditioning injection (amber, solid)
             - nograd: no_grad or discrete routing (grey, dashed)
             - grad:   backward gradient or emphasis (red, solid)

    Returns
    ----
    None. The annotation is already added to ax.
    """
    if kind not in _ARROW_STYLES:
        raise ValueError(f"connect: kind must be one of {list(_ARROW_STYLES.keys())}, got {kind!r}")

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
    """Save the diagram as both PDF and PNG at 600 DPI, reusing figkit.save_fig.

    Parameters
    ----
    fig:      matplotlib Figure
    out_stem: output path without a suffix, e.g. "/path/to/diag", which writes
              /path/to/diag.pdf and /path/to/diag.png

    Note: fig is closed by plt.close() on return and cannot be reused.
    """
    # save_fig closes the figure, so the PNG has to be written first and the
    # vector PDF second, through save_fig.
    from figkit.palette_base import BG

    fig.patch.set_facecolor(BG)
    fig.savefig(out_stem + ".png", dpi=600, bbox_inches="tight", facecolor=BG)
    # save_fig closes fig
    save_fig(fig, out_stem + ".pdf", dpi=600)
