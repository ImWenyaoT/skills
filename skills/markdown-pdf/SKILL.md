---
name: markdown-pdf
description: 'Markdown-to-PDF conversion for presentable printable documents/reports: cover page, generated table of contents, syntax-highlighted code, styled tables, and page-number footer. Use only when the source is Markdown and the requested output is PDF. Do not use for resume content editing, non-Markdown conversion, or text-only Markdown edits.'
---

# Converting Markdown to PDF

Turn a Markdown file into a polished, PDF-ready document.

## Inputs

- `markdown_file`: required `.md` source.
- `title`: optional; if omitted, infer from the first `# Heading`, then the filename.
- `author`: optional; if omitted, leave blank.
- `date`: optional; if omitted, use the current local date.

## Workflow

1. Validate the input is Markdown.
2. Read the Markdown text (don't persist the original upload).
3. Render safe HTML with a custom cover page.
4. Generate a table of contents from the headings.
5. Syntax-highlight fenced code blocks.
6. Render pipe tables as HTML tables with alternating row backgrounds.
7. Save a self-contained HTML artifact.
8. Export/print the artifact to PDF with a page-number footer.

## Rendering decision

Keep the workflow tool-agnostic: use the best supported renderer in the current runtime instead of
requiring one bundled browser or PDF engine. A fixed engine would make the skill less portable and
would still leave font availability, browser versions, and platform print behavior uncontrolled.
Determinism therefore comes from requiring the same observable artifacts and acceptance evidence
regardless of which renderer produced them.

## Completion checklist

Do not report completion until every applicable item below has direct evidence. A renderer exiting
successfully is not sufficient evidence by itself.

- **Artifacts:** both a saved `.html` artifact and the final `.pdf` artifact exist and are non-empty.
- **Self-contained HTML:** the HTML opens as a standalone file without network access. Embed all
  required styles, fonts needed for legibility, images, and other resources in that file; sidecar
  files, temporary upload paths, and remote URLs do not satisfy this requirement.
- **Structure:** inspect the HTML and confirm source headings remain headings, every generated table
  of contents entry points to the intended heading, and the no-heading fallback appears when needed.
- **Content rendering:** inspect representative pipe tables and every fenced code block. Tables must
  retain their rows and columns; code must retain whitespace and literal characters, with escaped
  plain code used when syntax classification is unavailable.
- **PDF smoke check:** open the PDF with a PDF parser or viewer, confirm it has at least one page, and
  confirm the page count is plausible for the rendered HTML. A file-existence check alone does not
  prove that the PDF is readable.
- **Pagination:** inspect the footer on representative pages, including the first applicable content
  page and the final page, and confirm page numbers are present, ordered, and not clipped. If the
  cover intentionally suppresses its number, document that exception and verify numbering after it.
- **Visual sample:** render or view at least the first page, one content page containing a table or
  fenced code block when present, and the final page. Check for clipping, overlap, missing glyphs,
  broken links/resources, unreadable contrast, orphaned headings, and obviously bad page breaks.
- **Evidence report:** name the HTML and PDF artifact paths and record the checks performed, including
  PDF open/page-count evidence and which pages were visually sampled. If any required check fails or
  cannot be performed, report the blocker instead of claiming the conversion is complete.

## Failure behavior

- Not Markdown → fail with a clear, user-readable validation error.
- No headings → keep it printable with a short table-of-contents fallback.
- An unclassifiable code token → render escaped plain code.
- Never persist the raw uploaded Markdown file.

## Tooling

Prefer a Markdown→HTML renderer plus an HTML→PDF/print step over ad-hoc shell commands. If your
runtime exposes helpers for upload-text extraction, Markdown→HTML rendering, artifact saving, and
HTML→PDF, use those; otherwise a local toolchain (a Markdown library + a headless browser or a
print-to-PDF engine such as weasyprint) achieves the same result.
