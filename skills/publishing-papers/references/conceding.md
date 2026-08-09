# Conceding without losing the paper

Four comments cannot be answered by simply running what was asked, because answering each one
honestly means giving something up. The techniques below differ, but they share a shape: concede the
narrow point fast and in your own words, then spend the space on what the concession does *not*
cost you. A concession you volunteer costs one sentence; the same fact found by the reviewer costs
your credibility on everything else.

## Contents

- [The novelty overlaps something you adopted](#the-novelty-overlaps-something-you-adopted)
- [The reviewer's premise is factually wrong](#the-reviewers-premise-is-factually-wrong)
- [A number's provenance cannot be recovered](#a-numbers-provenance-cannot-be-recovered)
- [The experiment proves the reviewer right](#the-experiment-proves-the-reviewer-right)

## The novelty overlaps something you adopted

Name the components you adopted, cite them, and state plainly what is yours: *"Built on the adopted
X [cite]; unlike prior work, we …"*

This is counterintuitive and it works. Volunteering an adopted component is what moved one
submission from major to minor revision. The reviewer is already suspicious; a concession you
volunteer costs one sentence, while the same fact discovered by the reviewer costs your credibility
on everything else.

The corollary: **keep adopted components out of the contribution list.** A contribution that leads
with someone else's idea invites exactly the "these two works look similar" comment.

When that comment does arrive, answer it by differentiating **claim sets**, not architectures.
Rewrite the contribution list until every claimed contribution is distinct from both the nearest
cited method and your own prior work. The objection is usually one of three shapes — *collision*
(two works claim the same thing), *hierarchy* (a minor claim is billed as a major one), or
*emphasis* (the adopted part leads) — and none of the three is a demand to abandon the adopted
component. State the adopted parts as foundations, then locate the novelty where it actually lives:
in the mechanism, the allocation, the interaction, the objective, or the evidence. If a separate
comment challenges a foundation itself, answer it there rather than letting it bend the novelty
response.

## The reviewer's premise is factually wrong

Reviewers make factual errors. Handle it in this order — the order is the whole technique:

1. **Concede the literal claim** if it is literally true. Spend no word defending it.
2. **Locate the premise** behind the claim, which is usually where the error lives ("I guess the
   authors want X" is a premise wearing a disguise).
3. **Correct it with evidence, briefly** — ideally from a source the reviewer already trusts (the
   original paper of the method they are citing at you, their own cited work's tables).
4. **Then do what they asked anyway.** The correction earns nothing on its own; the experiment
   does. Running the comparison they wanted is what converts "the author argued with me" into "the
   author addressed it."

A correction without an experiment reads as a dodge, no matter how right it is.

## A number's provenance cannot be recovered

A number matching a published one is not evidence that it was copied from the paper. Before you
explain a suspicious baseline, go looking: run directories, archived machines, logs, checkpoints,
scripts, old drafts, a co-author's records. Keep three states apart — reproduced locally with
artifacts, reported from an external source, and provenance not yet recovered. "Not yet recovered"
is an evidence slot to work on, not a licence to write a tidy origin story.

When someone remembers a real run on another machine, hold that as a hypothesis and leave the
response unwritten until the artifact or the protocol turns up. A letter can explain an
unfavourable real result; it cannot recast it as a citation or a protocol mix-up that never
happened.

This governs your *investigation*, not your prose. What you may say is a separate rule — the
response letter reports only work that exists — and neither one licenses guessing.

## The experiment proves the reviewer right

The comparison they demanded sometimes returns the answer they predicted and you feared. Your
method is not the best choice; the component they doubted contributes nothing measurable. This is
the moment the revision is won or lost, and the instinct that loses it is to go looking for the cut
of the data where you still win.

Report the result. A number you suppress is a number the next reviewer finds, and by then it costs
the paper rather than one comment.

Then separate two questions that the reviewer's phrasing fused into one. *"Prove that X is the best
choice"* presumes X is your contribution. Frequently it is not — it is the substrate your
contribution runs on, and the comparison you just ran across substrates is evidence that your real
contribution holds across all of them. Name what you actually claim, show the comparison supports
that claim, and state plainly why the paper keeps the substrate it uses: comparability with the
prior work under review, cost, or scope. Volunteering the better alternative as a direction
strengthens the paper, because a limitation you name yourself is one the reviewer no longer has to.

Two details make the concession land instead of read as defeat:

- **Say that their judgement was confirmed.** They wrote the comment because they suspected
  something; the experiment agreeing with them is the strongest evidence you took it seriously.
- **Point out any handicap the losing arm carried in its favour.** If your method had a trainable
  parameter the baselines lacked and still lost, say so — it forecloses "you did not tune the
  comparison properly," which is otherwise the next round's comment.

The boundary: hunting for a favourable framing is legitimate, and hunting for a favourable number
is not. Reframing chooses which honest claim to foreground. Rerunning until the result flatters
you, or reporting the one split where you win, is the fabrication that ends careers. If a new angle
needs a new experiment, commit to reporting whatever it returns before you launch it.
