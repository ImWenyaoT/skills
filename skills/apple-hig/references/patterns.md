# Patterns

How HIG composes components into **flows**. Patterns are where "feels native" is won or lost. Each
includes the web realization.

## Contents

- [Navigation](#navigation)
- [Modality & dismissal](#modality--dismissal)
- [Onboarding](#onboarding)
- [Loading / empty / error states](#loading--empty--error-states)
- [Search](#search)
- [Settings](#settings)
- [Data entry](#data-entry)
- [Undo & confirmation](#undo--confirmation)
- [Adaptivity & multitasking](#adaptivity--multitasking)

## Navigation

Pick one model per app and stay consistent:

- **Hierarchical (drill-down)** — push/pop through a tree; a navigation bar shows depth and "back".
  Good for content with clear parent/child structure.
- **Flat** — peer top-level sections via a tab bar/sidebar; switching preserves each tab's state.
- **Modal** — step out of the main flow for a self-contained task (see Modality).

Rules: people should always know **where they are, how they got here, and how to get back**. Don't mix
models confusingly (e.g., a tab that sometimes replaces the whole nav). Web: reflect location in the
URL, mark the current item (`aria-current`), and make Back behave (real history, not a dead button).

## Modality & dismissal

- Use modality for a **focused, must-finish-or-cancel** task, an important decision, or content that
  needs full attention — sparingly.
- A modal view names its task and offers a clear way out: **Cancel** (discard) and **Done/Save**
  (commit). Destructive discards confirm if work would be lost.
- Prefer **nonmodal** when people may want to reference other content or the step is optional.
- Web: `<dialog>`/overlay with focus trapped, background inert + scroll-locked, Esc and backdrop to
  dismiss, focus restored to the trigger. Don't nest modals; don't make dismissal a guessing game.

## Onboarding

- Get people to value **fast**; don't gate the app behind long tutorials. Teach in context, just-in-time.
- **Prime then request permissions** (notifications, location): explain the benefit right before the
  system prompt — never on cold launch. Respect "no" and offer a later path.
- Make first-run **skippable** and **resumable**; don't demand account creation to look around if you
  can avoid it.
- Web: progressive disclosure, inline hints, empty states that teach (below). Avoid modal carousels.

## Loading / empty / error states

Design all three for every data view — they are not edge cases:

- **Loading**: skeletons for content-shaped waits; a delayed spinner (~300 ms) for short ones; keep
  layout stable to avoid shift. Web: `aria-busy`, reserved space.
- **Empty**: explain *why it's empty* and give the **next action** ("No notes yet — Create one").
  Never show a blank screen. Distinguish "empty" from "still loading" from "error".
- **Error**: say what happened in plain language, whether it's the user's or the system's fault, and
  the recovery action (Retry / Edit / Contact). Keep the user's input. Web: announce via `aria-live`,
  focus the error, don't dump stack traces.

## Search

- Offer **recent searches / suggestions** before typing; filter live when cheap; provide **scopes**
  for large/heterogeneous result sets.
- Show counts and a useful **no-results** state (suggest alternatives, clear filters). Make clearing
  the query one tap.
- Web: `role="search"` landmark, debounced input, `aria-live` result counts, keyboard-navigable results.

## Settings

- Keep settings **shallow and grouped**; surface the few that matter, bury the rest. Use the right
  control (switch for instant binary, picker for a set). Changes apply immediately where sensible.
- Provide sensible **defaults** so most people never open settings. Don't hide core functionality there.
- Web: grouped sections with labels; switches apply instantly with feedback; destructive items (delete
  account, reset) are isolated and confirmed.

## Data entry

- Ask for the **least** information needed; pre-fill and autofill aggressively; remember prior input.
- Match the **input method** to the data: numeric keypad for numbers, email keyboard for email, date
  picker for dates. Web: `type`/`inputmode`/`autocomplete`.
- Validate kindly: inline, on blur or submit, with how-to-fix; don't punish mid-typing. Preserve
  entered values on error. Show progress for multi-step forms.

## Undo & confirmation

- Prefer **reversible actions + undo** over up-front confirmation for most operations (less friction,
  fewer dialogs). Web: a toast with **Undo** (`aria-live`), or a soft-delete + restore.
- Reserve **confirmation dialogs** for the genuinely destructive/irreversible (delete account, erase
  data). Name the consequence and the object ("Delete 3 files?"), make the destructive button distinct,
  and don't make it the easy default.
- Never silently destroy data; never confirm trivial, reversible actions (confirmation fatigue).

## Adaptivity & multitasking

- Design **responsively**: adapt to size class / viewport, orientation, split view, and external
  displays; respect **safe areas** (notch, home indicator, rounded corners) — web: `env(safe-area-inset-*)`.
- Preserve and restore **state** across resize, backgrounding, and relaunch; don't lose the user's place.
- Build **mobile-first at 44px targets**, then enhance for pointer/keyboard on larger surfaces.
