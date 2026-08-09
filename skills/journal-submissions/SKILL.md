---
name: journal-submissions
description: Triggers on 投稿, 修回稿, 投稿材料, and journal submission packaging for a mature manuscript — Elsevier Editorial Manager, IEEE Author Portal or ScholarOne, cover letter, highlights DOCX, required statements, EDICS, supplemental material, page-limit verification, source zip, revision response, and the final upload checklist. Does not apply to creating or editing manuscript LaTeX source, class options, template scaffolding, local compile repair, or reviewing the paper's prose.
license: MIT
compatibility: Requires Python 3; pdfinfo (poppler-utils) for page counts, latexmk for the standalone source compile, and python-docx for the Markdown-to-DOCX step.
---

# Packaging Journal Submissions

## Boundary

Turn a mature manuscript into the files the target journal's current submission screen
requests. This skill owns packet evidence, side materials, source-archive verification, and
the final upload checklist. It does not start a manuscript, choose authoring layouts, repair
a general LaTeX installation, or rewrite the paper's argument.

## Prerequisites

`python scripts/check_packet.py` needs only Python. Two checks call external tools and stop
with exit `2` instead of passing when they are absent: `pdfinfo` (poppler-utils) for page
counts and `latexmk` for the standalone source compile.

The Markdown-to-DOCX converter needs `python-docx`. `uv run --with python-docx` fetches it
per run, which needs `uv` and network access. Without either, install the package once
(`pip install python-docx`) and call `python scripts/md_to_docx.py` directly.

## Inputs

Require the canonical manuscript source, target journal and article type, live author-guide
URL, current submission-system step, submission stage (initial or revision), author-approved
facts, and any editor/reviewer instructions. Stop for missing facts; never infer
declarations, contributions, funding, data availability, conflicts, EDICS categories, or
conference-extension difference claims.

## Precedence

Instructions arrive from several places and they do conflict. The narrower the audience a
source was written for, the more it outranks:

1. The decision or invitation letter, written about this manuscript.
2. The live submission screen for the current step: the item types it names, the limits it
   displays, the formats it refuses.
3. The journal's Guide for Authors.
4. Publisher-wide policy and support articles, which describe every journal and therefore
   none of them exactly.

Record the conflict in the manifest instead of resolving it silently. A screen that
contradicts the guide is a durable fact about this journal, and it will contradict it
again next round.

Your notes about a source are not that source and hold no rank at all. A digest of the
decision letter, a checklist someone typed up from the guide, a summary of last round —
each is a claim to re-verify against the artifact it describes, and each drifts toward
the generic list its author half-remembered. The specific failure to expect: a note that
promotes a publisher's optional materials into "required", sending you off to build
documents the screen never asked for. Read the letter and read the screen.

System behaviour is not a rung on this ladder. How the platform unpacks an archive, where
it puts figures, what it does to a filename — that is mechanism. It holds whatever any
instruction says, and no journal wording overrides it. The failure to avoid is inferring a
requirement from a mechanism: that a platform expands an archive into per-file items tells
you how to tag and order those items, and nothing at all about how many files the archive
should have contained.

## Build the packet

1. Establish the publisher, then read exactly one reference for the publisher-specific
   steps, statements, and screen fields:
   [references/elsevier.md](references/elsevier.md) or [references/ieee.md](references/ieee.md).
2. Open the live author guide and the current submission screen, and record both in a local
   `packet.json`. The manifest is the evidence that you looked, and the place the
   precedence conflicts above get written down.

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

   `publisher` is required and selects which further keys are legal; each publisher
   reference lists its own. Unknown keys — including the other publisher's — are rejected,
   because a silently ignored key disables the check it was meant to enable. Evidence dates
   older than `--max-evidence-age-days` (30) fail: journal limits move.

3. Start side materials from `assets/cover-letter.md` and, when the journal asks for
   highlights, `assets/highlights.md`. For a revision, add the point-by-point response and
   any file the decision letter requests.
4. Convert Markdown side materials to DOCX:

```bash
uv run --with python-docx scripts/md_to_docx.py <files.md> --out <upload-dir>
```

5. Open every generated DOCX and inspect text, author names, journal name, line wrapping,
   and page breaks. A file's existence is not a content review.
6. Create a source zip only when the current step requests source. It must be flat, use
   ASCII filenames, include every build input (dereference symlinks when staging), omit
   generated manuscript PDFs, and compile after extraction into an empty directory with zero
   missing files, undefined citations, and undefined references. The upload archive is a
   copy, never the canonical source tree. Read the publisher reference for how the system
   presents the archive at the attach step, since that decides the item types and ordering
   you assign by hand.
7. Produce a plain-text copy of every field the submission screen makes you paste rather
   than read from the source — abstract and keywords at minimum — generated from the
   manuscript so a later edit cannot leave a stale copy behind. The publisher reference
   states the text shape the screen's editor requires.
8. Run the executable final check:

```bash
python scripts/check_packet.py packet.json
```

Treat exit `2` as a blocked verification that names the missing runtime next step, not a
pass. Do not declare the packet ready until the command exits zero.

## DOCX helper smoke

After changing the Markdown converter, prove the bundled fixture produces a real `.docx`:

```bash
uv run --with python-docx python scripts/smoke_md_to_docx.py
```

## Done

- The manifest names the current submission step and a recently checked live journal guide.
- Publisher-required statements and screen metadata are present, ordered, accurate, and
  author approved.
- Every requested side material exists as an inspected file with correct names and limits.
- When source is requested, the archive passes flat-name and standalone-compile checks.
- Fields typed into the screen exist as generated plain text in the shape the screen accepts.
- Revision packets answer every editor/reviewer item and distinguish clean from marked files.
- The upload set matches the current submission screen, not merely a generic checklist.
