# HIG review checklist

For the judgment pass when auditing a frontend. Walk top to bottom; for each miss report
**rule → where it's violated → the fix (with web mapping)**, then give a per-area scorecard. Pair
this with the mechanical pass (`scripts/hig_audit.py`), which catches a subset automatically.

## Contents

- [Interaction](#interaction)
- [Components](#components)
- [Patterns](#patterns)
- [Foundations](#foundations)
- [Scorecard](#scorecard)

## Interaction

- [ ] All interactive targets ≥ 44×44 px with ≥8px spacing.
- [ ] Every control shows default / hover / **focus** / active / disabled / selected / loading.
- [ ] Focus is always visible (`:focus-visible`); no bare `outline:none`.
- [ ] Fully keyboard-operable; logical tab order; Esc closes overlays; focus trapped+restored in modals.
- [ ] Gestures have visible alternatives; pinch-zoom not blocked.
- [ ] Feedback within ~100 ms for every action; async results announced (`aria-live`).
- [ ] Motion is purposeful, short, and gated by `prefers-reduced-motion`.

## Components

- [ ] Standard components used where possible; custom ones behave like the standard.
- [ ] Buttons: one dominant primary per view; verb-first labels; destructive is distinct, not default.
- [ ] Lists: whole row is the target when it navigates; chevron only for drill-in; swipe actions also visible.
- [ ] Navigation/tab bar: top sections only, current item marked, not an action dumping ground.
- [ ] Sheets/alerts: clear task name, multi-way dismissal, safe vs. destructive obvious; not stacked deep.
- [ ] Forms: visible labels (not placeholder-only), correct `type/inputmode/autocomplete`, inline errors,
      values preserved on error.
- [ ] Search/menus/selection controls use the right control and full keyboard support.

## Patterns

- [ ] One consistent navigation model; user always knows where they are and how to go back; URL reflects it.
- [ ] Modality reserved for focused/must-decide tasks; nonmodal preferred otherwise.
- [ ] Loading **and** empty **and** error states all designed (empty teaches + offers next action;
      error is plain-language + recovery + keeps input).
- [ ] Onboarding is fast/skippable; permissions primed in context, not on cold launch.
- [ ] Destructive actions: reversible + undo where possible; confirmation only for irreversible, naming
      the consequence; no confirmation fatigue.
- [ ] Settings shallow/grouped with good defaults; layout adapts to viewport and safe areas; state preserved.

## Foundations

- [ ] System font stack; `rem` sizing; zoom not disabled; body ~15–17px; legible at 200%.
- [ ] Contrast ≥4.5:1 (text) / ≥3:1 (large/UI); meaning never by color alone.
- [ ] Dark mode + `prefers-contrast` supported via semantic variables.
- [ ] Materials/translucency keep text legible (opaque fallback); not over reading content.
- [ ] Semantic HTML + landmarks/headings/labels; ARIA only to fill gaps; alt text present.
- [ ] No SF Symbols shipped on web; icon-only controls have accessible labels.

## Scorecard

Report each area as **Pass / Needs work / Fail** with the top 1–3 fixes, then the highest-priority
fix overall:

| Area | Verdict | Top fixes |
| --- | --- | --- |
| Interaction | | |
| Components | | |
| Patterns | | |
| Foundations | | |
