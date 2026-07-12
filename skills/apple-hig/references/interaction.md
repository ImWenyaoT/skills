# Interaction

How Apple-quality UIs respond to people: targets, gestures, pointer/keyboard, focus, states,
feedback, and motion. Each rule includes the **web realization** so it applies to a web app, blog,
or agent UI — not just native.

## Contents

- [Touch targets](#touch-targets)
- [Gestures (and their web/pointer equivalents)](#gestures-and-their-webpointer-equivalents)
- [Pointer & keyboard](#pointer--keyboard)
- [Focus](#focus)
- [Control states](#control-states)
- [Feedback & haptics](#feedback--haptics)
- [Motion](#motion)

## Touch targets

- **Minimum 44×44 pt** for any interactive element on touch surfaces. Small visuals (a 20px icon)
  still need a 44px tappable area via padding.
- Keep **≥8 pt spacing** between adjacent targets so people don't hit the wrong one.
- The hit area should match the *visual affordance* — don't make a tiny chevron the only target when
  the whole row is meant to be tappable.
- Web: `min-height:44px; min-width:44px;` or `padding` to reach it. Make the whole row/card the
  `<button>`/`<a>`, not just the label. Pointer-only UIs (desktop web) can go smaller, but design
  mobile-first at 44px.

## Gestures (and their web/pointer equivalents)

- Gestures are **shortcuts, not the only way** — every gesture-driven action must have a visible
  control too (discoverability + accessibility).
- Use **standard gestures** with their expected meaning: tap = activate, swipe = scroll/reveal,
  long-press = contextual menu, edge-swipe = back/system. Don't redefine them.
- Web mapping:
  - tap → `click`; long-press → contextmenu / press-and-hold timer **plus** a visible "⋯" menu.
  - horizontal swipe-to-delete on a list → also expose a visible delete/edit affordance.
  - pinch-zoom → never block it (`user-scalable=no` is an accessibility failure).
  - drag-and-drop → provide keyboard reordering as well.

## Pointer & keyboard

- On pointer surfaces (Mac, iPad+trackpad, desktop web) controls get **hover** feedback and the
  pointer can change shape over actionable content.
- **Full keyboard operability is mandatory.** Everything reachable and operable by Tab/Shift-Tab,
  Enter/Space, arrows, and Esc. Provide shortcuts for frequent actions.
- Logical **tab order** follows reading/visual order. Don't trap focus except inside an open modal.
- Web: prefer native interactive elements (`<button>`, `<a href>`, `<input>`) — they are keyboard-
  and AT-operable for free. If you must make a `<div>` interactive, add `role`, `tabindex="0"`, and
  key handlers, and you now own every state the native element gave you.

## Focus

- **Focus must always be visible.** A clear focus indicator (ring/halo) shows where keyboard or
  remote focus is. On tvOS the focused element lifts/scales (the focus engine).
- Move focus deliberately: opening a modal moves focus into it and returns focus to the trigger on
  close. New content shouldn't steal focus unexpectedly.
- Web: never `outline:none` without an equally-visible replacement. Use `:focus-visible` to show the
  ring for keyboard users; trap focus inside `<dialog>`/overlays and restore it on dismiss.

## Control states

Every control must visibly express all the states that apply to it:

| State | Meaning | Web cue |
| --- | --- | --- |
| default | resting | base style |
| hover | pointer over (pointer devices only) | `:hover` |
| focus | keyboard/remote target | `:focus-visible` ring |
| active / pressed | during the press | `:active` |
| selected | persistent chosen state | `aria-selected` / `aria-pressed` |
| disabled | not available now | dimmed + `disabled`/`aria-disabled` (still discoverable) |
| loading | working | spinner/progress + `aria-busy` |

- Don't signal a state by **color alone** — add an icon, label, weight, or shape.
- A disabled control should explain *why* nearby when the reason isn't obvious; prefer enabling +
  validating over a permanently dead button.

## Feedback & haptics

- **Acknowledge every action within ~100 ms** — a state change, highlight, spinner, or haptic. Silence
  reads as "broken."
- Match feedback to weight: subtle for routine actions, distinct for success/failure, **confirmation
  or undo** for destructive/irreversible ones.
- Native haptics (Taptic Engine) reinforce events but are **supplementary** — never the only signal.
- Web: there is no Taptic Engine; rely on visual/state feedback (and `aria-live` for async results).
  Never design an interaction that *depends* on a buzz.

## Motion

- Motion exists to **show hierarchy, continuity, and feedback** — where something came from, where it
  goes, that an action registered. Decorative motion that doesn't inform is deference debt.
- Keep it **short (~200–350 ms)** and eased (ease-in-out); avoid long, blocking, or looping animation.
- **Reduce Motion is a requirement.** Replace large movement/parallax with a cross-fade or instant
  change when the user asks for less motion.
- Web: `@media (prefers-reduced-motion: reduce) { /* shorten or remove non-essential animation */ }`.
  Animate cheap properties (`transform`, `opacity`); don't animate layout.
