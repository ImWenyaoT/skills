# Attribution

## Upstream

This template descends from **"Ultimate LaTeX Response Letter Template | 论文投稿回复信终极模板"**
by **Hai-Jun-Yan** (<https://github.com/Hai-Jun-Yan>), released under the **MIT licence**.

What the upstream project contributed, as documented in its README:

- the overall idea of a `tcolorbox`-driven response letter with distinct box colours for
  editor/reviewer comments, author responses, and revision text;
- automatic comment numbering and per-reviewer section reset, including the
  `\startReviewerSection{...}` command name, which is carried over unchanged;
- automatic table-of-contents generation;
- a pdfLaTeX-only design (no `fontspec`), so it compiles on TexPage/Overleaf and on
  Editorial Manager's default engine.

Upstream's README asks — as a request, not as a licence condition — that users star the
repository and consider citing the author's paper (Yan et al., *Enhancing feature interaction
for improved generalization in few-shot metal surface defect segmentation*, Knowledge-Based
Systems 330:114606, 2025).

Note: the upstream README states "License: MIT" but the copy this template was derived from
did not ship a `LICENSE` file, so the verbatim MIT text below is the standard one, reproduced
to satisfy the licence's notice requirement. The upstream copyright holder is Hai-Jun-Yan.

## What was changed downstream

The downstream rework (by the owner of this skill, for an Elsevier journal
major revision) is substantial enough that little upstream code survives verbatim:

- **Interface changed from macros to environments.** Upstream exposes single-argument macros
  (`\myEditorComment{...}`, `\myReviewerComment{...}`, `\myReviewerResponse{...}`,
  `\myReviewerRevision{...}`). This template replaces them with LaTeX environments
  (`editorcomment`, `editorresponse`, `reviewercomment`, `reviewerresponse`, `changes`) so
  that multi-paragraph responses containing display math, lists, and nested boxes can be
  written directly instead of being stuffed into a macro argument.
- **Pantone-derived three-family palette.** The default `xcolor` names
  (`gray!60!black`, `cyan!70!black`, `green!45!black`) were replaced with coated-guide hex
  equivalents in gray / blue / green families, each with a matching lighter title fill.
  Upstream's red "diff" box is gone; the green `changes` box quotes revised manuscript text
  instead of showing an original-vs-revised diff.
- **Title bar moved INSIDE the box frame.** Upstream (and this template's own earlier
  revisions) attached the boxed title above the frame; the floating title was not reserved in
  the surrounding paragraph flow, so on dense pages a box title clipped into the previous
  box's bottom frame. The `letterboxbase` style now puts the title inside the frame, which
  makes the collision structurally impossible. The comment explaining this is in `main.tex`.
- **TOC integration.** Every comment and response registers itself with
  `\addcontentsline` at `subsection`/`subsubsection` level, and `hyperref`'s `linktoc=all`
  plus a re-pointed `linkcolor` paints the whole table of contents in the editorial blue.
- **Bibliography removed.** Upstream ships `biblatex` with a per-reviewer reference list.
  This template loads no bibliography package: references in a response letter are given
  inline in author-year plain text so they can be cross-checked against the manuscript's own
  bibliography without an extra bib pass.
- **Elsevier letter framing added.** `authblk` author/affiliation block, `fancyhdr` two-sided
  headers, a "Manuscript Information" panel, the six `\my...` metadata commands, the opening
  letter, and the "Summary of Revisions Made" section with its `Addresses <comment ids>`
  convention are all downstream additions.
- **`letterboxbase` shared style, geometry, and typography settings** (A4 two-sided, Helvetica
  substitute, `emergencystretch`/`tolerance` tuning for dense math bullets) are downstream.

## MIT Licence

```
MIT License

Copyright (c) Hai-Jun-Yan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
