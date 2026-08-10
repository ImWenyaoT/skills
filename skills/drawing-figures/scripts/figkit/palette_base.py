"""figkit.palette_base — the backdrop, arrow grammar, typography, and scatter
conventions shared by every figure.

A paper's figures/scripts/palette.py needs only:
    from figkit.palette_base import *          # backdrop, arrows, type, scatter
and then defines the semantic module colours specific to that paper (a module's
fill and stroke). One backdrop, per-paper module colours — which is what stops
two palette.py files from each reinventing the backdrop and the arrow grammar.
"""

# ── Backdrop (page and panel, identical across every figure) ─────────────
BG = "#FAFAF8"  # page background
PANEL = "#FFFFFF"  # plotting-area background
TEXT = "#333333"  # primary text
MUTED = "#666666"  # secondary text
RULE = "#CCCCCC"  # grid lines and light rules

# ── IO tensor boxes (input and output, neutral) ──────────────────────────
IO_FILL = "#FFFFFF"
IO_STROKE = "#333333"

# ── Arrow grammar (identical across every architecture diagram) ──────────
ARROW_FWD = "#3A5A6A"  # standard forward data flow
ARROW_COND = "#C49A3C"  # conditioning injection (amber)
ARROW_NOGRAD = "#888888"  # no_grad or discrete routing (usually dashed)
ARROW_GRAD = "#B94A48"  # backward gradient or emphasis
ACCENT = "#7952B3"  # optional accent

# ── Scatter points (the shared "ours vs baselines" convention) ───────────
POINT_OURS_FILL = "#B94A48"  # our method: red
POINT_OURS_STROKE = "#7A2A2A"
POINT_BASE_FILL = "#5B9EA6"  # baselines: teal
POINT_BASE_STROKE = "#2A6478"

# ── Typography (font sizes) ──────────────────────────────────────────────
FONT_TITLE = 12
FONT_AXIS = 10.5
FONT_TICK = 9.5
FONT_LABEL = 9.5
FONT_ANN = 9.0
FONT_LEGEND = 9.5
FONT_FOOTER = 8.5


def with_modules(**module_colors):
    """Merge this paper's semantic module colours into the shared backdrop.

    Used from a paper's own palette.py:
        from figkit.palette_base import with_modules
        PALETTE = with_modules(GCM_FILL="#D4E8EB", GCM_STROKE="#2A6478", ...)
    The returned dict holds both the shared keys (BG, PANEL, ARROW_*, FONT_*)
    and the module colours passed in, so a drawing script can look every colour
    up by name.
    """
    base = {k: v for k, v in globals().items() if k.isupper() and isinstance(v, (str, int, float))}
    base.update(module_colors)
    return base
