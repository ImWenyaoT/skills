# Frontend Resume Layout

Read this reference when the authoritative resume is editable HTML/CSS or when the user comments on spacing, density, wrapping, hierarchy, or print layout.

## Treat the resume as a frontend

Define the target flow before editing:

`authoritative HTML -> print CSS -> headless browser PDF -> rendered PNG -> visual and text checks`

Use an available frontend testing or debugging skill for the rendered surface. For a print-only page with no usable browser session, record that limitation and use the workspace's deterministic headless-browser build plus PDF/PNG inspection. Preserve editable controls, print-only behavior, links, and redaction behavior when they exist.

Layout work is complete only when the browser projection and delivered PDF agree; a successful build alone is insufficient.

## Freeze a layout contract

Before changing CSS, record the user-approved constraints that can fail independently:

- page size and page count;
- authoritative content source;
- minimum font sizes and maximum line height;
- fixed sections or content that must not change;
- bullet line cap and preferred full-line rhythm;
- photo dimensions, header blocks, redaction, and print behavior;
- target files such as HTML, PDF, and preview PNG.

Treat these as acceptance criteria, not suggestions. Recheck every constraint after each meaningful layout change.

Take numeric thresholds from the user, workspace profile, or an already approved artifact. When the request is qualitative, compare before and after renders and report the measured result; do not invent a millimeter target and present it as user-approved.

## Spend the page budget deliberately

Treat page height and width as a layout budget. Adjust CSS in this order:

1. Preserve approved content and evidence hierarchy.
2. Use available width, page padding, and component geometry to control wrapping.
3. Use font size, line height, letter spacing, and inter-block spacing to create a coherent vertical rhythm.
4. Rewrite or split a bullet only when its visual line cap still fails; keep its thesis and evidence boundary.

Prefer whitespace redistribution over font compression. When the bottom is empty but the top is cramped, move space into top/bottom padding, section gaps, row gaps, and line height rather than inventing new content. Judge optical balance from the rendered page, not from numerically equal margins alone.

For photo headers, model name, optional summary, contact information, and photo as separate layout blocks. Preserve the hierarchy `name > summary > contact information`. Anchor the name and photo to one top guide, and anchor the final contact row and photo to one bottom guide. A robust implementation gives the text column the photo height and uses `name -> 1fr spacer -> summary -> 1fr spacer -> contact grid`; the equal flexible spaces keep the summary vertically centered between the name and contact block, while the contact grid stays aligned to the end and the photo stays aligned to the start. Keep the name's top-left anchor stable so font-size changes grow toward the lower right instead of shifting the header origin. Reflow or resize the contact block before squeezing the summary or body.

## Control rhythm and anchors

Use final rendered lines as the source of truth. Prefer a bullet to occupy the user's chosen two or three complete lines. Avoid half-line tails and punctuation-only wraps. If preserving the core argument exceeds the cap, split the argument into another bullet with a distinct short label instead of shrinking below the minimum font size or deleting proof. When content is frozen, preserve every word and split only at a semantic boundary; do not silently rewrite the sentence.

Use `<strong>` as a scan anchor for short thesis labels, exact high-signal JD terms, and defensible evidence. Keep anchors sparse enough that the intended scan path remains obvious. Do not use manual `<br>` elements to force line counts.

## Run the frontend/PDF QA loop

After each meaningful edit:

1. Rebuild from the authoritative HTML with the workspace command.
2. Confirm page identity, meaningful content, assets, links, and absence of browser or framework errors when a browser surface is available.
3. Inspect a fresh full-page screenshot or PNG for clipping, overlap, density, hierarchy, top/bottom optical balance, and unexpected black or missing regions.
4. Use `pdfinfo` for page count and dimensions.
5. Use `pdftotext -layout` to verify selectable text, bullet wraps, orphan lines, and source/PDF agreement.
6. Check embedded fonts and the declared minimum font sizes.
7. Run `git diff --check` and preserve unrelated worktree changes.

For annotation-driven changes, keep a short mismatch ledger: annotated problem, CSS cause, rendered fix, and any intentional residual difference. Finish when the latest render passes every frozen constraint and the annotated defect is no longer visible.
