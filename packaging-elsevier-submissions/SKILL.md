---
name: packaging-elsevier-submissions
description: Use when packaging a finished LaTeX manuscript for an Elsevier journal via Editorial Manager — initial submission or revision. Covers the required statement set and its order (CRediT, declaration, acknowledgements, data availability), hard specs (abstract/highlights/graphical-abstract limits), single- vs double-column strategy, the flat ASCII source zip, cover letter, and the defensive-writing / self-citation gotchas seen on HGD-Net and CARETrack.
---

# Packaging Elsevier Submissions

## Overview

Turn a *mature* manuscript into an Editorial Manager (EM) submission packet. The narrative
and the actual `.tex` are authored elsewhere — this is the **last-mile packaging** layer:
right statements, right order, right specs, a clean flat source zip. Done for HGD-Net
(Information Sciences, accepted) and CARETrack (Information Fusion). The reusable playbook,
templates, CLI and a single-column `example.tex` survive under
`docs/_archive/paper-pipeline/` (archived 2026-06-27) — **point to them, don't rewrite.**

## Authoritative sources (read these first)

- Per-paper truth: `<project>/paper/submission/<JOURNAL>_guide.md` + `submission/README.md`
  + `submission/shared_materials/` (hand-filled cover letter / declaration / highlights md).
- Reusable: `docs/_archive/paper-pipeline/knowledge-work-half/` — `PLAYBOOK.md`,
  `submission/*_template.md`, `submission/checklist_initial.md`, `guides/revision_guide.md`,
  `guides/example.tex` (single-column). Tools: `…/workflow-half/bin/make-submission-zip.py`,
  `make-marked-pdf.py`; journals registry `…/workflow-half/registry/journals.yaml`.

## Required statements — set AND order

In the manuscript back-matter, in this order (the order itself was a real correction point):

1. **CRediT authorship contribution statement** — roles per author. Not a separate upload
   file; goes in manuscript and/or the EM form.
2. **Declaration of competing interest** — mandatory; standard sentence if none.
3. **Acknowledgements / Funding** — exact phrasing, **no parentheses**:
   `This work was supported in part by … under Grant <number>.`
4. **Data availability** statement — mandatory at submission.

## Hard specs (verify against the live journal guide — numbers vary)

| Item | Spec |
|---|---|
| Abstract | ≤ 250 words, single paragraph, factual, no citations/abbreviations |
| Highlights | 3–5 bullets, **≤ 85 chars each (incl. spaces)**, Word file whose name contains "highlights" |
| Graphical abstract | optional; single image, ≥ 1328×531 px, 300 dpi, Times/Arial fonts, **no AI-generated art**, no extra text/border |
| References | "Your Paper Your Way": any *consistent* style at initial submission; `elsarticle-num` at revision |

## Single- vs double-column

Keep **two** LaTeX sources so edits to one never corrupt the other:
`main.tex` = canonical double-column; `main_preprint.tex` = `elsarticle` `preprint`
single-column adaptation. Export the submission `01_manuscript.pdf` from the single-column
version (cleaner first-read); preserve the double-column original.

## EM source zip (revision / when source required)

`make-submission-zip.py <slug> <stage>` produces a **flat (no subdirs), ASCII-filename**
zip with **real `.cls/.bst` materialized in**, excluding the compiled `main.pdf`. Always
**verify**: unzip into an empty dir and `latexmk -pdf main.tex` must compile standalone,
with zero undefined references. Marked-diff PDF for revisions: `make-marked-pdf.py <slug>
<prev> <cur>` (latexdiff).

## Voice & content gotchas (cost real round-trips before)

- **Regular research-paper tone, not defensive.** Strip hedging / over-causal / "we
  acknowledge out-of-domain…" framing; state results plainly. Hunt the *whole* file for
  each issue class (font drift, repeated explanations), not just the first hit.
- **Concede adopted components openly** ("built on the adopted X [cite]; unlike prior…") —
  this is what dropped HGD-Net from major to minor revision.
- **Self-cite** your relevant prior work where it genuinely supports the claim.

## Common mistakes

- Editing the manuscript inside `submission/upload/` — that's a regenerated build product;
  fix in `../manuscript/` or it's overwritten.
- Uploading LaTeX source at initial submission when EM only wants the PDF (source at
  revision) — check the **current EM step**, which overrides the Guide's generic text.
- Putting `.cls/.bst` in the draft tree; treating the flat zip as canonical. Both are
  build products — keep one source of truth, materialize on package.

## Final check

Walk `docs/_archive/paper-pipeline/knowledge-work-half/submission/checklist_initial.md`
(initial) or `checklist_revision.md` (revision) line by line before declaring ready.

## 投稿材料 md → EM DOCX

将 Highlights / Cover Letter / CRediT 等投稿材料写成 `.md` 文件，再用捆绑的脚本批量转成
Editorial Manager 所需的 Arial 11pt DOCX：

```bash
uv run --with python-docx scripts/md_to_docx.py <a.md> <b.md> --out <dir>
```

- 每个输入文件在 `<dir>` 下生成同名 `.docx`（`highlights.md` → `highlights.docx`）。
- 自动去除 `**bold**` 标记和 `` `code` `` 标记（仅保留文字内容）。
- 全局样式：Normal / Body Text → Arial 11pt；Heading 1–3 → Arial 13–11pt。
- 脚本本体：`scripts/md_to_docx.py`（来自 docxkit，零硬编码，纯 argparse CLI）。
- 无需预装依赖，`uv run --with python-docx` 隔离运行即可。
