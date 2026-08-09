# Review dimensions

The four passes a full manuscript review makes. Each one names what to look for and what a finding
has to carry; classify every finding as P0, P1, or P2 back in the skill.

## Contents

- [1. Language and format](#1-language-and-format)
- [2. Logical self-consistency](#2-logical-self-consistency)
- [3. Figure-text linkage](#3-figure-text-linkage)
- [4. Experimental data](#4-experimental-data)

## 1. Language and format

Check for: sentence fragments; subject-verb agreement; spelling and out-of-vocabulary words; mass
nouns used as count nouns (`researches`, `equipments`); sentences that run long and dense; informal
register; weak or vague verbs; repeated words; padding; overused connectives; undefined
abbreviations and initialisms; misused `etc.`; comma splices and run-ons; redundant parentheses,
repeated abbreviations, over-bolding, over-explaining.

Polish to: standard academic written English; no contractions (`it is`, not `it's`); no ornate or
obscure vocabulary; no possessive on a method, model, or system name (prefer `the performance of
METHOD`); and no paragraph converted into a list unless the source was a list or the author asked.

Widom's general-writing hard rules — each one greppable, and each one prone to creeping back in
through paragraphs newly written for a revision:

- **Bare referents.** A sentence-initial `This` / `That` / `It` carries an explicit noun after it
  (`This desaturation …`, not `This is …`). Walk them with
  `grep -nE "^(This|It|That) "` and judge each.
- **Italics mark definitions and quotations, not emphasis.** Delete emphatic italics such as
  `\emph{without any fine-tuning}`; naming definitions such as
  `\emph{Retinex-inspired decomposition}` are legitimate.
- **`etc.` only when the remaining items are entirely obvious**, and never "for various reasons" —
  give the reasons.
- **A term or notation is defined once** (a reminder after a long gap aside). A second parenthetical
  definition of the same abbreviation is a violation.
- Section pointers on contribution bullets, a conclusion that does not restate the abstract (use a
  quantitative phrasing instead), and limitations inside introduction point 5 — those three live in
  the drafting framework, and **a review checks them again**: an abstract and conclusion rewritten
  for a revision drift back toward each other, and a newly added contribution is the one that loses
  its pointer.

### Disposing of block citations

A multi-key `\cite{a,b,c}` renders as [1,2,3] in a numeric journal style, which Elsevier editors
explicitly forbid. Take one of two routes at each site:

- **Split.** When the sentence names methods, attach each citation to its own method name
  (`RetinexNet \cite{a}, KinD \cite{b}, and URetinex-Net \cite{c} explicitly split …`). No
  reference is lost, so this is the first choice.
- **Trim.** A general statement carrying a string of citations — three surveys on one sentence, a
  topic sentence citing the set of methods the next paragraphs name one by one, a second reference
  back to a set already cited — keeps only the most relevant one, or loses the whole block when
  each member is already cited by name elsewhere.

The test: every `\cite` answers "which specific claim in this sentence does this reference
support?" One key, one claim. A key with no claim behind it is what trimming removes. Splitting the
block into consecutive single citations (`X \cite{a} \cite{b}`) does not comply — that is the same
block with different punctuation. Delete any bib entry left uncited afterwards.

Prevention: a related-work section that narrates method by method is immune by construction. A
block citation is almost always the symptom of a lazy general sentence; make the sentence specific
and the citations separate themselves.

## 2. Logical self-consistency

Check for: statements that contradict each other; a core concept renamed halfway through; causal
leaps; conclusions reaching past their evidence; contributions claimed in the introduction that no
experiment verifies; a method description that cannot explain the measured behaviour; failure
cases, limitations, or boundaries that conflict with the claims; and sentences that look like
explanations but are patches.

The pass does not attack the work's novelty. It asks whether the paper holds together as a story.

## 3. Figure-text linkage

Read the figures, tables, and prose as one channel of information. A reviewer who reads only the
figures and tables should get roughly 80% of the core message. The prose adds the necessary
background, causality, and interpretation rather than repeating what the figure already shows.
Figures and tables complement each other instead of making the same point twice. Every reference in
the text points at the right object. Each caption stands on its own for the key information. Look
for paragraphs of prose that a figure could carry, for a figure order that fights the narrative,
for a table that would read better as a plot, and for a plot that needs a table beside it for exact
values.

## 4. Experimental data

Every conclusion stays strictly inside the supplied data: invent no numbers, overstate no gain,
report no phenomenon that is not there. The focus: comparison against the state of the art;
parameter sensitivity; the performance-efficiency trade-off; each module's contribution in the
ablation; consistency of datasets, metrics, and settings; single runs kept distinct from repeated
ones; and whether error bars, confidence intervals, or significance marks are needed.

Avoid ledger prose. Not "A is 0.5 and B is 0.6" but what the difference means for the claim.
