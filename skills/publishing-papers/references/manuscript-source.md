# The Manuscript Source

This phase owns the publisher-specific LaTeX source: document class structure, class options,
the title block, bibliography conventions, figures, and a reproducible local compile. It does
not write the paper's argument and it does not package a finished manuscript for a submission
screen.

Installing or repairing a TeX distribution is the user's runtime problem. What follows only
diagnoses the commands and packages the bundled templates actually need.

## Start from the bundled assets

Copy exactly one asset directory into the paper workspace — `assets/elsarticle/` **or**
`assets/ieeetran/`. Keep `main.tex` and `references.bib` side by side until the project has a
real reason to introduce directories; an early directory split mostly costs you path fixes.

Read the one publisher reference — [elsarticle.md](elsarticle.md) or
[ieeetran.md](ieeetran.md) — before choosing class options or touching the frontmatter,
bibliography, or image formats.

## Choose the class options deliberately

Pick one configuration and know why you picked it:

- `elsarticle`: `preprint` for a readable submission draft, `review` when you want increased
  line spacing for reviewers, and `1p`/`3p`/`5p` only when the journal asks for that model.
- `IEEEtran`: `journal` for two-column output, which is the default because it is what the
  journal actually sets. `draftclsnofoot,onecolumn` is a reading draft only. Society variants
  (`comsoc`, `compsoc`, `transmag`) go in only when the target journal requires them.

## Replace the title block placeholders

Every placeholder in the template has to go, and each class fails differently when one stays:

- `elsarticle`: preserve the ordering inside `frontmatter` and keep author-affiliation keys
  stable, because the keys are what bind `\author` entries to `\affiliation` entries — a
  renamed key silently detaches an author from their institution.
- `IEEEtran`: keep `\thanks` notes inside the `\author` block, keep the trailing `%`
  line-enders (a dropped `%` injects spurious space into the author line), and update both
  arguments of `\markboth` — the running heads differ on odd and even pages.

## Run the bundled smoke before building on the template

```bash
python scripts/smoke_template.py --publisher elsevier   # or: --publisher ieee
```

It compiles the bundled fixture in a temporary directory when a LaTeX runtime is available.
Without one it exits `2` and names the missing binary or package, rather than reporting a
false pass. Exit `2` is therefore a statement about your environment, not about the template:
install what it names, then run it again. Do not proceed to debug `main.tex` on the strength
of a `2`.

## Compile and diagnose

Prefer a build tool that reruns BibTeX and LaTeX as many times as the cross-references need:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

For manual diagnosis run `pdflatex main.tex`, then `bibtex main`, then `pdflatex main.tex`
twice. Missing citations, undefined references, substituted fonts, and a nonzero exit are all
failures, including the ones LaTeX is willing to continue past.

Clean with `latexmk -C`, which removes generated files only. The source is canonical; the PDF
and the auxiliaries are build products and should never be edited to fix something.

## Read a Guide for Authors into a journal profile

When the user supplies a Guide for Authors, an Information for Authors page, or a URL, read
[journal-profile.md](journal-profile.md) and extract the profile before changing the
manuscript — the profile is what tells you which class options and limits are even in play.

Keep those journal-specific limits in the paper workspace. Treating one journal's numbers as
publisher-wide defaults is how a limit from last year's target journal ends up silently
governing this one.

## Done for this phase

- The selected class options match the target journal's current author guide.
- The journal profile records every applicable limit and keeps verified journal requirements
  separate from reusable publisher conventions.
- All title-block placeholders are replaced; affiliations, `\thanks`, and running heads
  resolve with no overfull warnings from the title block.
- Every figure is legible at print size in the compiled PDF.
- Source changes are the only changes; generated PDFs and auxiliaries carry nothing unique.
