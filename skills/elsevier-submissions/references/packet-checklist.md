# Editorial Manager Packet Checklist

## Contents

- Record current requirements
- Required manuscript backmatter order
- Live limits and side materials
- Extract a supplied Guide for Authors
- Source archive when requested

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
  "side_materials": ["highlights.docx", "cover-letter.docx"],
  "submission_stage": "revision",
  "response_to_reviewers": "response.docx",
  "marked_manuscript": "marked.pdf"
}
```

`submission_stage` is required and must be `initial` or `revision`. A revision must declare
`response_to_reviewers`; `marked_manuscript` is optional but, when declared, must exist and
differ from the clean manuscript. Unknown keys are rejected — a misspelled field would
otherwise silently disable the check it was meant to enable.

Run `python scripts/check_packet.py packet.json`. It checks freshness of the EM-step and
live-guide evidence, enforces the recorded abstract/highlights limits, verifies structural
statement order and real DOCX parts, confirms revision files exist, checks flat ASCII
source-zip names, and performs a standalone `latexmk` build when source is required. A missing
LaTeX runtime blocks completion instead of becoming a false pass. If the EM step contains
`source`, the manifest cannot set `source_required` to false.

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

## Extract a supplied Guide for Authors

When a guide is supplied as a PDF, saved page, or URL, build the manifest from it instead of
copying prose into the packet. Separate reusable publisher conventions from journal-specific
requirements and current submission-screen requests. Record the journal, guide source,
access date, article type, and source page or heading for every limit.

Extract these categories when present:

- editable manuscript and source-file requirements;
- article-type-specific manuscript, abstract, keyword, reference, and highlights limits;
- required declarations and their ordering or exact wording;
- separate artwork, graphical abstract, supplement, video, and research-data files;
- cover letter, title page, anonymized manuscript, response letter, and clean/marked revision;
- permissions, preprint, authorship-change, competing-interest, funding, CRediT, data, and
  generative-AI requirements.

Do not retain a journal's special cover-letter questions, scope language, article types, or
numeric limits as general Elsevier instructions. Keep those values only in the target
packet's dated manifest. When the live submission screen disagrees with the guide about
which files are requested now, follow the screen and preserve the discrepancy as evidence.

Before deleting the supplied guide, verify that every applicable requirement is either in
the packet manifest, represented by a checked upload artifact, or intentionally excluded as
journal-specific material irrelevant to the current reusable skill.

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
