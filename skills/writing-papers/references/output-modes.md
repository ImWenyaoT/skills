# Output modes

What the deliverable looks like, once the review or polish work is done. Mode 1 is the default when
the user names no mode.

Modes 2, 3, and 5 emit a Chinese back-translation beside the English LaTeX. That is deliberate: a
literal translation is how the author checks that polishing preserved the technical meaning, and it
is the only place in this skill where the output is bilingual.

## Contents

- [Mode 1: full review](#mode-1-full-review)
- [Mode 2: LaTeX polish](#mode-2-latex-polish)
- [Mode 3: strip AI tone](#mode-3-strip-ai-tone)
- [Mode 4: final-pass redline](#mode-4-final-pass-redline)
- [Mode 5: experiment analysis](#mode-5-experiment-analysis)
- [Mode 6: figure and table captions](#mode-6-figure-and-table-captions)

## Mode 1: full review

- **A. Overall judgement** — one paragraph on the single largest problem. Only what affects
  acceptance, comprehension, or persuasiveness; no generic appraisal.
- **B. Problem list** — ordered by severity. Each entry carries the problem type, the location in
  the source, why it is a problem, and the smallest repair that fixes it.
- **C. Language and AI tone** — repeated phrasings, mechanical connectives, over-explanation,
  abuse of bold and parentheses, an abbreviation defined twice. Give drop-in replacement sentences
  where they help.
- **D. Logical self-consistency** — contradictions, concept jumps, unclear causality, thin
  evidence, conclusions past their evidence. Do not attack novelty.
- **E. Figure-text linkage** — what stays in the prose and what the figures and captions should
  carry.
- **F. Drop-in replacements** — for the paragraphs with obvious problems, give a replacement
  version. Prefer the smallest necessary edit over a rewrite.
- **G. Length and risk notes** — anything that may affect word count, logic, figure references,
  terminology consistency, or the LaTeX build.

## Mode 2: LaTeX polish

- **Part 1 [LaTeX]** — the polished English LaTeX only. Preserve equations, citations, labels, and
  the commands that matter; handle `%`, `_`, and `&` correctly; add no unrelated formatting.
- **Part 2 [Translation]** — a literal Chinese translation for meaning-checking, without
  parenthesised English scattered through it.
- **Part 3 [Modification log]** — a short account of the main edits: grammar, compression, AI tone,
  duplicate abbreviations, logical connectives strengthened.

## Mode 3: strip AI tone

- **Part 1 [LaTeX]** — the rewritten English LaTeX. If the source already reads naturally, emit it
  unchanged.
- **Part 2 [Translation]** — a literal Chinese translation.
- **Part 3 [Modification log]** — which mechanical constructions were removed. When nothing needed
  changing, emit `[PASS — no substantive issues]` and say the source already reads naturally.

## Mode 4: final-pass redline

With nothing that must change, emit `[PASS — no substantive issues]`. Otherwise list the findings
briefly, restricted to fatal logic problems, terminology inconsistency, and serious grammar
errors.

## Mode 5: experiment analysis

- **Part 1 [LaTeX]** — an English LaTeX paragraph opening with `\paragraph{Key finding}` followed
  by the analysis. No lists, no `\textbf{}` or `\emph{}`.
- **Part 2 [Translation]** — a literal Chinese translation.
- **Part 3 [Data check]** — exactly which data each conclusion rests on. Say so plainly when the
  data is insufficient, the trend is weak, or the numbers cannot support a strong conclusion.

## Mode 6: figure and table captions

Emit the English caption with no `Figure 1:` or `Table 1:` prefix. A noun phrase takes title case
and no final period; a full sentence takes sentence case and a period. Avoid `The figure shows`,
`This diagram illustrates`, `showcase`, and `depict` — padding, and the AI register.
