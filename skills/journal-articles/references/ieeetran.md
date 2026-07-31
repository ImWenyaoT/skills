# IEEEtran Authoring Reference

## Contents

- Frontmatter
- Class options and columns
- Affiliation and `\thanks` wording
- Migrating from another publisher's class
- Fitting a page limit without touching content
- Submission-system renditions differ from your PDF
- Compile expectations
- BibTeX and citations
- Structure idioms
- Images
- Common local failures

## Frontmatter

Journal mode has no `frontmatter` environment. Keep this order before `\maketitle`:
`\title`, one `\author` block with `\IEEEmembership` grades and `\thanks` notes
(affiliations, e-mail, manuscript dates), then `\markboth{<journal banner>}{<running
head>}`. After `\maketitle` come `abstract`, `IEEEkeywords`, then
`\IEEEpeerreviewmaketitle`. Open the first section with `\IEEEPARstart{X}{yz}`. End
matter order: `\appendices`, `\section*{Acknowledgment}`, bibliography, then
`IEEEbiography` entries. A trailing `%` after each `\thanks` and author line prevents
spurious spaces.

## Class options and columns

| Options | Use |
|---|---|
| `journal` | Default two-column transactions/journal layout; the normal submission mode. |
| `journal,draftclsnofoot,onecolumn` | Single-column, double-spaced draft for reading or markup; page counts do not reflect the published density. |
| `conference` | IEEE conference layout; different frontmatter idioms (`\IEEEauthorblockN/A`). |
| `technote` | Correspondence/technote layout, 9pt. |
| `peerreview`, `peerreviewca` | Anonymized title-page variants for journals that require them. |
| `comsoc`, `compsoc`, `transmag` | Society-specific variants; only when the target journal is published under that society's format. |

Signal Processing Society transactions (including TIP and TMM) use plain `journal` mode.
The current IEEE Template Selector transactions skeleton (`bare_jrnl_new_sample4.tex`)
opens with `\documentclass[lettersize,journal]{IEEEtran}` — but `lettersize` is not a
real IEEEtran v1.8b option (the 2021 sample targets a class revision that never shipped)
and triggers `LaTeX Warning: Unused global option(s): [lettersize]`. Write
`[letterpaper,journal]` (or bare `[journal]`; letterpaper is the default) so the log
stays warning-clean for submission validators. The official zip ships the class,
skeleton, and how-to but no `.bst` or `.bib` — the bibliography style comes from the TeX
distribution. Page limits are counted against the
two-column `journal` layout, so verify length in that mode even if drafting in
`onecolumn`. Change only class options to switch views; do not fork the manuscript into
per-layout sources that can drift.

## Affiliation and `\thanks` wording

In "with the Department of X, Y University", the article belongs to *Department*, not
the university. Universities whose names start with a place or person name take no
article ("with Zhejiang University of Science and Technology", "with Stanford
University"); the "University of X" pattern takes "the" ("with the University of
Michigan"). A few institutions brand an official "The" (e.g., The Hong Kong University
of Science and Technology) — follow the institution's official English name, not habit.

## Migrating from another publisher's class

Converting an `elsarticle` (or similar) source to IEEEtran, beyond swapping the class:

- Frontmatter: `frontmatter`/`\corref`/`\ead`/`\affiliation` become one `\author` block
  with `\thanks` notes; move funding acknowledgements into a `\thanks` too (IEEE puts
  funding on page 1, not in a back-matter section).
- Keywords: `\sep` separators become plain commas inside `IEEEkeywords`.
- Drop publisher-specific back matter (CRediT, competing-interest, data-availability
  sections) unless the IEEE journal's author information asks for an equivalent.
- Add `\IEEEPARstart{X}{yz}` to the first paragraph; add `\markboth` with the journal
  banner and running head.
- Drop `fleqn`/`lineno`-style layout options and any house font switches for tables or
  captions (`\sffamily` wrappers); IEEE tables and captions use the text font.
- SPS journals require a 150–250-word abstract with no abbreviations, footnotes,
  displayed equations, or references — spell out coined acronyms at first use and audit
  leftover bare metric acronyms.
- Verify content parity mechanically after the port: diff the sets of section titles,
  `\label`s, `\cite` keys, `\includegraphics` targets, and equation/table counts between
  old and new sources.

## Fitting a page limit without touching content

Order of attack when the compiled paper must lose pages but the text must not change:

1. Read the log first. `Requested size` lines versus each figure's natural size expose
   figures scaled *beyond* their native dimensions — shrinking those back is free.
   `LaTeX Warning: Text page N contains only floats` plus `Overfull \vbox ... while
   \output is active` means a float stack is taller than the page: shrink members of
   that stack.
2. Nudge figure widths a few percent at a time and recompile; diagram-style figures
   with embedded text have a legibility floor (~0.85 of their designed width) — render
   the page at ~110 dpi and actually look before going lower.
3. Unify table font tiers (`\small` → `\footnotesize` where siblings already use it)
   and tighten `\abovecaptionskip` a point or two; with many floats this recovers
   surprising amounts.
4. When the last page holds only a few reference lines, any ~10 pt saved upstream pulls
   one line back — global caption/float-sep knobs beat further figure shrinking.

Verify each round with `pdfinfo` (page count), a zero grep for `Overfull` and
`contains only floats`, and page renders (`pdftoppm -png -r 50`) to catch new layout
pathologies. `pdffonts` must show every font embedded; for rasters, effective dpi =
pixel width / displayed inches — check it against the 300/600 dpi floors before
concluding a figure must be re-rendered.

## Submission-system renditions differ from your PDF

Publisher portals (IEEE Author Portal/Atypon, Editorial Manager) convert uploaded LaTeX
through an XML pipeline whose preview typically renders single-column with all floats
collected after the references and `\thanks` turned into endnotes. Float specifiers
cannot influence that converter, and distorting the source to chase it (forced
`\clearpage`, `[h]` everywhere) damages the real layout. Prove the source innocent by
compiling locally in `journal`, `onecolumn`, and `draftcls` modes — if floats sit
before the references in all three, the drift is the converter's, and the uploaded PDF
(which reviewers read) is what counts.

## Compile expectations

Preferred command:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Manual sequence for a BibTeX paper:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

`IEEEtran` (class and `.bst`) is distributed by TeX Live and MiKTeX. Confirm discovery
with `kpsewhich IEEEtran.cls` and `kpsewhich IEEEtran.bst`. Runtime installation and
general LaTeX doctor work are outside this skill.

## BibTeX and citations

Use `\bibliographystyle{IEEEtran}` with plain `\cite`; add the `cite` package so runs of
citations compress to `[1]–[4]`. Do not load `natbib` or `biblatex` — IEEEtran's own
style is required and `natbib` author-year commands have no meaning in IEEE numeric
style. `IEEEabrv.bib` (bundled string definitions) yields IEEE-standard abbreviated
journal names: `\bibliography{IEEEabrv,references}`. A question-mark citation means
BibTeX did not run, the key is absent, or the `.bst` is unavailable; read the first
relevant `.blg`/`.log` error rather than re-running LaTeX.

## Structure idioms

- Displayed equations: prefer `IEEEeqnarray` (from bundled `IEEEtrantools`) over
  `eqnarray`; `amsmath` environments also work and are common.
- Appendices use `\appendices` + `\section`; a single appendix uses `\appendix`.
- Author photos/bios: `\begin{IEEEbiography}[{\includegraphics[...]{photo}}]{Name}`;
  use `\begin{IEEEbiographynophoto}{Name}` before photos exist. Bios count toward page
  limits at many IEEE journals — keep them in the length budget.
- Table captions sit above tables in IEEE style (`\caption` before the tabular); figure
  captions sit below.

## Images

With `pdflatex`, prefer PDF for vector art and PNG or JPEG for raster images; EPS needs
conversion before a direct PDF build. IEEE production accepts EPS/PS/PDF/PNG/TIFF
(high-resolution JPEG only for author photos) and expects >300 dpi for color/grayscale
raster figures and >600 dpi for line art at final size — column widths are 3.5 in
(single) and 7.16 in (double). Keep image paths relative and inspect the compiled PDF at
normal reading size; two-column layout makes single-column figures narrow, so use
`figure*` only for genuinely full-width content. The official transactions skeleton loads
`subfig` as `\usepackage[caption=false,font=normalsize,labelfont=sf,textfont=sf]{subfig}`;
omitting those options changes subfigure caption behavior relative to the official
template.

## Common local failures

- `IEEEtran.cls not found`: install the distribution's `IEEEtran` package, refresh the
  filename database, and rerun `kpsewhich IEEEtran.cls`.
- `IEEEtran.bst not found`: install or repair the same package; do not silently swap
  bibliography style.
- `Citation ... undefined`: verify the key, run BibTeX, then run LaTeX twice.
- Undefined `\citep`/`\citet`: the source still carries natbib idioms from another
  publisher's template; convert to plain `\cite`.
- Overfull warnings around authors: missing `%` line-enders inside the `\author` block.
- `\IEEEpubid` overlaps text: it is for accepted-version footers; remove it from
  submission drafts.

## Primary references

- Official demo skeletons (`bare_jrnl.tex` etc.) ship with the package:
  `texmf-dist/doc/latex/ieeetran/` in TeX Live.
- CTAN package and current manual: https://ctan.org/pkg/ieeetran
- IEEE Author Center LaTeX resources: https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/authoring-tools-and-templates/
- IEEE Template Selector: https://template-selector.ieee.org/
