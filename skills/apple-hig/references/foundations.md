# Foundations (supporting)

The basics that every component and pattern rests on. This skill's focus is interaction/components/
patterns, so this file is a compact reference — go deep via the official pages in routing-index.md.

## Contents

- [Color](#color)
- [Typography](#typography)
- [Layout](#layout)
- [Materials](#materials)
- [Dark mode](#dark-mode)
- [Accessibility](#accessibility)
- [Icons](#icons)

## Color

- Use a small, purposeful palette: a **tint/accent** for interactive elements + neutral surfaces.
  Prefer **semantic** colors (label, secondary label, separator, fill) over hardcoded hex so they
  adapt to light/dark and contrast settings.
- **Never convey meaning by color alone** (status, selection, errors) — pair with text/icon/shape.
- Meet contrast: **≥4.5:1** body text, **≥3:1** large text and meaningful UI glyphs.
- Web: define semantic CSS custom properties (`--label`, `--fill`, `--accent`) and redefine them under
  `prefers-color-scheme` / `prefers-contrast`.

## Typography

- Use the **system font** (San Francisco on Apple platforms). On web, the system stack:
  `-apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif`.
- Follow a **type scale** with clear hierarchy (title → headline → body → caption). Native text styles
  (Large Title, Title, Headline, Body, Callout, Subhead, Footnote, Caption) map to a web `rem` scale.
- Support **Dynamic Type / user zoom**: size in `rem`, never disable zoom, keep layouts reflow-safe to
  large text. Body around 15–17 px; avoid going below ~11 pt equivalent.
- Limit weights/sizes; keep line length comfortable (~45–75 chars) and line-height generous.

## Layout

- Respect **safe areas** and readable margins; give content room to breathe (deference).
- Align to a consistent spacing rhythm (Apple lays out in points; a 4/8-pt spacing rhythm is the common,
  HIG-compatible convention on web). Maintain visual grouping via proximity and alignment.
- Design for the **smallest target first**, then adapt up; keep primary content and actions within easy
  reach. Web: `env(safe-area-inset-*)`, fluid grids, `min()/max()/clamp()`.

## Materials

- Apple uses **materials** (translucency, blur, vibrancy) so layered surfaces show context behind them
  — chrome that defers to content. The 2025 cycle introduced **Liquid Glass**, a dynamic translucent
  material across system UI.
- Use materials for transient/overlay chrome (bars, sheets, sidebars), not for dense reading content.
- Web: `backdrop-filter: blur()` with a **solid opaque fallback** (and check contrast over the blur);
  don't let translucency hurt text legibility.

## Dark mode

- Support light **and** dark as first-class. Use semantic colors that invert correctly; don't just
  swap black/white — preserve hierarchy and contrast, and dim large bright fills.
- Test both for contrast; elevate surfaces with subtle layering, not pure-black-on-pure-white.
- Web: `@media (prefers-color-scheme: dark)` redefining your semantic variables.

## Accessibility

- Accessibility is **part of the design**, not a pass at the end: VoiceOver/screen-reader labels,
  Dynamic Type, sufficient contrast, Reduce Motion, Reduce Transparency, and full keyboard/switch use.
- Web: **semantic HTML first** (landmarks, headings, lists, buttons, labels); ARIA only to fill gaps;
  honor `prefers-reduced-motion` / `prefers-contrast`; meaningful focus order; alt text; live regions
  for async updates.

## Icons

- Apple platforms use **SF Symbols** — a system icon set with weights/scales matching the system font.
  **SF Symbols are © Apple and licensed only for use on Apple platforms — do not ship them on the web.**
- On web, use a comparable open icon set, but follow the *principles*: consistent optical size and
  weight, paired with text labels, recognizable metaphors, never icon-only for critical actions
  without an accessible label (`aria-label`).
