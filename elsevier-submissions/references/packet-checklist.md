# Editorial Manager Packet Checklist

## Record current requirements

Before generating files, open the target journal's live Guide for Authors and the current
Editorial Manager step. Record both in a local `packet.json`; the current EM step overrides
generic instructions about which files are requested now.

```json
{
  "em_step": "revision source upload",
  "em_step_checked_on": "2026-07-10",
  "journal_guide_url": "https://journal.example/guide-for-authors",
  "journal_limits_checked_on": "2026-07-10",
  "journal_limits": {
    "abstract_max_words": 250,
    "highlights_min_items": 3,
    "highlights_max_items": 5,
    "highlight_max_characters": 85
  },
  "manuscript": "main.tex",
  "source_required": true,
  "source_zip": "source.zip",
  "source_entrypoint": "main.tex",
  "side_materials": ["highlights.docx", "cover-letter.docx"]
}
```

Run `python scripts/check_packet.py packet.json`. It checks freshness of the EM-step and
live-guide evidence, enforces the recorded abstract/highlights limits, verifies structural
statement order and real DOCX parts, checks flat ASCII source-zip names, and performs a
standalone `latexmk` build when source is required. A missing LaTeX runtime blocks completion
instead of becoming a false pass. If the EM step contains `source`, the manifest cannot set
`source_required` to false.

## Required manuscript backmatter order

1. CRediT authorship contribution statement.
2. Declaration of competing interest.
3. Acknowledgements and funding, as applicable to the paper.
4. Data availability statement.

Use the journal's exact required wording. CRediT roles must be accurate and agreed by all
authors. Do not invent funding, conflicts, data access, or author contributions.

## Live limits and side materials

Journal rules vary. Verify the live guide for abstract length, highlights, graphical
abstract, keywords, anonymization, reference style, and each upload's file type. Elsevier's
general highlights guidance says three to five bullets, at most 85 characters including
spaces, supplied as a Word document, but a journal-specific guide can override when or how
they are requested.

Generate Markdown side materials with:

```bash
uv run --with python-docx scripts/md_to_docx.py highlights.md cover-letter.md --out upload
```

Open every generated DOCX and inspect text, author names, journal name, line wrapping, and
page breaks. A file's existence is not a content review.

## Source archive when requested

- Include every `.tex`, `.bib`, figure, table, and nonstandard class/style needed to build.
- Use a flat archive with ASCII filenames and no generated manuscript PDF.
- Do not treat the upload archive as the canonical source tree.
- Extract into an empty directory and compile the declared entrypoint with `latexmk -pdf`.
- Require zero missing files, undefined citations, and undefined references.

Primary sources:

- https://www.elsevier.com/researcher/author/policies-and-guidelines/latex-instructions
- https://www.elsevier.com/researcher/author/tools-and-resources/highlights
- https://www.elsevier.com/en-gb/researcher/author/policies-and-guidelines/credit-author-statement
