# Drafting framework (a technical paper from nothing)

## Source and attribution

The skeleton comes from **Jennifer Widom, "Tips for Writing Technical Papers"** (Stanford InfoLab,
January 2006; lightly revised for the 2009 retelling, unchanged in 2012) — original:
<https://cs.stanford.edu/people/widom/paper-writing.html>. This file restates that methodology and
adapts it to the conventions used here (CVPR/ICCV/NeurIPS/ICLR/ICML/ACL style, LaTeX, no AI tone,
claims bound to evidence); its key lines are quoted short and marked. The original is not
reproduced in full — keep this attribution when you use the method.

## Contents

- [Drafting principles](#drafting-principles)
- [1. Title](#1-title)
- [2. Abstract](#2-abstract)
- [3. Introduction (five paragraphs)](#3-introduction-five-paragraphs)
- [4. Related work](#4-related-work)
- [5. Body](#5-body)
- [6. Experiments](#6-experiments)
- [7. Conclusions](#7-conclusions)
- [8. Future work](#8-future-work)
- [9. Acknowledgements, citations, appendices](#9-acknowledgements-citations-appendices)
- [10. Grammar and small-scale writing](#10-grammar-and-small-scale-writing)
- [11. Mechanics](#11-mechanics)
- [12. Versions and distribution](#12-versions-and-distribution)
- [Drafting checklist](#drafting-checklist)

## Drafting principles

- **The goal is not a fancier paper but one that reads as acceptable**: natural language, coherent
  logic, figures carrying the information density, conclusions bound strictly to evidence.
- **The hard rule, shared with review: invent nothing.** No data, experiment, citation, conclusion,
  or method detail. Mark what is missing as `[AUTHOR INPUT]` rather than writing it for the author.
- **Strip AI tone in the first draft, not later**: no piles of `novel` / `state-of-the-art` /
  `it is worth noting`. A checkable statement such as `improves SR by 1.8%` replaces the empty
  self-praise.
- **Spell out a concept once as "full form (abbreviation)"**, then use the abbreviation. Treat
  terms and notation like program variables: define before use, and define exactly once.

## 1. Title

Three shapes; pick by the temperament of the venue.

- **Descriptive and long**: `Linear-Time External Multipass Sorting with Approximation Guarantees`.
- **Short**: `Approximate External Sort`.
- **Middle, with a handle** (give the method a memorable name): `Floosh: A Linear-Time Algorithm
  for Approximate External Sort`.

House rule: top venues favour "memorable method name + one line of positioning". A title that is a
pile of keywords is not a title.

## 2. Abstract

> From the original: state the problem, your approach and solution, and the paper's main
> contributions, with almost no background or motivation; factual but complete; **do not repeat the
> abstract verbatim in the body.**

House rule: the abstract may close on one quantitative headline result (`cuts sorting cost from
O(n log n) to O(n) with bounded unsortedness`), using only numbers the paper actually has.

## 3. Introduction (five paragraphs)

The introduction decides the paper. A reviewer has usually made up their mind by the end of it and
spends the rest of the paper looking for evidence to support that judgement; a casual reader uses
it to decide whether to read at all.

The Stanford InfoLab five-paragraph structure — absent a good reason, the introduction is five
paragraphs, each answering one question (quoted from the original):

1. **What is the problem?**
2. **Why is it interesting and important?**
3. **Why is it hard? (E.g., why do naive approaches fail?)**
4. **Why hasn't it been solved before? (Or, what's wrong with previous proposed solutions? How does
   mine differ?)**
5. **What are the key components of my approach and results? Also include any specific
   limitations.**

Then add a paragraph or subsection, **"Summary of Contributions"**: the main contributions as
bullets, each naming the section that delivers it. That bullet list doubles as the paper's outline,
which saves space and removes a redundant paragraph.

House rule: item 5 states the limitations honestly. Contribution bullets use `\item` and echo the
`\section` numbering of the body.

## 4. Related work

Whether it goes **early** or **late** depends on the paper.

- **Early** (a subsection at the end of the introduction, or section 2): when related work can be
  both short and sufficient, or when the paper must take a defensive stance against prior work from
  the first page.
- **Late** (before the conclusion, often "Discussion and Related Work"): when a sentence in the
  introduction or preliminaries covers it for now, or when a fair comparison needs the paper's own
  technical content first.

House rule: state factual differences from prior work; do not disparage it. Related work is not a
list of everything published.

## 5. Body

Two guidelines that apply to every paper (quoted from the original):

- **Guideline #1**: `A clear new important technical contribution should have been articulated by
  the time the reader finishes page 3` — that is, before the first quarter of the paper.
- **Guideline #2**: `Every section of the paper should tell a story.` The story is linear, each
  step pulls the reader to the next, and **nothing interrupts it** (interruptions go to the
  appendix). The common trap: telling the story of how you groped your way to the result. Tell the
  story of **the result**.

The body varies with content, but the usual components are:

- **Running example**: one example carried through the whole paper where possible, introduced at
  the end of the introduction or in section 2 or 3.
- **Preliminaries**: the notation and terminology that are **necessary but not yours**, which is
  what marks off "not a contribution of this paper". Keep it short — remember Guideline #1.
- **Content** (algorithm, system, new construction, analysis): narrate **top-down**, so the reader
  can see where it is going and still catch the point when skimming.

## 6. Experiments

Most venues expect experiments. Two traps: running a **hokey** experiment, and reporting only the
settings that flatter you. Settle two questions first:

- **What to measure**: raw running time, sensitivity to a key parameter, scalability along each
  dimension (data size, problem complexity, and so on).
- **What to show**: absolute performance (usable, acceptable), performance against a naive method,
  against prior work, or across your own variants.

House rule: a reported gain carries its baseline, a consistent setting, and error bars, confidence
intervals, or significance where they apply. Do not recite numbers like a ledger — say what each
difference means for the claim.

## 7. Conclusions

Usually one short paragraph, and **never a copy of the abstract or introduction**. Use the
quantitative results to say the original claim more concretely — a measured speedup redeeming the
promise the introduction made.

## 8. Future work

This is where the paper shows what it opens up; bullets suit it. Two points:

- State the follow-up you are already running (`We are currently extending the algorithm to…, and
  preliminary results are encouraging.`). This marks your territory.
- Someone taking a topic from your future work is a compliment, not a threat.

## 9. Acknowledgements, citations, appendices

- **Acknowledgements**: do not skip them, or you cause offence. Discussions, feedback on drafts,
  implementation help all belong. When in doubt, thank.
- **Citations**: complete and consistent. Do not paste inconsistent BibTeX off the web and call it
  done; check every entry in the final pass.
- **Appendices**: detailed proofs and algorithms only. Two rules: (1) the appendix holds nothing
  needed to understand the paper's contribution; (2) detail most readers will not care about goes
  there — which is what keeps an over-long paper in bounds.

## 10. Grammar and small-scale writing

Strunk & White, *The Elements of Style*, is worth reading. Common pet peeves:

- Every "variable" (term, notation) is defined before use and defined once. A restatement after a
  long gap is a kindness. Global definitions live in Preliminaries; the rest are defined nearby.
- **Avoid "etc."** unless the remaining items are entirely obvious. Fine: `phases 1, 3, 5, 7, etc.`
  Not fine: `factors such as volatility, scalability, etc.`
- **Avoid "for various reasons"** — give the reasons.
- Avoid `this` / `that` / `these` / `it` with no referent (Ullman's pet peeve). Requiring `this`
  to be followed by what it refers to forces the sentence to become clear.
- Italics mark a definition or a quotation, **not emphasis** (Gries's pet peeve). Emphasis should
  fall out of the context.
- `that` versus `which`: `that` is defining, `which` is not. `The algorithms that are easy to
  implement all run in linear time.` against `The algorithms, which are easy to implement, all run
  in linear time.`

## 11. Mechanics

- **Spell-check the final version.** There is no excuse.
- Drafts and technical reports: 11pt, generous line spacing, 1" margins, single column. Do not
  punish readers with the cramped two-column conference layout.
- Font size inside a figure roughly matches the body text.
- Tables, figures, plots, and algorithms go at the **top of a page or column**, unless they are
  small enough to sit in the text flow.
- Each of them appears on the same page as its first reference, or the next one, where LaTeX
  allows.
- **Print the paper once** before submitting or publishing. Paper often reads differently from a
  screen.

## 12. Versions and distribution

- The usual arrangement is a conference version, later formally published, plus a full technical
  report online. Make the full version the conference version plus appendices; keep only the full
  version public (outside the proceedings), keep it in sync with the final conference version, and
  overwrite every public older copy when you revise it.
- A finished paper can go online immediately, dated, cited as a technical report — no formal number
  needed. **Never** put a conference copyright notice on a paper that has only been submitted, and
  **never** cite your own paper as "submitted to conference X": a year later, when it appears at
  conference Y, the citation embarrasses only you.

## Drafting checklist

- Does the introduction answer, in five paragraphs, what the problem is, why it matters, why it is
  hard, why it is unsolved, and what your approach and limitations are — with contribution bullets
  that double as the outline?
- Is a clear new technical contribution articulated before page 3 (Guideline #1)?
- Does every section tell one linear, uninterrupted story (Guideline #2), and is that the story of
  the result rather than of the search?
- Do the abstract, introduction, and conclusion avoid copying each other, and does the conclusion
  redeem the claim with a quantitative result?
- Do the experiments say what is measured and what is shown, with baselines and consistent
  settings?
- Are citations complete and consistent, acknowledgements present, and the appendix free of
  anything necessary?
- Is the AI tone gone, are abbreviations handled, is every notation defined before use? **Has
  nothing been invented — no data, experiment, citation, or conclusion?**
