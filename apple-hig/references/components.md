# Components

HIG components with their **anatomy, behavior, web equivalent, and do/don't**. Reach for a standard
component before inventing one; if you build custom, make it *behave* like the standard.

## Contents

- [Navigation bar](#navigation-bar)
- [Tab bar / sidebar](#tab-bar--sidebar)
- [Buttons](#buttons)
- [Lists & tables](#lists--tables)
- [Sheets & popovers](#sheets--popovers)
- [Alerts & action sheets](#alerts--action-sheets)
- [Forms & text fields](#forms--text-fields)
- [Selection controls](#selection-controls)
- [Search](#search)
- [Menus](#menus)
- [Segmented control](#segmented-control)
- [Progress indicators](#progress-indicators)

## Navigation bar

- **Anatomy**: title (large or inline), a back affordance on the leading side, ≤1–2 actions trailing.
- **Behavior**: title can collapse from large → inline on scroll; the back control shows where "back"
  goes. Don't crowd it; move overflow into a menu.
- **Web**: a top `<header>`/`<nav>` with the page title and a clear back link; keep actions to the
  right, collapse extras into a "⋯" menu. Mark the current location.
- **Don't**: put unrelated global actions here, or use it as a toolbar dumping ground.

## Tab bar / sidebar

- **Tab bar** = top-level, **flat** navigation across 3–5 peer sections; persistent; one selected at a
  time; tapping the active tab scrolls to top / pops to root. Don't use it for actions or for >5 items.
- **Sidebar** (iPad/Mac) = the same role with more room and nesting.
- **Web**: bottom tab bar (mobile) or sidebar (desktop) of `<a>`/`<button role="tab">`; mark the
  active one with `aria-current="page"`/`aria-selected`. Keep it to the app's top sections.

## Buttons

- **Roles**: primary (the preferred action, visually dominant — one per view), secondary/neutral,
  and **destructive** (distinct, usually red, never the default focus).
- **Labels**: verb-first and specific ("Save Draft", not "OK"). Sentence/title case per platform.
- **States**: see interaction.md → Control states. Loading buttons stay sized to avoid layout shift.
- **Web**: `<button>` (never a clickable `<div>`). Express role with style + `aria`; size to ≥44px;
  give every state. Destructive actions get confirmation/undo (patterns.md).
- **Don't**: have two competing primaries; disable the primary with no explanation.

## Lists & tables

- **Anatomy**: rows with a label, optional secondary text, leading icon, and a trailing accessory
  (chevron = drill-in, switch, checkmark, detail). Group with section headers/footers.
- **Behavior**: the **whole row** is the target when it navigates; swipe reveals row actions (with a
  visible alternative); support pull-to-refresh / edit mode where relevant.
- **Web**: semantic list (`<ul>`/`<table>`); make the full row an `<a>`/`<button>`; expose swipe
  actions as visible buttons too; use a real chevron only when the row drills in.
- **Don't**: hide the only path to an action behind a swipe; use a table for non-tabular layout.

## Sheets & popovers

- **Sheet** = a modal/semi-modal surface sliding from an edge for a **self-contained, focused** task;
  supports detents (partial/full height) and swipe-down to dismiss; keep it shallow.
- **Popover** = a transient panel anchored to its trigger (pointer/iPad context).
- **Web**: `<dialog>` or a focus-trapped overlay; dismiss via swipe-down, Esc, backdrop tap, and an
  explicit Done/Close; move focus in on open and restore on close; lock background scroll.
- **Don't**: stack sheets deeply, or trap the user with no obvious dismissal.

## Alerts & action sheets

- **Alert** = brief, **interrupting** message needing a decision: short title, optional one-line body,
  ≤2–3 buttons. The safe/cancel choice is clear; the **destructive** choice is visually distinct.
- **Action sheet / menu** = a set of choices related to the current context, presented from the
  triggering control or screen edge.
- **Web**: `role="alertdialog"` with focus trap and a labelled title/description; default focus on the
  safe action; Esc cancels. Don't use alerts for non-critical info — prefer inline/toast.
- **Button order**: keep Cancel and the affirmative/destructive action positions consistent with the
  target platform; never make destructive the easy-to-hit default.

## Forms & text fields

- **Field**: a clear label (visible, not placeholder-only), the input, and helper/error text. Group
  related fields; one idea per field.
- **Behavior**: validate at the right time (on blur / on submit, not keystroke-nagging); show errors
  inline next to the field with how to fix; keep submitted values.
- **Web**: `<label for>` + `<input>`; set `type`/`inputmode`/`autocomplete` so the right keyboard and
  autofill appear; link errors with `aria-describedby` and set `aria-invalid`; never rely on
  placeholder as the label.
- **Don't**: clear the form on error; block paste; hide the requirements until after a failed submit.

## Selection controls

- **Toggle/switch**: immediate, binary, *no* confirm button — flipping it *is* the action. Web:
  `role="switch"` / styled checkbox; reflect state by more than color.
- **Slider**: continuous range; show the value; allow keyboard arrows. Web: `<input type="range">`.
- **Stepper**: small discrete +/− changes. **Picker**: choose from a set (date/time/options). Web:
  `<select>` or a custom listbox with full keyboard support.
- **Don't**: use a switch for an action that needs confirmation; use a slider where exact values matter.

## Search

- **Anatomy**: a search field (magnifier glyph, placeholder, clear button), optional scope bar,
  results, and recents/suggestions.
- **Behavior**: filter as you type when cheap; show recent/suggested before input; make "clear" easy;
  show a helpful empty-results state.
- **Web**: `<input type="search">` in a `role="search"` landmark; debounce; announce result counts via
  `aria-live`; keyboard-navigable suggestions (`aria-activedescendant`).

## Menus

- **Context/pull-down menu** = a list of actions/options from a control or long-press. Group and order
  by frequency; mark current selections; put destructive items last and distinct.
- **Web**: `role="menu"`/`menuitem` with arrow-key navigation and Esc to close, or a native `<select>`
  for simple option choice. Anchor to the trigger; restore focus on close.

## Segmented control

- A small set (2–5) of **mutually exclusive** views/filters shown inline; one selected at a time.
- **Web**: `role="tablist"` of `role="tab"`, or radio group; reflect selection beyond color. Don't use
  it for actions or for many/long labels — that's a picker or tabs.

## Progress indicators

- **Determinate** (bar) when you know the proportion; **indeterminate** (spinner) when you don't.
- Show progress for anything > ~1 s; for very short waits, avoid flicker (delay the spinner ~300 ms or
  use a skeleton). Keep layout stable.
- **Web**: `<progress>` or a spinner with `aria-busy`/`aria-live`; reserve space to prevent layout shift.
