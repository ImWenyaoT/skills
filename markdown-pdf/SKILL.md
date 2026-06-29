---
name: markdown-pdf
description: Converts a Markdown source file into a polished, print-ready PDF — cover page, generated table of contents, syntax-highlighted code blocks, zebra-striped tables, and page-number footer. Use when the source is Markdown and the requested output is a presentable PDF/printable document/report. Do not use for resume content editing, non-Markdown conversions, or text-only Markdown edits.
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
