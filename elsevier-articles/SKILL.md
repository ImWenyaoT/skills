---
name: elsevier-articles
description: Triggers when a local Elsevier `elsarticle` source needs template scaffolding, frontmatter, author affiliations, corresponding-author metadata, single-column or double-column class options (`preprint`, `review`, `1p`, `3p`, `5p`), line numbering, image formats, compile smoke, `pdflatex`, `latexmk`, `natbib`, or BibTeX diagnosis. Does not apply to Editorial Manager submission packaging or unrelated document formatting.
---

# Authoring Elsevier Articles

## Boundary

Own the Elsevier-specific manuscript source: `elsarticle` structure, class options,
frontmatter, bibliography conventions, figures, and a reproducible local compile. Do not
write the paper's argument or package a finished manuscript for Editorial Manager. Generic
TeX distribution installation and repair remain the responsibility of the user's LaTeX
runtime; this skill only diagnoses the commands and packages its bundled template needs.

## Start or maintain a manuscript

1. Read [references/elsarticle-authoring.md](references/elsarticle-authoring.md) before
   choosing class options or changing frontmatter, bibliography, or image formats.
2. Copy `assets/minimal-article/` into the paper workspace. Keep `main.tex` and
   `references.bib` together until the project has a reason to introduce directories.
3. Choose one deliberate class configuration. Default to `preprint` for a readable
   submission draft; use `review` for increased line spacing; use `1p`, `3p`, or `5p`
   only when the target journal asks for that model. Add `twocolumn` only where the model
   supports it and the journal requests it.
4. Replace every placeholder in the frontmatter. Preserve `frontmatter` ordering and keep
   author-affiliation keys stable while editing.
5. Run the bundled smoke before building on the template:

```bash
python scripts/smoke_template.py
```

The smoke compiles the bundled fixture in a temporary directory when a LaTeX runtime is
available. Without one, it exits with a doctor-style installation next step and never
reports a false pass.

## Compile the working paper

Prefer a build tool that reruns BibTeX and LaTeX as needed:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

For manual diagnosis, use `pdflatex main.tex`, `bibtex main`, then `pdflatex main.tex`
twice. Treat missing citations, undefined references, substituted fonts, or a nonzero exit
as failures. Delete generated files with `latexmk -C`, not manuscript sources.

## Done

- The selected class options match the target journal's current author guide.
- All frontmatter placeholders are replaced and affiliations resolve correctly.
- The local build exits zero with no undefined references or citations.
- The PDF uses the intended column strategy and every figure is legible.
- Source changes remain canonical; generated PDFs and auxiliaries are build products.
