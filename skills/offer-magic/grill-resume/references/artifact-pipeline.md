# Artifact Pipeline

Read this reference only when layout or exported artifacts are in scope.

## Design for scanning

Use typography to expose structure:

- Give the highest-value section the strongest combination of position, space, size, weight, and anchors.
- Keep a coherent type scale and spacing rhythm; de-emphasize supporting sections before shrinking important evidence.
- Keep body text legible and respect any profile-defined minimum size.
- Let sentences wrap naturally. Rewrite orphan lines containing only a tiny fragment, character, or punctuation instead of inserting rigid manual breaks.
- Use bold for screening evidence and defensible discussion points; sparse contrast beats uniform emphasis.
- Prefer a compact one-page result for early-career candidates when evidence remains readable. Add a page when compression would damage comprehension or truth.

Complete layout when a short visual scan lands on the intended evidence and the page is neither sparse nor cramped.

## Synchronize and export

Edit the declared content source first, then update derived formats through the workspace’s existing pipeline. Preserve unrelated changes. Prefer one editable and printable HTML when HTML is part of the workflow.

Use existing workspace scripts first. Use bundled scripts when the workspace has no equivalent or when preparing an isolated review packet. Run bundled Python through `scripts/run-python.sh`, which tries `uv`, local Python, then Conda.

When the source is HTML or CSS, read [frontend-resume-layout.md](frontend-resume-layout.md) and validate it as a rendered frontend before judging the PDF projection. Use the PDF skill when PDF layout matters. Inspect the rendered artifact, not only extracted text. Verify as applicable:

- expected page count and dimensions;
- no clipping, overlap, broken glyphs, browser chrome, or orphan lines;
- fonts, minimum sizes, and visual hierarchy match the working contract;
- text remains selectable and important information is not trapped in images;
- source content and every delivered format agree;
- public previews follow the declared redaction policy;
- dirty-worktree changes outside the task remain untouched.

Finish only after the latest deliverables pass visual inspection and report their stable paths.
