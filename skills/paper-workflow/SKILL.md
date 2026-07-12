---
name: paper-workflow
description: Orchestrate an academic paper from manuscript work through figures, venue authoring, and submission packaging.
disable-model-invocation: true
---

# Paper Workflow

This is a user-invoked orchestrator. It selects the next discipline; it does not duplicate their
rules or perform their work inline.

## Route

1. Establish the requested outcome and current artifact state.
2. Invoke `writing-papers` for drafting, manuscript review, academic polishing, or rebuttal text.
   Complete when the requested prose is evidence-bound and unresolved author inputs are explicit.
3. Invoke `drawing-figures` when the paper needs a figure budget or figure artifacts. Complete when
   every planned/final figure satisfies that skill's evidence contract.
4. Invoke `elsevier-articles` only when the target uses Elsevier `elsarticle` source. Complete when
   the canonical manuscript compiles reproducibly.
5. Invoke `elsevier-submissions` only for an Elsevier Editorial Manager packet. Complete when every
   requested upload artifact passes its packet checks.

Skip inapplicable disciplines. Done means the user's requested endpoint is reached and every invoked
skill has met its own completion criterion; a later possible phase is not unfinished current work.
