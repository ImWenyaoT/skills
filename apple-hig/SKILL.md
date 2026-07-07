---
name: apple-hig
description: Use when building, refining, or reviewing the interaction, components, and patterns of a frontend — web app, blog, dashboard, or agent/chat UI — so it genuinely follows Apple's Human Interface Guidelines (HIG). Covers HIG components (navigation bar, tab bar, buttons, lists, sheets, alerts, forms, pickers, search, menus), interaction (touch targets, gestures, focus, states, feedback, motion), and patterns (modality, onboarding, loading/empty/error states, settings, data entry, confirmation), and maps each HIG rule to web HTML/CSS/ARIA; also answers native iOS/iPadOS/macOS/watchOS/tvOS/visionOS HIG questions. 触发词:让我的 blog/网页/agent 界面符合 Apple HIG、苹果设计规范、组件交互模式、像原生一样、HIG 审查。Do not use for Android or Material Design, generic chart/figure/diagram drawing, or non-UI backend logic.
---

# apple-hig

Make a frontend's **interaction, components, and patterns** genuinely satisfy Apple's Human
Interface Guidelines (HIG) — most often a **web** surface (web app, blog, dashboard, agent/chat
UI), and also native Apple platforms when asked. HIG is written in points, gestures, and SF
Symbols; this skill keeps the *intent* of each rule and **translates it to HTML/CSS/ARIA** so a
web UI feels native-quality without pretending to be a native app.

This is a **focused reference + review** skill. It does not draw charts/figures, does not cover
Android/Material Design, and does not write backend logic.

## How this skill loads (progressive disclosure)

1. **Always read the "Non-negotiables" below first** — they hold for every Apple-quality UI.
2. **Identify the target surface**: web (default) vs. a specific native platform. Web rules map
   through [references/web-mapping.md](references/web-mapping.md).
3. **Scan the task for the topic**, then open the matching reference via
   [references/routing-index.md](references/routing-index.md) (keyword → file + official Apple URL).
   Read only the file(s) you need.
4. **Answer with the rule + the concrete mapping** (e.g. "≥44×44 pt → `min-height/min-width: 44px`"),
   and cite the official HIG page from the routing index for anything beyond this bundle.
5. **For "is my UI compliant?" requests**, switch to Review mode (below).

## The HIG mindset (apply before any specific rule)

- **Clarity** — legible text at every size, precise icons, generous negative space; content is
  the focus, chrome recedes.
- **Deference** — UI helps people understand and interact with content, never competes with it;
  prefer translucency/blur and restrained color over heavy decoration.
- **Depth** — distinct visual layers and purposeful motion convey hierarchy and give feedback;
  transitions explain where things came from and where they go.
- **Consistency** — reuse standard components and platform conventions so behavior is predictable;
  surprise is a cost, not a feature.

## Non-negotiables (tier-1, always true)

These are the rules a HIG-quality UI must not break, with their web mapping:

- **Hit targets ≥ 44×44 pt.** Every tappable/clickable control. Web: `min-height:44px;min-width:44px`
  (or padding to reach it); keep ≥8px between adjacent targets.
- **Type stays legible and scalable.** Use the system font stack; never ship body text below ~11 pt
  (≈15–17 px on web for body). Web: `font: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI",
  Roboto, Helvetica, Arial, sans-serif`; size in `rem` and honor the user's font size — never disable zoom.
- **Contrast ≥ 4.5:1** for normal text, ≥3:1 for large text/UI glyphs. Never encode meaning by
  **color alone** — pair with text, icon, or shape.
- **Respect system preferences.** Dark mode → `prefers-color-scheme`; reduced motion →
  `prefers-reduced-motion` (drop/replace non-essential animation); increased contrast →
  `prefers-contrast`. These are requirements, not enhancements.
- **Every control has all its states.** default · hover (pointer) · focus (visible ring) · active/pressed ·
  disabled · loading · selected. A focus state that is invisible is a bug. Web: never `outline:none`
  without an equally-visible replacement.
- **Feedback is immediate and proportional.** Acknowledge every action within ~100 ms (state change,
  spinner, or haptic on native). Destructive/irreversible actions need confirmation or undo.
- **Motion has purpose and an off switch.** Use motion to show hierarchy and continuity, keep it short
  (~200–350 ms), ease in/out, and gate it behind `prefers-reduced-motion`.
- **One primary action per view.** Make the preferred choice visually dominant; demote or remove the rest.
- **Standard components over custom.** Reach for the platform/standard control first; only build custom
  when a standard one genuinely can't express the need — then make it behave like the standard.

## Interaction · Components · Patterns (the core)

This skill's weight is here. Open the file that matches the task:

- **Interaction** → [references/interaction.md](references/interaction.md): touch targets, gestures →
  pointer/keyboard, focus order, control states, feedback & haptics, transitions/motion.
- **Components** → [references/components.md](references/components.md): navigation bar, tab bar, buttons,
  lists/tables, sheets, alerts & action sheets, forms & text fields, pickers/toggles/sliders/steppers,
  search, menus, segmented controls — anatomy, behavior, web equivalent, do/don't.
- **Patterns** → [references/patterns.md](references/patterns.md): navigation (hierarchical/flat/modal),
  modality & dismissal, onboarding, loading/empty/error states, search, settings, data entry,
  undo & confirmation, multitasking/adaptivity.
- **Foundations (supporting)** → [references/foundations.md](references/foundations.md): color, typography,
  layout/spacing, materials/vibrancy, dark mode, accessibility, icons (and why SF Symbols are not
  redistributable for web).
- **Per-platform deltas** → [references/platforms.md](references/platforms.md): how Web/PWA, iOS, iPadOS,
  macOS, watchOS, tvOS, and visionOS differ on the same component/pattern.

## Web translation, in one line each

Full table in [references/web-mapping.md](references/web-mapping.md). The high-frequency ones:

| HIG concept | Web realization |
| --- | --- |
| 44 pt hit target | `min-height:44px; min-width:44px` + spacing |
| SF Pro / Dynamic Type | system font stack + `rem` sizing, respect user zoom |
| Reduce Motion | `@media (prefers-reduced-motion: reduce)` |
| Dark Mode | `@media (prefers-color-scheme: dark)` + semantic CSS vars |
| Materials / vibrancy | `backdrop-filter: blur()` with a solid fallback |
| VoiceOver | semantic HTML first, ARIA only to fill gaps |
| Sheet / modal | `<dialog>` or focus-trapped overlay, swipe/Esc to dismiss |
| Haptic feedback | visual/state feedback on web (no Taptic); never rely on it |
| SF Symbols | use a comparable web icon set — SF Symbols are not licensed for web |

## Review mode — "is my UI HIG-compliant?"

When asked to audit/grade an existing frontend:

1. Run the mechanical pass: `scripts/hig_audit.py` flags high-signal, machine-checkable violations
   (sub-44px targets, `outline:none` without replacement, missing `prefers-reduced-motion` /
   `prefers-color-scheme`, non-system fonts, color-only state). It cannot judge layout, semantics,
   or copy — treat it as a smoke test, not a verdict.

   ```bash
   uv run apple-hig/scripts/hig_audit.py path/to/src            # scan a dir
   uv run apple-hig/scripts/hig_audit.py styles.css index.html  # or specific files
   ```

2. Do the judgment pass with [references/review-checklist.md](references/review-checklist.md) —
   walk interaction → components → patterns → foundations and report each finding as
   **rule → where it's violated → the fix (with the web mapping)**, citing the official HIG page.

3. Summarize as a short scorecard (pass / needs-work per area) plus the prioritized fixes.

## Sources & attribution

Guidance here is **distilled in our own words** from Apple's Human Interface Guidelines; deep-dive
links in [references/routing-index.md](references/routing-index.md) point to the canonical pages at
`developer.apple.com/design/human-interface-guidelines`. HIG text and SF Symbols are © Apple Inc.;
this skill is an independent reference and is not affiliated with or endorsed by Apple.
