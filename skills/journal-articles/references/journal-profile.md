# Extracting a Journal Author Guide

Use this reference when a journal's author guide is supplied as a PDF, saved page, or URL —
an Elsevier "Guide for Authors", or an IEEE society "Information for Authors" page plus a
per-journal submission-guidelines page. The goal is a compact, evidence-backed journal
profile for the current manuscript, not a copy of the guide.

## Contents

- Separate the layers
- Journal profile
- Reusable authoring conventions
- Conference-extension papers
- Generative AI extraction
- Completion check

## Separate the layers

Classify every relevant statement before using it:

- **Publisher convention**: reusable authoring behavior, such as required templates, the
  citation style, editable source files, artwork supplied separately, or ORCID for
  corresponding authors.
- **Society rule** (IEEE): a policy the sponsoring society applies to all of its journals —
  page-limit bands, overlength charges, double-anonymous rollout, AI-disclosure wording.
  Record which society and which journals it claims to cover.
- **Journal requirement**: a volatile value for the named journal — article types, page,
  word, and reference limits, abstract and keyword limits, EDICS or subject areas, review
  model, required sections or declarations, submission system URL.
- **Submission-step requirement**: a file or answer requested by the current submission
  screen. Record it with the submission packet rather than the manuscript source.

Never promote one journal's limits, cover-letter questions, scope language, section names,
or article types into a publisher-wide or society-wide rule. When a society page and the
journal's own page conflict, record both with URLs and access dates and treat the journal
page as primary.

## Journal profile

Capture only fields present in the source; write `not stated` instead of guessing:

```yaml
journal: <name>
guide_source: <path-or-url>
checked_on: YYYY-MM-DD
society: <sponsoring-society-or-not-stated>
review_model: <single-anonymous|double-anonymous|not-stated>
article_type: <selected-type>
template: <required-template-or-not-stated>
layout: <submission-layout>
submission_system: <name-and-url>
limits:
  manuscript: <page-or-word-limit-and-what-counts>
  overlength: <charge-policy-or-not-stated>
  abstract_words: <number-or-range-or-not-stated>
  keywords: <range-or-not-stated>
  references: <number-or-not-stated>
required_sections: []
required_metadata: []      # EDICS/subject areas, ORCID, suggested reviewers...
required_declarations: []  # CRediT, competing interest, funding, data, AI use...
artwork_requirements: []
supplementary_policy: <summary-or-not-stated>
prior_version_policy: <conference-extension-rules-or-not-stated>
source_files_required: <true-false-not-stated>
```

If limits apply to a formatted template rather than raw source, validate the compiled PDF —
page limits are counted in the journal's own layout, which for IEEE transactions is the
two-column `journal` mode, never a single-column draft. If requirements differ by article
type, keep separate profiles instead of merging their limits.

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

## Conference-extension papers

When the manuscript extends a published conference paper, extract the policy on required
difference statements, how much new material is expected, and whether the conference version
must be uploaded at submission. Record the answers in the journal profile; the difference
summary itself belongs to the submission packet.

## Generative AI extraction

Extract text-use and image-use rules separately. Record whether the guide requires a general
AI-use declaration, per-figure disclosure, both, or neither, and where the disclosure goes.
Preserve the research-integrity boundary: explanatory diagrams and reproducible data
visualizations are different from creating or altering primary observed or experimental
data. Never infer permission from a different journal or from a general publisher page when
the journal guide is stricter.

## Completion check

Done means every manuscript-affecting requirement has a source location and access date, all
selected article-type limits are represented once, and journal-specific material stays in
the local journal profile rather than this reusable reference.
