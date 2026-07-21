# Response-letter template (LaTeX, Elsevier)

A point-by-point response-to-reviewers letter. `article` class, pdfLaTeX only — that is
Editorial Manager's default engine, so what compiles here compiles on submission.

Comments, responses, and quoted manuscript text each get their own coloured `tcolorbox`
(gray / blue / green), every box registers itself in the table of contents, and comment
numbers are generated rather than typed.

## Layout

```
response-letter/
├── main.tex              preamble, palette, box environments, front matter, \input list
├── Reviewers/
│   ├── Editor.tex        response to the editor's meta-review
│   └── R1.tex            one file per reviewer
├── README.md
└── ATTRIBUTION.md        upstream template (Hai-Jun-Yan, MIT) and what changed downstream
```

`main.tex` defines everything and `\input`s the files under `Reviewers/`. To add a reviewer,
copy `R1.tex` to `R2.tex` and add an `\input{Reviewers/R2.tex}` line at the bottom of
`main.tex` — **the order of the `\input` lines is the order of the sections in the PDF.**

## Placeholder convention

Everything that belongs to one specific paper is written as `{{FIELD-NAME}}`: double curly
braces, ALL-CAPS, hyphen-separated (no underscores — a bare `_` is a syntax error in LaTeX
text mode). The braces are LaTeX grouping characters, so an unsubstituted template still
compiles and each placeholder prints its own name in the PDF.

List every placeholder still outstanding:

```sh
grep -ron '{{[A-Z0-9-]\+}}' .
```

The ones in `main.tex`:

| Placeholder | Goes into |
| --- | --- |
| `{{JOURNAL-NAME}}` | `\myJournal` — title block, header, Manuscript Information panel |
| `{{MANUSCRIPT-ID}}` | `\myManuscriptID` — e.g. `ABCD-D-26-01234` |
| `{{MANUSCRIPT-TITLE}}` | `\myManuscriptTitle` — full manuscript title |
| `{{EDITOR-NAME}}` | `\myEditorName` — handling editor, also the salutation |
| `{{REVISION-ROUND}}` | `\myRevisionRound` — e.g. `Major Revision 1` |
| `{{AUTHOR-NAME}}` | `\author` block and the sign-off |
| `{{AUTHOR-AFFILIATION}}` | `\affil` — e.g. `Corresponding author.` |
| `{{REVIEWER-LIST}}` | e.g. `Reviewers~\#2, \#3, and~\#4` |

`\myShortTitle` is left as `Response to reviewers` — it is the running header, not per-paper.

The body placeholders (`{{REVIEWER-COMMENT-VERBATIM}}`, `{{ACTION-TAKEN}}`,
`{{VERBATIM-REVISED-MANUSCRIPT-TEXT}}`, `{{CHANGE-HEADLINE}}`, `{{COMMENT-IDS}}`, …) mark
prose that has to be written, not substituted mechanically. Delete the example items you
do not need rather than leaving them empty.

## Numbering is by order of appearance

There are no explicit comment numbers anywhere. `reviewercomment` and `editorcomment` call
`\stepcounter` on entry, so the Nth `reviewercomment` in a file becomes "Reviewer \#1
Comment N", and `\startReviewerSection` resets the counter so each reviewer starts at 1.

Consequence: **reordering the environments renumbers the letter.** Ids you cite elsewhere
(`Addresses R2-Q1`, the summary list, the tracking board) will silently stop matching. Keep
the environments in the order the decision letter uses, and give every numbered comment its
own pair — including the trivial ones.

## Environments

| Environment | Colour | Use |
| --- | --- | --- |
| `editorcomment` | gray | the editor's meta-review, verbatim (auto-italic) |
| `editorresponse` | blue | your reply to it |
| `reviewercomment` | gray | one reviewer comment, verbatim (auto-italic) |
| `reviewerresponse` | blue | your reply — action, evidence, location |
| `changes` | green | exact wording now in the manuscript; goes *inside* a response |

`\startReviewerSection{Reviewer \#1}` starts a reviewer's section: page break, section
heading, counter reset.

## Compile

```sh
latexmk -pdf main.tex          # two passes, for the table of contents
latexmk -c                     # drop the aux files, keep main.pdf
```

Nothing outside a standard TeX Live install is required: `tcolorbox`, `authblk`, `helvet`,
`csquotes`, `enumitem`, `fancyhdr`, `hyperref`, `babel`.

Licence and provenance: see [ATTRIBUTION.md](ATTRIBUTION.md).
