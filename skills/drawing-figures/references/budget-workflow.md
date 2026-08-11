# Budget Workflow

Run Phase A once per representative reference corpus. Keep outputs beside the paper's planning
artifacts so the eventual figure plan is traceable to its source corpus.

## Running these scripts in your environment

The commands below use `uv run --with …`, which fetches the dependency per run and
needs nothing installed. That is the zero-setup path, and it is what the examples
show.

**If you already have an environment with these packages — conda, a virtualenv,
anything — run the script with your own Python instead:** `python scripts/<name>.py …`.
Prefer that when the script has to see your data, your checkpoints, or anything else
your environment resolves, because `uv run --with` builds a *separate* ephemeral
environment: it will not see what your conda env sees.

Whichever way you run it, a missing package stops the script with exit code 2 and a
message naming the package and the uv, pip, and conda commands that install it. Exit 2
means the work is blocked, never that a check failed.

## 1. Section word counts

```bash
uv run scripts/section_wordcount.py \
  --corpus <dir-of-pdfs> --out <output-dir> \
  [--exclude <regex>] [--prefix <string>]
```

Requires Poppler's `pdftotext`. The output reports median and IQR per recognized section.

## 2. Figure and table counts

```bash
uv run scripts/reference_fig_table_stats.py \
  --corpus <dir-of-pdfs> --text-root <dir-of-txt> --out <output.csv>
```

The CSV surveys figures and tables in each paper's experiments section. Use its distribution to
set a figure budget rather than copying a single reference paper.

## 3. Palette extraction

```bash
uv run --with numpy --with pillow scripts/extract_colorpick_palette.py \
  --src <dir-of-pngs-or-pdfs> --out <palette.md> \
  [--n-colors 32] [--merge-dist 22]
```

The Markdown output records dominant hex/RGB swatches. Treat extracted colours as evidence about
venue conventions, then choose an accessible palette with redundant encodings.

## 4. Caption audit

```bash
uv run scripts/extract_pdf_fig_tables.py \
  --pdf-dir <dir-of-pdfs> --out <captions.md>
```

Read the extracted captions for recurring figure/table types and caption phrasing, then record the
patterns your own corpus shows. Extraction is an audit aid, not a citable substitute for checking
the source PDFs.

## Budget evidence

Record the corpus path and date, commands used, and paths for all four outputs. If a required input
or executable is missing, record that fact explicitly rather than silently presenting a partial
budget as complete.
