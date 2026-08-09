# Publication artwork

One export standard covers almost every venue. Conference and journal figure requirements differ
very little in practice, so start from the default and only read a venue guide when that venue names
something the default does not already satisfy.

## The default

- **Anything that can be vector, is vector.** Plots, diagrams, schematics → PDF, EPS, or SVG with
  fonts embedded.
- **Everything else at 600 dpi** at its final physical size. Photographs, microscopy, qualitative
  panels, heatmaps.
- **Design at final column width**, text at 8 pt or larger, no meaning carried by colour alone.

That is enough for CVPR, ICCV, NeurIPS, and the ordinary Elsevier or IEEE submission.

## When to go read the guide

Four things vary enough to be worth checking, and only when the venue actually raises them:

- **Separate artwork files.** Some Elsevier journals want each figure uploaded as its own file
  rather than embedded in the PDF.
- **A stated DPI above 600**, usually for rasterised line art.
- **Colour mode** — a print journal that asks for CMYK.
- **A physical size limit** in millimetres for single- and double-column figures.

Elsevier guides classify artwork rather than giving one DPI: roughly 300 dpi for halftones,
500 for combination art, 1000 for rasterised line drawings. Those numbers are a reason to keep
line art vector, not a set of defaults to apply everywhere.

## Validate the deliverable

1. Export at final physical dimensions; DPI without print size means nothing.
2. Confirm pixel dimensions meet `inches × dpi` on both axes.
3. Inspect at the size used in the manuscript: labels, legends, symbols, and thin strokes stay
   readable, and no text is disproportionate.
4. Cite and number every figure in manuscript order, with logical filenames.
5. Keep the caption outside the artwork unless the venue says otherwise; explain every symbol and
   abbreviation, and keep text inside the image minimal.
6. Check colour contrast, and confirm meaning survives in greyscale.
7. Preserve the data and the script behind every analytical plot. A figure has to be reproducible
   from the data underneath it.
8. Treat observed or experimental images as evidence: keep the originals, use only documented,
   scientifically acceptable processing, and never generate missing evidence.

Done means the canonical vector or source artifact is retained, every raster meets its pixel
requirement, and the final manuscript rendering is legible at print size.
