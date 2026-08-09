# IEEE Packet Reference

## Contents

- Manifest keys
- Author Portal and ScholarOne
- EDICS
- Page count against the two-column PDF
- Abstract word range
- Supplemental material
- Conference-extension difference statement
- Resubmission of previously rejected manuscripts (SPS)
- Screen metadata worth verifying before typing
- Author Portal optional-upload fields decoded

## Manifest keys

Beyond the shared keys, an IEEE manifest declares `manuscript_pdf` (required) and `edics`
(required, non-empty), and may declare `supplemental_pdf` and `difference_statement`. Its
`journal_limits` may declare `abstract_min_words`, `max_pages`, and `supplemental_max_pages`;
a declared supplemental PDF makes `supplemental_max_pages` required.

```json
{
  "publisher": "ieee",
  "submission_step": "initial submission",
  "submission_step_checked_on": "<YYYY-MM-DD>",
  "journal_guide_url": "https://signalprocessingsociety.org/publications-resources/information-authors",
  "journal_limits_checked_on": "<YYYY-MM-DD>",
  "journal_limits": {
    "abstract_min_words": 150,
    "abstract_max_words": 250,
    "max_pages": 13,
    "supplemental_max_pages": 6
  },
  "manuscript": "main.tex",
  "manuscript_pdf": "upload/manuscript.pdf",
  "edics": ["<unified-EDICS-code>"],
  "side_materials": ["upload/cover-letter.docx"],
  "submission_stage": "initial",
  "supplemental_pdf": "upload/supplemental.pdf",
  "difference_statement": "upload/difference-statement.pdf",
  "source_required": true,
  "source_zip": "source.zip",
  "source_entrypoint": "main.tex"
}
```

## Author Portal and ScholarOne

IEEE journals submit through the IEEE Author Portal (Atypon, `ieee.atyponrex.com`) or the
older ScholarOne. The Author Portal requires **both** a `Main Document - LaTeX` archive
(.tex/.zip/.tar.gz) **and** a `Main Document - PDF` at initial submission — the older
"PDF only at initial" convention no longer holds, and the Portal screen is authoritative.
Reviewers read the uploaded PDF; the archive feeds validation and production.

Build the archive to stand alone: include every `.tex`, `.bib`, figure, and the `.bbl`, and
bundle `IEEEtran.cls` because the upload field asks for classes. Dereference symlinked
assets when staging (`cp -L`) — an archive of symlinks uploads empty. Run `pdffonts` on the
upload PDF and require every font embedded. IEEE also offers the LaTeX Analyzer
(https://latexqc.ieee.org/, login required); a clean standalone compile covers its core
checks in advance.

## EDICS

EDICS categories are required and typed into the screen, not uploaded, so record them in
`edics` and the checker enforces that they were chosen at all. Download the current Unified
EDICS spreadsheet and filter by its Journal column for the target journal: identically named
codes route to different journals — literal "Tracking" codes route to T-SP, multimodal codes
to T-MM, and T-IP takes the IV-* family.

## Page count against the two-column PDF

Page limits are judged against the compiled two-column `journal` rendering, so
`manuscript_pdf` must be the actual upload PDF, never a single-column draft. The checker
counts pages with `pdfinfo` and blocks with exit `2` when poppler-utils is absent rather
than reporting a pass. Societies override IEEE-wide defaults per journal (page bands,
overlength charges, supplemental caps) and those exceptions change — record the live
numbers.

## Abstract word range

IEEE societies state a range, not just a cap: SPS journals require 150–250 words with no
abbreviations, footnotes, displayed equations, or references. Record both
`abstract_min_words` and `abstract_max_words`; a 120-word abstract fails a 150-word floor
just as loudly as an overlong one.

## Supplemental material

Supplemental files have their own page cap and are declared separately from the manuscript.
A declared `supplemental_pdf` requires its recorded limit, so the cap comes from the live
journal page rather than memory.

## Conference-extension difference statement

When the manuscript extends a published conference paper, the society typically requires a
summary of differences and may request the conference version as a supporting file. Declare
the summary as `difference_statement`, and keep the claimed differences consistent with the
manuscript's related-work statement.

## Resubmission of previously rejected manuscripts (SPS)

SPS policy applies to manuscripts rejected "from any journal or conference for any reason",
including other publishers' journals.

- The submission questionnaire asks new submission versus resubmission; answer truthfully.
- A resubmission must attach a supporting document with **verbatim quotations of all
  relevant parts of all previous review reports** plus how each point was addressed. Declare
  it in `side_materials` so the checker enforces its existence.
- Only **one** resubmission is allowed per manuscript (scope-based rejections and explicit
  reject-and-resubmit invitations excepted) — a later rejection closes the society's sibling
  journals as fallbacks. Budget polish accordingly.

## Screen metadata worth verifying before typing

- ORCID: validate the ISO 7064 mod 11-2 check digit for every author before entering. A
  transposed digit passes visual inspection but fails the checksum.
- Corresponding e-mail: must match the manuscript's page-1 footnote and the Portal account.
  A manuscript still under review elsewhere keeps its original address there — contact
  information stays consistent per venue.
- Keywords and suggested/opposed reviewers are typed, not uploaded. Record the chosen values
  next to the manifest so the screen can be filled consistently.

## Author Portal optional-upload fields decoded

- `Previously Published - Statement / Files` — for earlier *publications*, such as the
  conference version being extended. A rejection elsewhere is not a publication; leave these
  empty for rejected-and-resubmitted work.
- `Supporting Documents` (max 1) — where the resubmission response document goes; the
  new-versus-resubmission question is asked in the Additional Information step.
- `Cover letter / Comments` — editor-only, never shown to reviewers; optional at initial
  submission.
- `Main Document - Tracked Changes` — revision rounds only (latexdiff-marked PDF).
- The Portal preview may re-render the LaTeX single-column with floats at the end; that is
  its converter, not a manuscript defect.

Primary sources:

- IEEE Author Center: https://journals.ieeeauthorcenter.ieee.org/
- IEEE SPS Information for Authors: https://signalprocessingsociety.org/publications-resources/information-authors
- IEEE Template Selector: https://template-selector.ieee.org/
