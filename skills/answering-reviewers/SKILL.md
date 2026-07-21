---
name: answering-reviewers
description: Answers reviewer comments on a major/minor revision — treats each comment as a spec to implement, not a claim to debate, and holds the work to that spec's scope. Use when the user has a revision decision, reviewer comments, an editor's summary, a point-by-point response to reviewers, 修回, 返稿, 逐条回应, 审稿意见, or asks how to handle a specific reviewer point. Also use when the user is deciding which requested experiments to run, is about to argue that a reviewer is wrong, is considering extra experiments nobody asked for, or asks where the revision stands (进展, 现在怎么说, what now). Does not draft or polish the manuscript prose itself, and does not assemble the Editorial Manager upload packet.
---

# Answering Reviewers

A revision decision means the editor already decided the paper can be saved. The reviewers have told you what they will not accept. Your job is to remove each objection — **the ask is the spec**.

The failure this skill prevents: an author who is technically right and rejected anyway.

## The ask is the spec

Read each comment as a work item, not as a proposition to evaluate. A spec you disagree with is still a spec.

This holds even when the reviewer is factually wrong (they often are — see [Wrong premises](#wrong-premises)). Being right about the science and wrong about the politics still ends in rejection.

**Completion criterion:** every numbered comment from every reviewer, plus every point in the editor's summary, has its own entry in the response. The editor's summary is a separate spec — it is what the person who decides your fate chose to emphasize. Comments that seem trivial (font sizes, a missing citation) get entries too; they are the cheapest points you will ever score.

## Doing beats arguing

The strongest answer is a table, not a paragraph. When a reviewer doubts something, run the experiment and report the number — the argument you would have written becomes unnecessary.

Reach for prose only where no experiment exists (a definition, a framing, a scope). Prose is what's left after doing, not an alternative to it.

## Not doing it is the exception

Default to running what they ask. An agent's instinct is to triage and defend the schedule — that instinct is what gets papers rejected on the second round, because a reviewer who asked twice is a reviewer who is done.

Before writing "we could not," walk the ladder:

1. **Enumerate every route.** For data: official link, mirrors, third-party hosts, the authors, competition organizers, colleagues who have it. For a method with no implementation: a non-differentiable version for inference-only comparison, a reduced-scope variant, a published number from another paper, a qualitative comparison.
2. **Actually try each one.** A 404 on the first link is one datum, not a conclusion.
3. **Downgrade before dropping.** Reviewers accept less than they asked for far more often than they accept nothing. A comparison on 3 of 5 datasets, a shorter training schedule, an inference-only variant, one seed instead of three — all of these are *doing it*.
4. **If everything fails, the response says what you tried.** "We were unable to obtain X; the official link (URL, accessed DATE) returns 404, the mirror requires competition registration which closed on DATE, and we contacted the authors on DATE without response" is a fact the reviewer can verify. "This dataset is unavailable" is an opinion they can reject.

An honest "we tried these five things and here is what happened" reads as diligence. A tidy dismissal reads as laziness, whatever its logic.

## The spec bounds the work in both directions

Work they did not ask for is not diligence — it is a new attack surface, paid for with the hours the asked-for work needed.

An unasked experiment hands the reviewer a question they had not thought to ask, and its result is outside your control. "Our core mechanism turns out to contribute less than claimed" is a sentence you can only discover *after* you have put it in front of them. A gap nobody raised is not a gap you have to fill this round.

So when an analysis surfaces a weakness the reviewers missed, that finding is intelligence for the *next* paper, not work for *this* revision. Note it, keep it, move on.

The exception is narrow: an unasked experiment earns its place only when it is the *cheapest* way to answer something they **did** ask. Test it by naming the comment number it serves. No number, no run.

## Concede early and openly

Name the components you adopted, cite them, and state plainly what is yours: *"Built on the adopted X [cite]; unlike prior work, we …"*

This is counterintuitive and it works. Conceding an adopted component is what moved HGD-Net from major to minor revision. The reviewer is already suspicious; a concession you volunteer costs one sentence, while the same fact discovered by the reviewer costs your credibility on everything else.

The corollary: **keep adopted components out of the contribution list.** A contribution that leads with someone else's idea invites exactly the "these two works look similar" comment.

## Wrong premises

Reviewers make factual errors. Handle it in this order — the order is the whole technique:

1. **Concede the literal claim** if it is literally true. Do not spend a word defending it.
2. **Locate the premise** behind the claim, which is usually where the error lives ("I guess the authors want X" is a premise wearing a disguise).
3. **Correct it with evidence, briefly** — ideally from a source the reviewer already trusts (the original paper of the method they are citing at you, their own cited work's tables).
4. **Then do what they asked anyway.** The correction earns nothing on its own; the experiment does. Running the comparison they wanted is what converts "the author argued with me" into "the author addressed it."

A correction without an experiment reads as a dodge, no matter how right it is.

## The response letter

Per comment, in this order: quote the comment verbatim → state the action taken → show the evidence → point to the location in the revised manuscript ("Sec. 4.3, Table 5, p. 8").

**Only report work that exists.** Every claim in the letter must be checkable in the attached manuscript. Promising a future experiment invites the reviewer to hold you to it on the next round, and there may not be one — if it isn't done by the deadline, it doesn't go in the letter.

Tone is a solved problem: plain, factual, no hedging, no gratitude inflation, no defensive framing. The letter's job is to be verifiable, not to be liked.

## Consistency is a second reviewer

A reviewer who catches one inconsistency starts auditing everything. Before submitting, check that the same number means the same thing everywhere: one metric protocol per column (raw and corrected scores are different columns, never the same one), one value per baseline across all tables and drafts, one name per method, one key per citation.

Baselines deserve a specific pass. A baseline you reproduced below its published number is read as suppression, whatever the cause. Either reproduce it with official weights, or state the protocol difference in the caption — before a reviewer states it for you.

## Working order

Verify → run → write. Land the numbers first; the letter is what you write once there is something to report.

When the schedule is tight, cut scope within each comment (fewer seeds, shorter schedule, fewer datasets) rather than dropping comments. An addressed comment at reduced scope scores; an unaddressed comment does not.

## The page

The revision lives on one page, not in chat. Build it the moment the decision letter arrives, in
whatever form it came — a PDF, a `.docx`, screenshots of the submission system, or text pasted
into the conversation. It starts as a translation of the reviewers' words and grows, comment by
comment, into the draft of the response letter.

Re-render it whenever the user asks where things stand, whenever results land and change a
status, and before any scope decision. They need the whole board, not the slice you happen to be
holding.

Three properties carry the work. **Verbatim originals beside the translation**, because
paraphrase is how scope quietly drifts. **An evidence slot that stays visibly empty** until a real
number fills it — intentions do not count, which is the rule the letter runs on too. And **the
force of the reviewer's wording marked in the English**, because translation flattens it: "provide
**concrete** evidence" is a reviewer who has already judged your evidence thin, and the Chinese
for it reads like a neutral request.

Offer two or three routes per open comment rather than one instruction, and let the page record
which one the author picks. They know which GPU is free and how much of the deadline is real.

See [references/html-report.md](references/html-report.md) for the format.

## The response letter

The page feeds a LaTeX letter; [`assets/response-letter/`](assets/response-letter/) holds the
template. Generate the skeleton once the ids and the verbatim text are settled — those blocks are
quotations, so they carry no risk — then fill each response in as it becomes true.

Emit the comment blocks in the letter's own order. The template numbers them by counter, so the
sequence in the file becomes the numbering the reviewer reads, and a list sorted by status
renumbers the response.
