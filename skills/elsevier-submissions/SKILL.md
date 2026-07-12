---
name: elsevier-submissions
description: Triggers when a mature or finished paper is being packaged for an Elsevier Editorial Manager submission step, including Elsevier 投稿, 修回稿, 投稿材料, required statements, highlights DOCX, journal correspondence, source zip, revision responses, and the final EM checklist. Does not apply to `elsarticle` scaffolding, class options, local authoring setup, generic LaTeX runtime repair, or paper prose review.
---

# Packaging Elsevier Submissions

## Boundary

Turn a mature manuscript into the files requested by the target journal's current Editorial
Manager step. This skill owns packet evidence, side materials, source-archive verification,
and the final upload checklist. It does not start a manuscript, choose authoring layouts,
repair a general LaTeX installation, or rewrite the paper's argument.

## Inputs

Require the canonical manuscript source, target journal and article type, live Guide for
Authors URL, current EM step, submission stage (initial or revision), author-approved facts,
and any editor/reviewer instructions. Stop for missing facts; never infer declarations,
contributions, funding, data availability, or conflicts.

## Build the packet

1. Read [references/packet-checklist.md](references/packet-checklist.md). Create its local
   `packet.json` manifest and record when the live journal limits were checked.
2. Confirm the required statements exist in the manuscript in the documented order and use
   the journal's exact wording.
3. Start side materials from `assets/highlights.md` and `assets/cover-letter.md`. For a
   revision, also include the response to reviewers and any marked manuscript requested by
   the editor.
4. Convert Markdown side materials to DOCX:

```bash
uv run --with python-docx scripts/md_to_docx.py <files.md> --out <upload-dir>
```

5. Create a source zip only when the current EM step requests source. It must be flat, use
   ASCII filenames, include every build input, omit generated manuscript PDFs, and compile
   after extraction into an empty directory.
6. Run the executable final check:

```bash
python scripts/check_packet.py packet.json
```

Treat exit `2` as a blocked verification that names the missing runtime next step. Do not
declare the packet ready until the command exits zero and the generated files are visually
inspected.

## DOCX helper smoke

After changing the Markdown converter, prove the bundled fixture produces a real `.docx`:

```bash
uv run --with python-docx python scripts/smoke_md_to_docx.py
```

## Done

- The manifest names the current EM step and a recently checked live journal guide.
- Required statements are present, ordered, accurate, and author approved.
- Every requested side material exists as an inspected DOCX with correct names and limits.
- When source is requested, the archive passes flat-name and standalone-compile checks.
- Revision packets answer every editor/reviewer item and distinguish clean from marked files.
- The upload set matches the current EM screen, not merely a generic checklist.
