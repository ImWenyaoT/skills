# Extracting an Elsevier Guide for Authors

Use this reference when a journal guide is supplied as a PDF, saved page, or URL. The goal
is a compact, evidence-backed journal profile for the current manuscript, not a copy of the
guide.

## Separate the layers

Classify every relevant statement before using it:

- **Publisher convention**: reusable Elsevier authoring behavior, such as providing editable
  source files, keeping equations and tables editable, or supplying artwork separately.
- **Journal requirement**: a volatile value or instruction for the named journal, such as
  article types, page/reference/word limits, keyword counts, review model, required sections,
  templates, or mandatory declarations.
- **Submission-step requirement**: a file or answer requested by the current submission
  system screen. Record it with the submission packet rather than the manuscript source.

Never promote one journal's limits, cover-letter questions, scope, section names, or article
types into a general Elsevier rule. Record the guide title or URL, journal, access date, and
the page or heading supporting each journal-specific value.

## Journal profile

Capture only fields present in the source; write `not stated` instead of guessing:

```yaml
journal: <name>
guide_source: <path-or-url>
checked_on: YYYY-MM-DD
review_model: <model-or-not-stated>
article_type: <selected-type>
template: <required-template-or-not-stated>
layout: <submission-layout>
limits:
  manuscript: <page-or-word-limit>
  abstract_words: <number-or-not-stated>
  keywords: <range-or-not-stated>
  references: <number-or-not-stated>
required_sections: []
required_declarations: []
artwork_requirements: []
source_files_required: <true-false-not-stated>
```

If limits apply to a formatted template rather than raw source, validate the compiled PDF.
If requirements differ by article type, keep separate profiles instead of merging their
limits.

## Reusable authoring conventions

Apply these only when the current guide confirms them or does not override them:

- Provide editable manuscript sources. A PDF is a review rendering, not a replacement for
  `.tex`, `.bib`, figures, tables, and supporting build inputs.
- Keep the title concise and informative; keep author order aligned with the submission
  system; provide complete affiliations and current corresponding-author contact details.
- Make the abstract standalone, factual, and free of undefined abbreviations. Avoid abstract
  citations unless essential and permitted.
- Submit equations as editable text, number displayed equations in citation order, and keep
  variables and notation consistent.
- Submit tables as editable text rather than images. Cite and number every table, provide a
  caption and notes, and avoid decorative rules or duplicated narrative.
- Cite and number every figure, provide a caption that explains symbols and abbreviations,
  and retain separate production-quality artwork files where requested.
- Cite every supplementary file and give it a descriptive caption. Treat supplements as
  published artifacts: verify them before upload because production may not reformat them.
- Keep citations bidirectionally complete: every in-text citation appears in the reference
  list and every listed reference is cited. Validate names, titles, year, pages, and DOI.
- Number sections and cross-refer to their numbers when the journal requires numbered
  structure; keep the abstract outside section numbering.
- Place acknowledgements and contribution, funding, conflict, data, and AI-use statements in
  the exact locations and wording required by the current guide. Obtain author approval for
  factual declarations.

## Generative AI extraction

Extract text-use and image-use rules separately. Record whether the guide requires a general
AI-use declaration, per-figure disclosure, both, or neither. Preserve the research-integrity
boundary: explanatory diagrams and reproducible data visualizations are different from
creating or altering primary observed or experimental data. Never infer permission from a
different journal or from a general publisher page when the journal guide is stricter.

## Completion check

Done means every manuscript-affecting requirement has a source location, all selected
article-type limits are represented once, and journal-specific material remains in the local
journal profile rather than this reusable reference.
