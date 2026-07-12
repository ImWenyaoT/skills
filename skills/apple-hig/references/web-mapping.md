# HIG → Web mapping

The translation layer. HIG is written for native (points, gestures, SF Symbols, Taptic); this turns
each rule into **HTML / CSS / ARIA** so a web app, blog, or agent UI can genuinely satisfy it. When a
native concept has no honest web equivalent, the rule is: **don't fake it — meet the intent.**

## Contents

- [Quick map](#quick-map)
- [Targets & spacing](#targets--spacing)
- [Typography & Dynamic Type](#typography--dynamic-type)
- [Color, dark mode, contrast](#color-dark-mode-contrast)
- [Motion & Reduce Motion](#motion--reduce-motion)
- [Materials / vibrancy](#materials--vibrancy)
- [Gestures & input](#gestures--input)
- [Feedback & haptics](#feedback--haptics)
- [Accessibility (VoiceOver → ARIA)](#accessibility-voiceover--aria)
- [Component equivalents](#component-equivalents)
- [What not to fake](#what-not-to-fake)

## Quick map

| HIG concept | Web realization |
| --- | --- |
| 44 pt minimum hit target | `min-height:44px; min-width:44px` + padding + ≥8px gaps |
| San Francisco / Dynamic Type | system font stack + `rem` sizing, never disable zoom |
| Reduce Motion | `@media (prefers-reduced-motion: reduce)` |
| Dark Mode | `@media (prefers-color-scheme: dark)` + semantic CSS vars |
| Increase Contrast | `@media (prefers-contrast: more)` |
| Materials / vibrancy / Liquid Glass | `backdrop-filter: blur()` + opaque fallback |
| Sheet / modal | `<dialog>` or focus-trapped overlay; swipe/Esc/backdrop dismiss |
| Alert | `role="alertdialog"` + focus trap + labelled title/body |
| Tab bar | `role="tablist"`/nav with `aria-current`/`aria-selected` |
| Focus ring | `:focus-visible` (never bare `outline:none`) |
| VoiceOver labels | semantic HTML + `aria-label`/`aria-describedby` |
| Haptic feedback | visual/state feedback + `aria-live` (no Taptic on web) |
| SF Symbols | comparable web icon set (SF Symbols not licensed for web) |

## Targets & spacing

Make the whole actionable region the control (`<button>`/`<a>`), not just its text. Reach 44px with
`min-height/min-width` or padding; keep ≥8px between neighbors. Mobile-first at 44px, then allow denser
pointer layouts on large viewports.

## Typography & Dynamic Type

System stack for the native feel; size in `rem` so the user's browser font-size scales everything;
keep `<meta name="viewport" content="width=device-width, initial-scale=1">` **without** `user-scalable=no`
or `maximum-scale=1`. Build a text-style scale (title/headline/body/caption) and test at 200% zoom.

## Color, dark mode, contrast

Define semantic custom properties once, redefine under media queries:

```css
:root { --label:#1c1c1e; --bg:#ffffff; --accent:#0a84ff; }
@media (prefers-color-scheme: dark) { :root { --label:#f2f2f7; --bg:#000000; } }
@media (prefers-contrast: more)     { :root { --label:#000000; } }
```

Verify ≥4.5:1 (text) / ≥3:1 (large/UI). Never use color as the only signal.

## Motion & Reduce Motion

Animate `transform`/`opacity` (compositor-friendly), keep 200–350 ms, ease-in-out, and gate it:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration:.01ms!important; transition-duration:.01ms!important; }
}
```

Replace large motion/parallax with a fade or instant change — don't just speed it up if it still
triggers vestibular discomfort.

## Materials / vibrancy

```css
.bar { background: rgba(255,255,255,.72); backdrop-filter: blur(20px); }
@supports not (backdrop-filter: blur(1px)) { .bar { background:#fff; } }  /* opaque fallback */
```

Reserve translucency for transient chrome; ensure text over it still meets contrast.

## Gestures & input

Every gesture needs a visible control too. Don't block pinch-zoom. Map: tap→`click`,
long-press→contextmenu + visible "⋯", swipe-action→visible button, drag-reorder→keyboard reorder.
Set `inputmode`/`type`/`autocomplete` on inputs so the right keyboard and autofill appear.

## Feedback & haptics

No Taptic Engine on the web — never depend on a buzz. Give visual/state feedback within ~100 ms and
announce async results with `aria-live="polite"` (or `assertive` for errors).

## Accessibility (VoiceOver → ARIA)

Prefer native elements (free semantics/keyboard). Use landmarks (`<header><nav><main><footer>`),
real headings, `<label for>`, and `:focus-visible`. Add ARIA only to fill gaps: `aria-label`,
`aria-describedby`, `aria-current`, `aria-selected`, `aria-expanded`, `aria-busy`, `role="dialog"`.
Trap focus in modals, restore on close.

## Component equivalents

- Navigation bar → `<header>`/`<nav>` with title + back link + trailing actions.
- Tab bar → `role="tablist"` (or nav) + `aria-current`.
- List row → full-row `<a>`/`<button>` in a semantic list; chevron only when it drills in.
- Sheet/popover → `<dialog>` / focus-trapped overlay with multi-way dismiss.
- Toggle → `role="switch"`; Slider → `<input type="range">`; Picker → `<select>`/listbox.
- Search → `<input type="search">` inside `role="search"`.

## What not to fake

- **SF Symbols** on web (licensing). Use a comparable icon set.
- **Haptics** as a required signal (no API parity).
- **Native gesture physics** / rubber-banding pixel-for-pixel — meet the intent (clear scrolling,
  dismissal), don't ship a janky imitation.
- **A real native app** — a web UI should feel Apple-quality and consistent, not deceptively pose as
  a system app.
