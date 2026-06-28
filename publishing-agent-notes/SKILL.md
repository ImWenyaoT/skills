---
name: publishing-agent-notes
description: Use only for the personal notes site rooted at /Users/edward/Documents/intern/docs/notes or the ImWenyaoT/notes repository: publishing agent paper/code reading notes, converting those notes to MkDocs, configuring that site's GitHub Pages, or verifying its artifact. Do not trigger for generic MkDocs, generic GitHub Pages, or unrelated blog/documentation sites.
---

# Publishing Agent Notes

Publish the intern agent reading notes as a small MkDocs site without exposing unrelated
`docs/` files or confusing source files with GitHub Pages output. Treat `docs/notes` as
the MkDocs source and `docs/site` as generated output.

## Workflow

1. Confirm the target: note content changes, MkDocs structure changes, GitHub Pages deployment,
   or live-site verification.
2. Inspect current files before editing: `docs/notes/mkdocs.yml`, `docs/notes/**/*.md`,
   `docs/notes/assets/styles.css`, and `.github/workflows/pages.yml`.
3. Keep public content under `docs/notes`; do not move helper configs to top-level `docs/`
   just because MkDocs examples do.
4. Keep PDFs and large paper assets under `docs/paper`; the Pages workflow copies them into
   `docs/site/paper` after build.
5. Build with `mkdocs build --config-file docs/notes/mkdocs.yml --strict`. Use the project
   venv or a temporary venv if MkDocs is not installed. Install from
   `docs/notes/requirements-mkdocs.txt`, not ad hoc package names.

## Publishing rules

- GitHub Pages serves static files. MkDocs must build the site first; Pages does not run
  MkDocs at request time.
- `docs/notes/mkdocs.yml` intentionally sets `docs_dir: .` and `site_dir: ../site` so the
  source can stay under `docs/notes`.
- `exclude_docs` should keep `mkdocs.yml` and `requirements-mkdocs.txt` out of rendered pages.
- `.github/workflows/pages.yml` is the deployment authority. Preserve the strict MkDocs build
  and artifact path `docs/site`.
- Do not commit generated `docs/site` unless the repository explicitly changes to branch-based
  static publishing.

## Verification

- Content-only changes: run the strict MkDocs build and inspect the changed pages.
- Publishing changes: confirm `.github/workflows/pages.yml` uploads `docs/site`, then verify
  the live site at `https://imwenyaot.github.io/notes/` after push.
- Live-site verification should check HTTP 200 and a phrase from the changed note.

## Common pitfalls

- If asked whether GitHub Pages supports MkDocs, answer: yes, by serving MkDocs-generated
  static HTML.
- If fewer files should be exposed under `docs/`, keep source files under `docs/notes` and
  configure MkDocs from there instead of flattening everything.
- If a command scans `/Users/edward/Documents/intern` broadly, cap depth and output. That tree
  has large archives and nested projects that can flood context.
