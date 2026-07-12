# elsarticle Authoring Reference

## Frontmatter

Keep this order inside `frontmatter`: title, authors and affiliations, corresponding-author
email, abstract, then keywords. Use stable affiliation keys such as `inst1`. Put manuscript
sections after `\end{frontmatter}`. Check the target journal for double-anonymous review;
when required, maintain an anonymous build without author-identifying metadata.

## Class options and columns

| Options | Use |
|---|---|
| `preprint` | Default submission-oriented, single-column draft. |
| `review` | Preprint-like layout with increased baseline spacing for review. |
| `1p` | Model 1+ appearance; single column. |
| `3p` | Model 3+ appearance; single column unless combined with `twocolumn`. |
| `5p` | Model 5+ appearance; normally two column. |

Do not infer a production model from another journal. Read the live Guide for Authors.
For writing and review, a single-column `preprint` or `review` source is usually easier to
inspect. If a double-column preview is required, change only the class options; avoid
forking manuscript content into two sources that can drift.

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

`elsarticle` is distributed by TeX Live and MiKTeX. Confirm discovery with
`kpsewhich elsarticle.cls` and `kpsewhich elsarticle-num.bst`. Runtime installation,
package-manager repair, and general LaTeX doctor work are outside this skill.

## BibTeX and natbib

`elsarticle` uses `natbib`; do not add `biblatex` unless the target journal explicitly
supports it. Common styles are `elsarticle-num`, `elsarticle-num-names`, and
`elsarticle-harv`. Match the journal guide. A question mark citation usually means BibTeX
did not run, the key is absent, or the `.bst` is unavailable. Read the first relevant error
in `.blg` and `.log`; repeated LaTeX runs cannot repair a missing key.

## Images

With `pdflatex`, prefer PDF for vector art and PNG or JPEG for raster images. EPS normally
needs conversion before a direct PDF build. Keep image paths relative, preserve extensions
when the submission system expects them, and inspect the final PDF at normal reading size.

## Common local failures

- `elsarticle.cls not found`: install the distribution's `elsarticle` package, refresh its
  filename database if required, and rerun `kpsewhich elsarticle.cls`.
- `elsarticle-num.bst not found`: install or repair the same package; do not silently swap
  bibliography style.
- `Citation ... undefined`: verify the key, run BibTeX, then run LaTeX twice.
- `File ... not found` for a figure: verify case-sensitive relative paths and compatible
  formats.
- Review line numbers collide with frontmatter: put `\linenumbers` after frontmatter unless
  the current official template says otherwise.
- A double-column figure is unreadable: use `figure*` only for genuinely full-width content
  and simplify labels instead of shrinking text.

## Primary references

- Elsevier LaTeX instructions: https://www.elsevier.com/researcher/author/policies-and-guidelines/latex-instructions
- CTAN package and current manual: https://ctan.org/pkg/elsarticle
- CTAN package files and templates: https://tug.ctan.org/macros/latex/contrib/elsarticle/
