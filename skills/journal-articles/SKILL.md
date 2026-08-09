---
name: journal-articles
description: Triggers on 期刊模板, 双栏 layout, 页数超限, and local `elsarticle` or `IEEEtran` manuscript sources — template scaffolding, frontmatter and author metadata (`\ead`/`\corref` or `\thanks`/`\markboth`), class options (`preprint`, `review`, `3p`, `journal`, `conference`, `onecolumn`), bibliography style (`natbib`, `IEEEtran.bst`), figure formats, and `pdflatex`/`latexmk`/BibTeX compile diagnosis. Does not apply to assembling upload files for a submission screen or writing and reviewing the paper's prose.
license: MIT
compatibility: Requires a LaTeX runtime (latexmk or pdflatex) with the elsarticle or IEEEtran class available.
---

# Authoring Journal Articles

## Boundary

Own the publisher-specific manuscript source: document class structure, class options,
frontmatter, bibliography conventions, figures, and a reproducible local compile. Do not
write the paper's argument or package a finished manuscript for a submission system. Generic
TeX distribution installation and repair remain the responsibility of the user's LaTeX
runtime; this skill only diagnoses the commands and packages its bundled templates need.

## Establish the publisher first

The two supported vocabularies do not overlap. `elsarticle` uses a `frontmatter`
environment with `\ead` and `\corref`; `IEEEtran` journal mode has no `frontmatter` and uses
`\thanks`, `\markboth`, and `\IEEEPARstart`. Mixing them produces a source that compiles
under neither class, so settle the publisher before touching the manuscript, then:

- read exactly one reference — [references/elsarticle.md](references/elsarticle.md) **or**
  [references/ieeetran.md](references/ieeetran.md);
- copy exactly one asset directory — `assets/elsarticle/` **or** `assets/ieeetran/`.

If the target journal is unknown, ask. A guessed publisher costs a full rewrite of the
title block, keywords, back matter, and bibliography setup.

## Start or maintain a manuscript

1. Read the one publisher reference before choosing class options or changing frontmatter,
   bibliography, or image formats.
2. When the user supplies a Guide for Authors, Information for Authors page, or URL, read
   [references/journal-profile.md](references/journal-profile.md) and extract the current
   journal profile before changing the manuscript. Keep journal-specific limits in the paper
   workspace rather than treating them as publisher-wide defaults.
3. Copy the one asset directory into the paper workspace. Keep `main.tex` and
   `references.bib` together until the project has a reason to introduce directories.
4. Choose one deliberate class configuration:
   - `elsarticle`: default to `preprint` for a readable submission draft, `review` for
     increased line spacing, and `1p`/`3p`/`5p` only when the journal asks for that model.
   - `IEEEtran`: default to `journal` (two-column) because IEEE transactions count page
     limits against that layout. Add `draftclsnofoot,onecolumn` only as a reading draft,
     never as the length yardstick; use society variants (`comsoc`, `compsoc`, `transmag`)
     only when the target journal requires them.
5. Replace every placeholder in the title block. For `elsarticle`, preserve `frontmatter`
   ordering and keep author-affiliation keys stable. For `IEEEtran`, keep `\thanks` notes
   inside the `\author` block, keep the trailing `%` line-enders, and update both
   `\markboth` arguments.
6. Run the bundled smoke before building on the template:

```bash
python scripts/smoke_template.py --publisher elsevier   # or: --publisher ieee
```

The smoke compiles the bundled fixture in a temporary directory when a LaTeX runtime is
available. Without one, it exits `2` naming the missing binary or package and never reports
a false pass.

## Compile the working paper

Prefer a build tool that reruns BibTeX and LaTeX as needed:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

For manual diagnosis, use `pdflatex main.tex`, `bibtex main`, then `pdflatex main.tex`
twice. Treat missing citations, undefined references, substituted fonts, or a nonzero exit
as failures. Delete generated files with `latexmk -C`, not manuscript sources.

## Done

- One publisher's vocabulary is used throughout; no macro from the other class survives.
- The selected class options match the target journal's current author guide.
- The journal profile records every applicable limit and separates verified journal
  requirements from reusable publisher conventions.
- All title-block placeholders are replaced and affiliations, `\thanks`, and running heads
  resolve with no overfull warnings from the title block.
- The local build exits zero with no undefined references or citations.
- The PDF uses the layout the journal judges length against, and every figure is legible at
  print size.
- Source changes remain canonical; generated PDFs and auxiliaries are build products.
