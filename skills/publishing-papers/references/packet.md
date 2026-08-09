# Building the Upload Packet

Turn a mature manuscript into the files the target journal's current submission screen requests:
packet evidence, side materials, source-archive verification, and the final upload checklist.

## Contents

- [Prerequisites](#prerequisites)
- [Inputs](#inputs)
- [The manifest](#the-manifest)
- [Side materials](#side-materials)
- [Source archive](#source-archive)
- [Fields typed into the screen](#fields-typed-into-the-screen)
- [Final check](#final-check)
- [Done](#done)

## Prerequisites

`python scripts/check_packet.py` needs only Python. Two checks call external tools and stop with
exit `2` instead of passing when they are absent: `pdfinfo` (poppler-utils) for page counts and
`latexmk` for the standalone source compile.

The Markdown-to-DOCX converter needs `python-docx`. `uv run --with python-docx` fetches it per run,
which needs `uv` and network access. Without either, install the package once
(`pip install python-docx`) and call `python scripts/md_to_docx.py` directly.

## Inputs

Require the canonical manuscript source, target journal and article type, live author-guide URL,
current submission-system step, submission stage (initial or revision), author-approved facts, and
any editor or reviewer instructions.

Stop for missing facts. Never infer declarations, contributions, funding, data availability,
conflicts, EDICS categories, or conference-extension difference claims — each of these is a
statement the authors sign, and a plausible-looking guess is the kind of error that survives
review and reaches print.

## The manifest

Open the live author guide and the current submission screen, and record both in a local
`packet.json`. The manifest is the evidence that you looked, and the place a conflict between two
instruction sources gets written down instead of resolved silently.

```json
{
  "publisher": "elsevier",
  "submission_step": "revision source upload",
  "submission_step_checked_on": "<YYYY-MM-DD>",
  "journal_guide_url": "https://journal.example/guide-for-authors",
  "journal_limits_checked_on": "<YYYY-MM-DD>",
  "journal_limits": {"abstract_max_words": 250},
  "manuscript": "main.tex",
  "side_materials": ["upload/cover-letter.docx"],
  "submission_stage": "revision",
  "response_to_reviewers": "upload/response.docx",
  "source_required": true,
  "source_zip": "source.zip",
  "source_entrypoint": "main.tex"
}
```

`publisher` is required and selects which further keys are legal; the publisher reference —
[elsevier.md](elsevier.md) or [ieee.md](ieee.md) — lists its own, along with the publisher-specific
steps, statements, and screen fields. Unknown keys, including the other publisher's, are rejected,
because a silently ignored key disables the check it was meant to enable. Evidence dates older than
`--max-evidence-age-days` (30) fail: journal limits move.

## Side materials

Start from `assets/cover-letter.md` and, when the journal asks for highlights,
`assets/highlights.md`. For a revision, add the point-by-point response and any file the decision
letter requests.

Convert Markdown side materials to DOCX:

```bash
uv run --with python-docx scripts/md_to_docx.py <files.md> --out <upload-dir>
```

Then open every generated DOCX and inspect text, author names, journal name, line wrapping, and
page breaks. A file's existence is not a content review — the converter can produce a well-formed
document that names last round's journal.

## Source archive

Create a source zip only when the current step requests source. It must be flat, use ASCII
filenames, include every build input (dereference symlinks when staging), omit generated manuscript
PDFs, and compile after extraction into an empty directory with zero missing files, undefined
citations, and undefined references. The upload archive is a copy, never the canonical source tree.

Read the publisher reference for how the system presents the archive at the attach step, since that
decides the item types and ordering you assign by hand.

## Fields typed into the screen

Produce a plain-text copy of every field the submission screen makes you paste rather than read
from the source — abstract and keywords at minimum — generated from the manuscript so a later edit
cannot leave a stale copy behind. The publisher reference states the text shape the screen's editor
requires.

## Final check

```bash
python scripts/check_packet.py packet.json
```

Treat exit `2` as a blocked verification that names the missing runtime next step, not a pass. Do
not declare the packet ready until the command exits zero.

After changing the Markdown converter, prove the bundled fixture produces a real `.docx`:

```bash
uv run --with python-docx python scripts/smoke_md_to_docx.py
```

## Done

- The manifest names the current submission step and a recently checked live journal guide.
- Publisher-required statements and screen metadata are present, ordered, accurate, and author
  approved.
- Every requested side material exists as an inspected file with correct names and limits.
- When source is requested, the archive passes flat-name and standalone-compile checks.
- Fields typed into the screen exist as generated plain text in the shape the screen accepts.
- Revision packets answer every editor and reviewer item and distinguish clean from marked files.
- The upload set matches the current submission screen, not merely a generic checklist.
