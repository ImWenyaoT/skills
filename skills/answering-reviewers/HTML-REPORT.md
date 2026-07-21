# Revision Dashboard (HTML)

The revision state is rendered as a single self-contained HTML file under the project's ignored `.reports/` directory. Tailwind comes from a CDN. No build step, nothing tracked.

Why HTML and not chat: a revision has 10–20 comments, each with an original quote, a translation, a status, and evidence. That is a table the reader scans and re-scans over weeks — chat scrollback is the wrong container for it.

## When to render

- The user asks for status ("现在怎么说", "what now", "进展如何").
- A batch of experiments lands and the per-comment status changes.
- Before the user makes a scope decision — they need the whole board, not a slice.

## Where it lives

`<repo-root>/.reports/revision-<manuscript-id>.html`.

**Not the OS temp directory.** A revision runs for weeks. `/tmp` is cleared on reboot, and by the second week the path is unmemorable — the dashboard becomes archaeology exactly when it is most needed. It belongs beside the work it describes, where reopening it is `ls -a`.

Create `.reports/` if absent and make sure it is gitignored — add the entry if it is missing. The page is a working instrument, not a tracked artifact; it is regenerated from the truth, never edited by hand.

Use a **stable filename with no timestamp**, so re-rendering overwrites in place and the reader's open tab only needs a refresh. Open it (`xdg-open` Linux, `open` macOS, `start` Windows) the first time and give the user the path; on later renders just say it refreshed.

If the work is not in a repo at all, fall back to the OS temp directory.

## Non-negotiables

**Verbatim originals.** The skill requires quoting each comment verbatim; the dashboard is where that text lives. Never paraphrase the original in the card — paraphrase belongs in the translation slot only.

**Deadline first.** The revision due date and days remaining go in the header, large. Every scope decision is downstream of it.

**Evidence, not intentions.** A comment's card shows the number that answers it, or it shows nothing. "Planned", "will do", "should improve" are not evidence and must not appear in the evidence slot — they belong in *Next action*. This mirrors the skill's *only report work that exists*.

## Scaffold

```html
<!doctype html>
<html lang="zh">
  <head>
    <meta charset="utf-8" />
    <title>Revision — {{journal}} {{ref}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
      .verbatim { font-family: ui-serif, Georgia, serif; }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900">
    <main class="max-w-6xl mx-auto px-6 py-10 space-y-10">
      <header>…</header>
      <section id="rollup">…</section>
      <section id="editor">…</section>
      <section id="comments">…</section>
      <section id="evidence">…</section>
      <section id="next">…</section>
    </main>
  </body>
</html>
```

## Header

Manuscript title, journal, manuscript number, decision (Revise / Major / Minor), and the **due date with days remaining** rendered large. If under 14 days, colour it red.

## Roll-up

One row of counters: `已完成 / 进行中 / 未开始` out of the total comment count, plus a thin progress bar. The denominator counts **every numbered comment from every reviewer plus every distinct point in the editor's summary** — the skill's completion criterion, made visible.

## Comment card

One `<article>` per comment. This is the heart of the page.

- **Badge row** — comment id (`R1-3`), status pill (`已完成` emerald / `进行中` amber / `未开始` slate), and a tag for what it demands (`实验` / `写作` / `数据` / `格式`).
- **原文** — verbatim English in `.verbatim`, in a bordered quote block. Never edited, never trimmed mid-sentence (use `…` only for genuinely omitted spans).
- **译文** — the Chinese rendering directly beneath, visually lighter (`text-slate-600`).
- **现状** — one or two sentences. What is actually true right now.
- **证据** — the number, table row, or figure that answers this comment. Empty state renders as a dashed grey box reading `尚无证据`, not as optimistic prose.
- **下一步** — the concrete next action, or `—` if the comment is closed.
- **位置** — where it lands in the revised manuscript (`Sec. 4.3, Table 5`). Fill in as it becomes true; this is what the response letter will cite.

Cards for closed comments collapse visually (lighter border, muted background) so the eye lands on the open ones.

## Evidence section

Tables of the numbers the revision has produced — ablations, baselines, controlled comparisons. Each table titled with the comment id it serves (`R2-4 · 模块级消融`). A number with no comment id has no business in a revision and should be questioned.

Highlight the row that is the *answer* (bold, or an accent left-border). If a result is preliminary (single seed, short schedule), say so in the caption — the skill's consistency rule applies to the dashboard too.

## Next steps

Ordered list, grouped by whether the item is blocked on GPU, on writing, or on a user decision. Each item carries the comment id it serves. Items serving no comment id get flagged — they are the unasked work the skill warns about.

## Style

- Editorial, generous whitespace, one accent colour plus red for the deadline and amber for in-progress.
- Chinese body text with English verbatim quotes: give the quotes a serif face so the eye separates *their words* from *our words* instantly.
- Tables scroll inside `overflow-x-auto`; the page body never scrolls sideways.
- No JS beyond the Tailwind CDN. The page is a document, not an app.

## Tone

The dashboard is an instrument, not a pitch. It shows what is done, what is not, and what the deadline is. If a comment has no evidence with eight days left, the page should make that uncomfortable to look at — that discomfort is the feature.
