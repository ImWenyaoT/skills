# Paper taste (Karpathy: a paper is a particular species)

## Source and attribution

Andrej Karpathy, "A Survival Guide to a PhD" (2016), the "Writing papers" section — original:
<https://karpathy.github.io/2016/09/07/phd/>. This file restates that methodology and adapts it to
the conventions used here; its key lines are quoted short. The original is not reproduced in full.

It **complements** [drafting-framework.md](drafting-framework.md) (Widom). Widom gives the
**section-level build order** — what goes in each section, where related work sits, how to report
experiments. Karpathy gives the **taste**: what a paper looks like as an object (its gestalt), the
single core contribution, paragraphs, and language. They do not conflict; use both.

## Contents

- [A paper is a particular species](#a-paper-is-a-particular-species)
- [Review bad papers to train a classifier](#review-bad-papers-to-train-a-classifier)
- [Find the single core contribution first](#find-the-single-core-contribution-first)
- [Gestalt: what a paper looks like](#gestalt-what-a-paper-looks-like)
- [Structure and paragraphs](#structure-and-paragraphs)
- [The anti-pattern: a laundry list](#the-anti-pattern-a-laundry-list)
- [Language: good words and bad words](#language-good-words-and-bad-words)
- [How this meets Widom's five points](#how-this-meets-widoms-five-points)

## A paper is a particular species

Writing papers well is a survival skill for a researcher, the way making fire was for a caveman.
The thing to notice is that **papers have a particular look, flow, structure, language, and set of
statistical regularities, and your academic peers expect all of them**. Early drafts are usually
bad, and that is where most of the learnable material is.

## Review bad papers to train a classifier

Reading only good papers to distil the pattern is training a binary classifier on positives only.
**You need heavy exposure to bad papers**, and **reviewing** is how you get it: at roughly a 25%
acceptance rate most of what you review is bad, and grinding through it builds a strong good/bad
classifier. You see the traps first-hand — unclear writing, undefined variables, an introduction
that stays abstract, a dive into detail far too early — and then avoid them in your own work. Join
or run a **journal club** and watch senior researchers attack papers; it shows you how yours will
be read.

## Find the single core contribution first

Before writing, settle the **single core contribution** the paper makes to the field — with the
emphasis on *single*. A paper is not a random collection of the experiments you ran. It **sells one
thing that was not obvious or did not exist before**: you argue it matters, that no one did it
before, and then support its value with controlled experiments. **Organise the whole paper around
that one contribution with surgical precision** — no fluff, nothing else smuggled in alongside.

Karpathy's own counter-examples:

- A video-classification paper with a second, unrelated multi-resolution architecture contribution
  wedged in, on the reasoning that "someone might find it interesting" and "two contributions beat
  one". **That reasoning is wrong**: the second contribution was minor and dubious, and it
  **diluted** the paper, split attention, and interested nobody.
- A CVPR 2014 paper carrying two independent models, ranking and generation — in hindsight, two
  papers.

The conclusion: **"two contributions beat one" is an illusion.** One paper, one contribution.

## Gestalt: what a paper looks like

Senior researchers use a paper's **gestalt** as a strong heuristic. Karpathy watched Fei-Fei flip
through four submissions for ten seconds each and correctly call one good and three bad — the same
verdict he reached after hours. Your paper needs **that same look**, because many people use it as
a cognitive shortcut for judging your work:

- Introduction about **one page**; related work about **one page**, with a **moderate citation
  density** — neither sparse nor crowded.
- A carefully designed **pull figure** on pages 1–2 and a **system figure** around page 3. **Not
  drawn in MS Paint.**
- Mathematical notation in the technical section; a results table **dense with numbers, some in
  bold**.
- One extra **cute analysis experiment**.
- **Exactly filling the page limit** — eight pages means eight, not a line short.

## Structure and paragraphs

- Default top-level structure: **Intro / Related Work / Model / Experiments / Conclusions**.
- Draft the introduction by first laying the top-level narrative out as **LaTeX comments**, a
  coherent skeleton, and filling the prose in underneath.
- **Each paragraph makes one specific point and states it in the first sentence**, with the rest
  supporting it. That is what makes a paper **skimmable**.
- A good introduction flow: (1) **X is an important problem** — define X first if it is not
  obvious; (2) the **core challenges** are A and B; (3) **prior work** solved it with Y, but the
  **problem with Y is Z**; (4) **this paper does W**; (5) W has these **good properties**, and the
  experiments show it.
- List only the challenges **you actually solve later**. Unrelated ones are speculation and belong
  in the conclusion.
- **Structure the whole paper, not just the introduction.** Each model section: (1) say plainly
  what this section does; (2) name the core challenge; (3) give the baseline or how prior work did
  it; (4) motivate and give your approach; (5) describe it.

## The anti-pattern: a laundry list

The structure to avoid at all costs: "Here is the problem. Right, first we do X, then Y, then Z,
then W, and here are the results." **Every step needs justification, motivation, explanation**: why
X, why Y, what the alternatives were, how others did it (a common approach can carry a citation).
**A paper is not a report, not an enumeration of what you did, not your chronological lab notes
translated into LaTeX.** It is a highly processed, tightly focused discussion of the problem, your
approach, and their context — it **teaches** your peers and **argues** each step, rather than
describing what you happened to do.

## Language: good words and bad words

You accumulate a list of good and bad words. For ML and CV papers:

- Not "**study**" or "**investigate**" — passive, boring, bad words. Use "**develop**", better
  "**propose**".
- Not "**system**", and certainly not "**pipeline**". Use "**model**".
- Do not learn "**features**" — learn "**representations**".
- **Never** "**combine**", "**modify**", or "**expand**". These are incremental, cheap words, and
  they nearly guarantee rejection.

> This complements stripping AI tone. Stripping AI tone removes empty self-praise and mechanical
> transitions; this replaces the verbs that make work sound incremental and passive.

## How this meets Widom's five points

Widom's five introduction paragraphs (**problem / why it matters / why it is hard / why it is
unsolved / approach and limitations**) and Karpathy's introduction flow (**important problem / core
challenges / prior Y and its problem Z / this paper's W / good properties and evidence**) are **two
phrasings of the same thing**. Both demand that the introduction carry problem → why it is hard and
where prior work falls short → your approach → evidence. Use either to lay the skeleton, then use
Karpathy's rules — first sentence states the point, no laundry list, good words over bad — to
finish the paragraphs and the language.
