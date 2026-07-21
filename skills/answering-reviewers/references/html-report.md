# The Revision Page

One self-contained HTML file carries the whole revision, from the day the decision letter lands
to the day the response letter compiles. It starts as a translation of the reviewers' words and
grows, comment by comment, into the draft of the response.

Chat is the wrong container for this. A revision holds ten to twenty comments, each with a
verbatim quote, a translation, a status, evidence, and a decision. That board gets re-read over
weeks. Scrollback loses it, and the summary drifts a little every time someone retypes it.

## Contents

- [Where it lives](#where-it-lives)
- [Reading the decision letter](#reading-the-decision-letter)
- [Marking the force of the words](#marking-the-force-of-the-words)
- [The comment card](#the-comment-card)
- [Offering the next step](#offering-the-next-step)
- [Carrying decisions back](#carrying-decisions-back)
- [Header, roll-up, and evidence](#header-roll-up-and-evidence)
- [Feeding the response letter](#feeding-the-response-letter)
- [Style](#style)

## Where it lives

`<repo-root>/.reports/revision-<manuscript-id>.html`.

Not the OS temp directory. A revision runs for weeks, `/tmp` clears on reboot, and by the second
week the path is unmemorable — the page becomes archaeology exactly when it matters most. It
belongs beside the work it describes, where reopening it is `ls -a`.

Create `.reports/` if it is absent and confirm that it is gitignored. Use a stable filename with
no timestamp, so a re-render overwrites in place and the reader only refreshes the tab. Open it
once (`xdg-open` on Linux, `open` on macOS, `start` on Windows) and give the path; after that,
just say that it refreshed.

If the work is not in a repository, fall back to the OS temp directory.

## Reading the decision letter

The letter arrives in whatever form the journal sent it: a PDF, a `.docx`, a Markdown export,
screenshots of the Editorial Manager screen, or text pasted straight into the conversation. Read
all of them. A screenshot needs your vision, a PDF needs a text extraction, and pasted text needs
nothing at all.

Two things decide whether the rest of the work stands on solid ground:

**Every comment gets an id, and the ids follow the letter's own order.** Number them `R1-1`,
`R1-2`, … per reviewer, and `E-1`, `E-2` … for the editor's summary. The order matters beyond
tidiness: the LaTeX template numbers comments with `\stepcounter`, so the sequence in the file
becomes the numbering in the compiled letter. A reordered card list silently renumbers the
response.

**The original text is copied, never paraphrased.** Paraphrase is how scope quietly drifts —
"evaluate on newer datasets" and "evaluate on LLIV-Phone or NTIRE 2024" are different specs, and
the second one is what you have to answer. Use `…` only where you genuinely omit a span.

When one numbered comment contains two separable asks, split it into `R1-4a` and `R1-4b` and say
in the card that you split it. Reviewers bundle; the response letter must still answer both, and
a bundled card hides the second ask until it is too late.

## Marking the force of the words

A reviewer's word choice carries their temperature, and Chinese translation flattens it. "Provide
concrete evidence" and "provide evidence" translate to nearly the same sentence, but the first is
a reviewer who has already decided your evidence is thin.

So in the verbatim English, bold the words that carry force. In the translation, keep the English
word in parentheses at the matching place.

The parenthesis is a backstop, not a licence to translate loosely. Spend the most care on exactly
these words: reach for the Chinese that carries the same temperature (`确凿的证据`, not `具体的
证据`, for **concrete evidence**), then put the English beside it for the residue that no
translation carries. A flat translation with an English word bolted on still reads as a neutral
request, which is the failure this whole section exists to prevent.

Five families are usually worth marking:

| Family | Examples |
|---|---|
| Demand strength | must, should, need to, is required, I insist, please ensure |
| Evidence bar | **concrete**, rigorous, convincing, quantitative, controlled, systematic, thorough |
| Negative judgement | unclear, insufficient, limited, out of date, too few, weak, overlooked, fails to |
| Absolutes | any, all, every, none, never, only, the best |
| Temperature | my most concerning, I am not convinced, surprising, questionable |

Mark what changes how you would act, and leave the rest alone. A card with fifteen bold words
carries no more signal than a card with none — the eye stops separating them. Three or four per
comment is usually where the meaning sits.

## The comment card

One `<article>` per comment. This is the heart of the page, and it grows over the weeks.

- **Badge row** — the id (`R1-3`), a status pill (`未开始` slate / `进行中` amber / `已完成`
  emerald), and a tag for what the comment demands (`实验` / `写作` / `数据` / `格式`).
- **原文** — the verbatim English in a serif face, inside a bordered quote block, with the forceful
  words bold.
- **译文** — the Chinese underneath, visually lighter, carrying the English original in
  parentheses wherever a marked word sits.
- **现状** — one or two sentences on what is actually true right now.
- **证据** — the number, table row, or figure that answers the comment. While it is empty it
  renders as a dashed grey box reading `尚无证据`, never as optimistic prose. "Planned", "will
  do", and "should improve" are not evidence; they belong under the next step.
- **下一步** — the options, and the chosen one. See below.
- **回复草稿** — the English paragraph that will become `\begin{reviewerresponse}`. Empty at
  first. This is what makes the page grow into the letter rather than merely describe it.
- **稿件改动** — the exact revised manuscript wording, when there is one. Becomes
  `\begin{changes}`.
- **位置** — where it lands (`Sec. 4.3, Table 5`). This is what the response letter cites.

Cards for closed comments collapse to a lighter border and a muted background, so the eye lands
on the open ones.

## Offering the next step

Each open comment carries two or three routes, not one instruction. The author knows things the
page does not: which GPU is free, which experiment already half-ran, how much of the deadline is
really left.

A useful option set usually spans the range the ladder describes — do it in full, do it at reduced
scope, or answer it in prose. Give each option its cost, its risk, and one line on what it buys.
The reduced-scope option is the one most often correct under a deadline, and it is also the one an
author under pressure forgets exists.

```
下一步 · 三选一
  A 全量   Lab + Luv + CIECAM02 三组受控对照   ~6 GPU天   最稳
  B 降级   只做 Lab + Luv(审稿人点名的前两个)  ~3 GPU天   推荐 · CIECAM02 在信里说明缺席理由
  C 只写   引文献论证 HVI 合理性               0 GPU      风险高 · R1 明确要了 ablation
```

Mark one option as recommended and say why in one clause. A page that recommends nothing pushes
the whole decision back to the reader, which is the work the page exists to reduce.

**The options are a starting set, not the whole space.** They exist to cut the cost of deciding,
by showing the routes that are already understood and what each one costs. The author knows
things the page does not — a colleague with the dataset, a reviewer's known preference, an idea
that arrived this morning. So every card carries a fourth choice, `另议`, with a free-text field,
and picking it is a legitimate outcome rather than a failure to decide. When it is chosen, the
next move is a conversation, and the page records what came out of that conversation.

Write the options as a recommendation with its reasoning attached, never as a verdict. The
difference shows in one word: *"B is recommended — the two colour spaces R1 named cost 3 GPU days
and CIECAM02 can be addressed in prose"* invites disagreement on the reasoning; *"Choose B"*
does not.

An option that answers no comment id does not belong here at all. Unasked work is a new attack
surface paid for with the hours the asked-for work needed.

## Carrying decisions back

The page is where decisions get made, so the page has to be able to hand them back.

Each card's options are radio inputs, and the status pill is clickable. Persist both to
`localStorage` under the manuscript id, so a refresh, a re-render, or a closed laptop does not
lose an afternoon of decisions.

A fixed bar at the bottom shows how many comments have a decision, and holds one button that
copies a compact digest to the clipboard:

```
KNOSYS-D-26-06552 · 2026-07-21 · 决策 7/11
R1-1 done
R1-2 doing
R1-3 todo  → B  Lab+Luv only, CIECAM02 explained in letter
R1-4 todo  → 另议  先问问同组有没有 LLIV-Phone 的镜像
```

Plain text and nothing else. It has to survive a paste into any agent, and some never render a
chooser while others run headless. Keep it short enough to paste without scrolling: ids,
statuses, choices, and one clause of reasoning each.

This is the one place where the page behaves as an application rather than a document. Everything
else stays static — no framework, no router, no build step. The interaction exists because the
alternative is the author reciting fifteen decisions into a chat box and mistyping one.

### Anchors the generator reads

The digest carries decisions; the letter needs content. Rather than export a second file that can
drift from the page, the letter generator parses the page itself, so give it stable hooks:

- each card is `<article class="comment-card" data-comment-id="R1-3" data-status="todo">`
- the fields carry fixed class names: `.verbatim`, `.translation`, `.status-now`, `.evidence`,
  `.response-draft`, `.manuscript-change`, `.location`
- the chosen option sits on the card as `data-choice="B"`
- document order equals letter order

One file holds the truth, and the parser fails loudly when a hook is missing rather than emitting
a letter with a silent gap.

## Header, roll-up, and evidence

**Header** — manuscript title, journal, manuscript number, decision type, and the **due date with
days remaining** rendered large. Under fourteen days, colour it red. Every scope decision on the
page is downstream of that number.

**Roll-up** — one row of counters (`已完成 / 进行中 / 未开始`) over the total, plus a thin
progress bar. The denominator counts every numbered comment from every reviewer plus every
distinct point in the editor's summary. That is the completion criterion, made visible.

**Evidence section** — the tables the revision has produced, each titled with the comment id it
serves (`R2-4 · 模块级消融`). Bold the row that is the answer. If a result is preliminary — one
seed, a short schedule — say so in the caption. A number that serves no comment id is worth
questioning: either it answers something nobody asked, or its card is missing.

## Feeding the response letter

The template lives in [`../assets/response-letter/`](../assets/response-letter/). The card fields
map onto it directly:

| Card field | LaTeX |
|---|---|
| 原文 (verbatim) | `\begin{reviewercomment}` |
| 回复草稿 | `\begin{reviewerresponse}` |
| 稿件改动 | `\begin{changes}` (nested inside the response) |
| 位置 + 现状 | one `\item` in *Summary of Revisions Made*, ending `\emph{Addresses R1-3.}` |
| header metadata | the six `\my…` commands in `main.tex` |

Generate the skeleton once the verbatim text and the ids are settled — the comment blocks carry
no risk, because they are quotations. Fill responses in as they become true.

[`../scripts/render_letter.py`](../scripts/render_letter.py) does the mechanical half: it reads
the page, escapes the LaTeX specials, and writes one file per reviewer plus the substituted
metadata. Escaping a reviewer's `%` or `&` by hand is exactly the work that should never depend
on attention.

```bash
python3 scripts/render_letter.py .reports/revision-<id>.html --out paper/response_letter
```

It refuses to write a card whose verbatim text is missing, because a silently empty
`reviewercomment` is a response letter that answers a question the reviewer never sees.

The order of the environments in each `Reviewers/*.tex` sets the printed numbering, so emit them
in the letter's own order and never sort them by status or by how finished they are.

Only text that describes work that exists may cross from the page into the letter. A promise in a
response letter is something the reviewer can hold you to on a round that may not come.

## Style

Editorial and generous with whitespace. One accent colour, red reserved for the deadline, amber
for in-progress. Chinese body text with English verbatim quotes in a serif face, so the eye
separates *their words* from *our words* without effort. Tables scroll inside their own
`overflow-x-auto`; the page body never scrolls sideways.

The page is an instrument, not a pitch. If a comment still has no evidence with eight days left,
looking at it should be uncomfortable. That discomfort is the feature.
