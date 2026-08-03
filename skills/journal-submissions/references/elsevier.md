# Elsevier Packet Reference

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

## The revision upload set

A revision screen asks for a fixed set, and the item types are not interchangeable:

| Item type | What it is |
|---|---|
| Cover letter | Restates the novel contribution; a revision also summarises what changed |
| Response to reviewers | Point-by-point, every numbered comment answered |
| Revised manuscript (with changes marked) | A **built PDF**, for review only |
| Latest editable source file | The **source archive**, for typesetting |
| Declaration of competing interest | Completed template |
| CRediT author statement | DOCX, author name then roles |

**PDF is rejected for "Latest editable source file" and for "Tables (editable version)".**
Those two slots take Word or LaTeX, because production typesets from them. Uploading the
built PDF into the source slot is the most common way a revision stalls before review.

For a LaTeX submission, bundle every source file into one archive: `.tex`, `.bib`, tables,
any `.cls` or `.sty` not in TeX Live, and anything else the manuscript needs to build.
Figures go up as **separate files as well**, not only inside the archive — production
requires them individually. Keep equations in editable form rather than as images; an
equation shipped as a picture surfaces as a query at proof stage.

The built PDF and the source archive must describe the same manuscript. Build the PDF from
the very files in the archive, in the same pass, so the two cannot drift.

The clean version is what moves to production, so its source archive — figures, `.bib`, and
class files included — is the copy that has to be complete and final.

## Mandatory checks that gate the editorial process

Some journals list requirements whose failure stops the paper before review. They read as
boilerplate and are enforced anyway:

- **An institutional e-mail for every author**, in the submission system *and* on the title
  page. Where one genuinely does not exist, the cover letter states why.
- **Exactly one corresponding author**, in both the system and the manuscript. Neither the
  corresponding author nor the author list can change after acceptance.
- **Every author approves the submission** through a link they each receive. Tell the
  co-authors before you submit; an unapproved paper simply waits.
- A cover letter accompanies every manuscript, and for a research article it states the
  novel contribution against the published literature.

Check these against the live screen at revision time too. A requirement that went unremarked
at first submission is still a requirement, and a desk rejection over an e-mail address costs
the same as one over the science.

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
