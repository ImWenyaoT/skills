# Elsevier Packet Reference

## Contents

- Manifest keys
- Editorial Manager step
- Source archive in Editorial Manager
- Screen fields pasted by hand
- Required back-matter statements and their order
- Highlights
- Clean versus marked manuscript
- Live limits worth rechecking

## Manifest keys

Beyond the shared keys, an Elsevier manifest may declare `marked_manuscript`, and its
`journal_limits` may declare `highlights_min_items`, `highlights_max_items`, and
`highlight_max_characters`. The three highlights limits become required once a declared
side material has `highlight` in its filename.

```json
{
  "publisher": "elsevier",
  "submission_step": "revision source upload",
  "submission_step_checked_on": "<YYYY-MM-DD>",
  "journal_guide_url": "https://journal.example/guide-for-authors",
  "journal_limits_checked_on": "<YYYY-MM-DD>",
  "journal_limits": {
    "abstract_max_words": 250,
    "highlights_min_items": 3,
    "highlights_max_items": 5,
    "highlight_max_characters": 85
  },
  "manuscript": "main.tex",
  "side_materials": ["upload/highlights.docx", "upload/cover-letter.docx"],
  "submission_stage": "revision",
  "response_to_reviewers": "upload/response.docx",
  "marked_manuscript": "upload/marked.pdf",
  "source_required": true,
  "source_zip": "source.zip",
  "source_entrypoint": "main.tex"
}
```

## Editorial Manager step

Elsevier journals submit through Editorial Manager. Record the current EM step in
`submission_step`; it decides which files are requested now, and a step containing `source`
cannot set `source_required` to false. When the live EM screen disagrees with the Guide for
Authors about what to upload, follow the screen and keep the discrepancy as evidence.

## Source archive in Editorial Manager

EM expands the uploaded archive into one submission item per file, each needing an item
type and an order position chosen by hand. Expect this and plan the attach step for it:

- Subfolders make the archive unprocessable. Everything sits at one level.
- Figures ship as separate files inside the archive and are tagged `Figure`. EM states
  this is mandatory for production, so never embed them in a container or a subfolder.
- Per the EM/PM LaTeX Guide, order the expanded list as the root `.tex` first, then
  `.bib`, `.bst`, `.cls` and the remaining source, then the figures. Source files take the
  manuscript or editable-source item type; images take `Figure`.
- A split chapter tree survives expansion — an archive of a dozen `.tex` files builds and
  reaches production. Inlining every `\input` into one `.tex`
  (`latexpand --empty-comments main.tex`, then strip the directory prefixes the flat
  layout invalidates, including `\graphicspath`) is optional: it removes any question
  about which file is the root and shortens the list you must classify by hand.

`Latest editable source file` and `Tables (Editable Version)` reject PDFs, because
typesetting reads them; the `Figure` item type accepts PDF, so vector figures are safe.
Tables written as LaTeX inside the source already satisfy the editable-tables requirement.

## Screen fields pasted by hand

The abstract and keywords are typed into the screen, not read from the source, so they need
a plain-text copy generated from the manuscript and regenerated whenever it changes. A
stale copy is how an old abstract reaches production.

EM's abstract box is a CKEditor rich-text widget, which constrains the text:

- One physical line per paragraph. A hard-wrapped file becomes several paragraphs.
- No Markdown, no LaTeX macros, no math. They paste as literal characters; a formula has
  to be re-entered through the widget's own math button, so keep the abstract free of it.
- ASCII only. Curly quotes, en dashes, and non-breaking spaces arrive as mojibake.

Keywords go in as a single semicolon-separated line. The screen states its own keyword
count and per-keyword character limits; record them in the manifest and verify the live
word count the widget displays against the abstract limit before moving on.

## Required back-matter statements and their order

The checker verifies these headings exist in the manuscript and appear in this order:

1. CRediT authorship contribution statement.
2. Declaration of competing interest.
3. Acknowledgements and funding, as applicable to the paper.
4. Data availability statement.

Use the journal's exact required wording. CRediT roles must be accurate and agreed by all
authors. Do not invent funding, conflicts, data access, or author contributions.

## Highlights

Elsevier's general guidance is three to five bullets, at most 85 characters including
spaces, supplied as a Word document. A journal-specific guide can override when or how they
are requested, so record the live numbers in the manifest rather than trusting the default.

## Clean versus marked manuscript

A revision declares `response_to_reviewers`. `marked_manuscript` is optional but, once
declared, must exist and must differ from the clean manuscript — uploading the marked file
as the clean one is the failure this check exists for.

## Live limits worth rechecking

Abstract length, highlights, graphical abstract, keywords, anonymization, reference style,
and each upload's accepted file type vary by journal. Keep a journal's own cover-letter
questions, scope language, article types, and numeric limits in the dated manifest; they are
not general Elsevier rules.

Primary sources:

- https://www.elsevier.com/researcher/author/policies-and-guidelines/latex-instructions
- https://www.elsevier.com/researcher/author/tools-and-resources/highlights
- https://www.elsevier.com/en-gb/researcher/author/policies-and-guidelines/credit-author-statement
