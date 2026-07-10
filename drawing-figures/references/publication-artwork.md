# Publication Artwork Requirements

Read the target venue's current guide first. Record the required file types, physical size,
minimum resolution, color mode, font handling, and whether figures must be separate files.
Do not generalize values from one journal.

## Classify before exporting

| Artwork class | Examples | Preferred output |
|---|---|---|
| Vector drawing | plots, diagrams, schematics | PDF or EPS with fonts embedded or text converted as required |
| Halftone | photographs, microscopy, continuous-tone images | TIFF, PNG, or JPEG at the guide's minimum DPI |
| Line drawing | monochrome strokes, text-heavy raster diagrams | vector preferred; otherwise high-resolution TIFF or PNG |
| Combination | line/text overlays on photographs or heatmaps | vector composition or raster at the guide's combination-art minimum |

Elsevier guides commonly distinguish these classes rather than accepting one DPI for all
artwork. A frequently encountered baseline is 300 dpi for halftones, 500 dpi for combination
art, and 1000 dpi for rasterized line drawings, but these are extraction cues, not defaults:
the target journal's current guide controls.

## Validate the deliverable

1. Export at final physical dimensions; DPI without print size is incomplete.
2. Confirm pixel dimensions meet `inches x required DPI` in both axes.
3. Inspect at the size used in the manuscript: labels, legends, symbols, and thin strokes
   remain readable without disproportionate text.
4. Cite and number every figure in manuscript order. Use logical filenames and keep each
   requested artwork item separate.
5. Supply a caption outside the artwork unless the venue requires otherwise; explain every
   symbol and abbreviation while keeping text inside the image minimal.
6. Check accessible color contrast and ensure meaning is not encoded by color alone.
7. Preserve the data and script behind analytical plots. AI-assisted data visualization must
   remain reproducible from the underlying data.
8. Treat primary observed or experimental images as evidence: preserve originals and use
   only documented, scientifically acceptable processing. Never generate missing evidence.

Done means the canonical vector or source artifact is retained, every raster upload meets
the venue's class-specific pixel requirement, and the final manuscript rendering is legible.
