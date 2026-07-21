# Karpathy Recipe — Stage by Stage

Source: Andrej Karpathy, *A Recipe for Training Neural Networks*
(karpathy.github.io/2019/04/25/recipe/).

This file expands the six stages of [SKILL.md](../SKILL.md) tip by tip. Each tip gives the reason
and the method. SKILL.md names the gate of each stage. This file gives the tips that open that
gate. Read [checklist.md](checklist.md) for the failure modes behind a gate that stays shut. This
file is the forward build order. The checklist is the backward search after a run goes wrong.

## Contents

- [Two root causes](#two-root-causes)
- [Three pillars of the recipe](#three-pillars-of-the-recipe)
- [Stage 1 — Become one with the data](#stage-1--become-one-with-the-data)
- [Stage 2 — Skeleton and dumb baselines](#stage-2--skeleton-and-dumb-baselines)
- [Stage 3 — Overfit](#stage-3--overfit)
- [Stage 4 — Regularize](#stage-4--regularize)
- [Stage 5 — Tune](#stage-5--tune)
- [Stage 6 — Squeeze](#stage-6--squeeze)
- [Conclusion](#conclusion)
- [Map to the checklist](#map-to-the-checklist)

## Two root causes

1. **Neural network training is a leaky abstraction.** A 30-line example in a library looks
   plug-and-play. The abstraction leaks:
   - Backprop and SGD do not make a network work on their own.
   - BatchNorm does not make convergence faster on its own.
   - An RNN does not make text plug-and-play.
   - A problem that you can state as RL does not have to use RL.

   Away from a standard task such as ImageNet classification, the hidden complexity appears. If
   you apply a method that you do not understand, you probably fail.

2. **Neural network training fails silently.** Traditional code raises an exception on a wrong
   config: an int for a string, a wrong argument count, a failed import, an absent key, two lists
   of unequal length. A unit test catches most of those. A misconfigured network still trains
   with correct syntax, and the performance degrades quietly. The error surface is large,
   logical rather than syntactic, and very hard to unit test. That is the root of the silence.
   Four typical silent defects:
   - A left-right flip augmentation that does not flip the label. The network still works,
     because it learns to detect a flipped image and to flip the prediction back.
   - An off-by-one in an autoregressive model. The target becomes part of the input.
   - You intend to clip the gradient, but you clip the loss. Outlier samples then stay ignored.
   - You initialize weights from a pretrained checkpoint, but you do not use its original mean.

**The countermeasure sets the tone of the whole recipe.** Build from simple to complex. Stay
thorough, defensive, and paranoid. Visualize almost everything that you can visualize. Suffering
is a natural part of neural network training, but these habits reduce it. Karpathy names patience
and attention to detail as the qualities that correlate most with success.

## Three pillars of the recipe

The recipe takes the two root causes very seriously. It rests on three pillars.

1. **Build from simple to complex.**
2. **State a concrete hypothesis before each addition.** Predict what happens. Then verify the
   prediction with an experiment, or investigate until you find the defect. Do not add a small
   step and wait to see what breaks.
3. **Never introduce a large amount of unverified complexity at once.** A defect that you bury
   under unverified complexity costs a long search, and you may never find it.

> An analogy makes the point: write training code as you train a network. Use a very small
> learning rate. Guess one small step. Evaluate on the whole test set after each iteration. Slow
> and steady. Trade time for clarity.

---

## Stage 1 — Become one with the data

**Why.** The model mirrors the data distribution. A bias that hides in the data from the start —
label noise, class imbalance, duplicates, corrupt samples, a leaked feature — transfers to the
model, and detection is very hard later.

**How**

- Scan thousands of examples for hours before you touch the model code. Look at the
  distribution, the patterns, the class balance, the label quality, and the outliers.
- Write throwaway scripts that search, filter, sort, and visualize the data. Inspect the samples
  of one class. Find the duplicates. Find the corrupt samples: an unreadable or truncated image,
  a bad frame, an empty file. Find the corrupt and the mismatched labels. Find an abnormal length
  or size. Confirm that each label matches its input.
- Visualize the distribution and the outliers along every axis: label type, annotation size,
  annotation count, length. An outlier almost always exposes a defect in the data or in the
  preprocessing. It is the cheapest defect probe that you have.
- Treat your own manual procedure as an architecture clue. It tells you what architecture and
  what preprocessing the data asks for. Ask these questions:
  - Are local features enough, or do you need the global context?
  - How large is the variation, and what form does it take?
  - Which variation is a spurious signal that preprocessing can remove?
  - Does the spatial position matter, or can average pooling discard it?
  - How much does fine detail matter? How far can you downsample?
  - How noisy are the labels?
- The network is a compressed version of the dataset. After training, look at its predictions and
  its mispredictions. You can usually trace each one back to a pattern in the data. A prediction
  that clearly disagrees with what you saw in the data indicates a defect. This makes data
  inspection a loop that runs before and after training.
- Build an intuition for a reasonable prediction and for a forgivable error. That intuition
  becomes your reference when you judge a metric later.

---

## Stage 2 — Skeleton and dumb baselines

**Why.** Connect training to evaluation through the simplest credible path first. This gives you
a baseline that you can trust. Pick a model that you cannot get wrong, such as a linear
classifier or a tiny ConvNet. Every item below is a cheap check that blocks a whole class of
silent defects.

**How, tip by tip**

- **Fix the seed.** Set it for torch, numpy, python, and cuda. The purpose is a reproducible run
  and an attributable change. The purpose is not to pick a lucky seed.
- **Simplify first.** Turn off augmentation. Turn off every fancy trick. Run the plain model end
  to end. Add the complexity one item at a time later.
- **Evaluate with full significant digits.** Evaluate on the whole test set. Do not estimate from
  one batch and then smooth the curve in TensorBoard. The noise hides the real trend. You want
  correctness, and you trade time for clarity.
- **Verify the loss at init.** The theoretical prior must match. Uniform `n`-class softmax cross
  entropy starts near `-log(1/n) = log(n)`. The same derivation gives the default for regression:
  L2 or MSE starts near the label variance. Huber has two regimes. For a small residual it
  degrades to MSE, so it also starts near the label variance. For a large residual it grows
  linearly with `δ`. A mismatch points at the initialization or at the final layer.
- **Init well.** Set the final-layer bias to a reasonable prior. For regression with a target mean
  of 50, set that bias to 50. For imbalanced classification at 1 positive to 10 negative, set the
  logit bias so that the first prediction gives probability 0.1, which is the scale of
  `log(pos/neg)`. Otherwise the first hundreds of steps only unlearn a wrong bias. You waste the
  loss curve, and a hockey stick can appear at the start.
- **Add a human baseline.** Track a metric that a human can read and check, such as accuracy.
  Measure your own human accuracy as the target ceiling. As an alternative, label the test set
  twice. Treat one copy as the prediction and the other copy as the ground truth. The agreement
  estimates the human level.
- **Add an input-independent baseline.** Zero the inputs, or shuffle them, and train again. If the
  loss still falls near the value of the real run, the model does not use its input. The
  information leaks in from somewhere else, or the model memorizes the labels. A healthy model is
  clearly worse without its input.
- **Overfit one batch.** Drive the loss near zero on 2 to N samples. This is the watershed. If the
  model overfits, the forward path, the backward path, the optimizer, and the loss are sound, and
  the problem is in the data, the regularization, or the generalization. If it does not, the path
  itself holds a defect: check train and eval mode, `zero_grad`, the logits contract, and label
  alignment. Plot the labels and the predictions in one figure. Confirm that they align point by
  point at the minimum loss. A misalignment means a defect remains. Do not enter the next stage.
- **Verify that more capacity lowers the training loss.** Enlarge the model, or remove a little
  regularization. The training loss must go lower. If it does not, the run does not use the
  capacity that it has.
- **Visualize at the last seam.** Print or plot `x` and `y` in denormalized form on the line
  directly above `y_hat = model(x)`, or above `sess.run` in TensorFlow. This line is the only
  source of truth. It catches the defect that appears at the last moment: the dataset is correct,
  but collate, a transform, or the copy to the GPU corrupts the batch.
- **Visualize the prediction dynamics.** Fix one batch of test samples. Watch how the predictions
  evolve across the whole run. Heavy jitter that swings back and forth indicates instability, and
  the learning rate is usually too large. Very slow convergence indicates a learning rate that is
  too small, or a bad initialization.
- **Map the dependencies with backprop.** Build a scalar in which only the loss of sample `i` is
  nonzero. Call backward. Confirm that only the input of sample `i` carries a nonzero gradient.
  Any gradient outside that boundary means that information crosses between samples, which a
  wrong `view` or `reshape` often causes. The same probe verifies an autoregressive model.
  Differentiate the output at step `t`. Confirm that the gradient lands only on the inputs 1 to
  `t-1`, and stays zero from `t` to `T`. That result proves causality: no future information
  leaks in. More generally, the gradient tells you what depends on what, so it is a strong
  debug tool.
- **Generalize from a special case.** Hardcode one small concrete case until it is correct.
  Confirm that it runs correctly. Then generalize it step by step into the real implementation.
  This applies to vectorized code above all. Write the full loop version first. Then replace one
  loop at a time, and compare the result after each replacement.

---

## Stage 3 — Overfit

**Why.** Prove first that the model has the capacity to fit the training set, that is, to reach a
very low training loss. Handle generalization after that. This step separates a capacity problem
from a generalization problem. If no model of any capacity lowers the training loss, that result
is itself a defect or a config error, by the same logic as the one-batch overfit.

**How**

- **Do not be a hero.** Find the most relevant paper. Copy the simplest architecture that it
  reports, and reproduce that first. For image classification, run ResNet-50 first. Make a custom
  change only after the copy works. A self-designed architecture is a debug pit later.
- **Adam is the safe choice.** Use Adam early. A learning rate near `3e-4` is a solid start,
  because Adam is not very sensitive to it. Note: for a ConvNet, a well-tuned SGD almost always
  beats Adam a little, but its optimal learning rate band is much narrower and problem-specific.
  So use Adam early, and consider SGD later. For an RNN or another sequence model, Adam is more
  common. In every case, do not be a hero at the start. Take the optimizer from the most relevant
  paper.
- **Add one thing at a time.** With several input signals, modules, or data sources, connect one
  and verify it, then connect the next. Do not connect them all at once. Complexity has other
  axes too. For example, feed small images first, then raise the size step by step to the target
  resolution.
- **Do not trust a learning rate decay from another domain.** A decay usually triggers on the
  epoch number, and the number of steps in one epoch depends on the dataset size. The ImageNet
  default divides the learning rate by 10 at epoch 30. Copied to a smaller dataset, that schedule
  drives the learning rate to 0 too early, and the run stalls before the model learns. Karpathy's
  own practice: turn the decay off completely, hold the learning rate constant, and tune it last.

---

## Stage 4 — Regularize

**Why.** The model can overfit now. Trade a little training fit for validation performance.

**How, in order of value**

1. **Get more real data.** This is the most effective option, and it comes first. More real data
   is almost the only method that improves performance monotonically without a limit. Do not
   spend your time to squeeze a small dataset. An ensemble also improves monotonically, but the
   return stops after about 5 models.
2. **Augment the data.** This expands the set half-synthetically. Use a more aggressive
   augmentation if you need one.
3. **Use creative augmentation.** If half-synthetic data is not enough, fully synthetic data can
   still help: domain randomization, simulation, insertion of simulated data into a real scene,
   even a GAN.
4. **Pretrain.** A pretrained network rarely hurts, even when you already have enough data.
5. **Stay with supervised learning.** Do not expect too much from unsupervised pretraining. In
   modern computer vision, no version of it reports a strong result so far. NLP is the exception:
   BERT and similar models do well there, perhaps because text is more deliberate and carries a
   higher signal-to-noise ratio.
6. **Reduce the input dimensions.** Drop a feature that probably carries only noise, that is, a
   spurious signal. On a small dataset, every spurious input is one more chance to overfit. If
   low-level detail does not matter, feed a smaller image.
7. **Reduce the model size.** Use a domain constraint to cut the capacity directly. For example,
   replace the top fully connected layer with average pooling, which removes many parameters.
8. **Reduce the batch size.** A smaller batch regularizes a little on its own. Its empirical mean
   and standard deviation approximate the full statistics more coarsely. The scale and the shift
   of BatchNorm then perturb that batch more, which acts as stronger regularization.
9. **Add dropout.** For a ConvNet, use `dropout2d`, that is, spatial dropout. Use dropout
   sparingly, because dropout and BatchNorm do not combine well.
10. **Raise the weight decay.**
11. **Stop early.** Watch the validation loss and stop just before the model overfits.
12. **Try a larger model again.** Keep this last, and use it only together with early stopping. A
    larger model overfits more in the end, but its performance at the early-stopped point is
    often better than the performance of a small model.

**Final check.** Visualize the first-layer weights. They must show reasonable edges. A filter that
looks like noise means a defect somewhere. Then check the internal activations for an odd
artifact. Both are cheap probes on the health of the network.

---

## Stage 5 — Tune

**Why.** Spend compute on a hyperparameter search only after the rest of the pipeline is stable.

**How**

- **Prefer a random search over a grid search.** The network is far more sensitive to some
  hyperparameters than to others. Under a fixed trial budget, a grid wastes repeated samples on
  the dimensions that do not matter. If parameter `a` matters and parameter `b` has almost no
  effect, a random search gives `a` many more distinct values, so it covers `a` more densely. A
  grid retries the same few points.
- **Treat Bayesian tools with care.** Several fancy hyperparameter tools exist, and some of
  Karpathy's friends report success with them. His own experience is different: the
  state-of-the-art method to explore a broad model and hyperparameter space is manual work. The
  blog jokes that you use an intern for it. Do not treat these tools as a silver bullet.

---

## Stage 6 — Squeeze

**Why.** After you find a good configuration, two low-risk free lunches remain.

**How**

- **Ensemble the models.** An ensemble gives about 2 percent almost every time. If compute is
  short, distill the ensemble back into one model. Karpathy calls that signal dark knowledge.
- **Train for longer.** People stop the run too early. A network can train for an unintuitive
  length of time and still improve. Do not stop while the curve still falls slowly. Karpathy
  reports that he left one model to train over a winter break, and it was state of the art in
  January.

---

## Conclusion

At the end of the six stages you hold every ingredient of success:
- A deep understanding of the technology, the data, and the problem.
- A training and evaluation infrastructure that you built and that you trust.
- An exploration of stronger models, in which each added complexity follows a prediction.

From here, read many papers, run many experiments, and go for the state of the art.

## Map to the checklist

The entries below are the numbered sections of [checklist.md](checklist.md). Read the entry when
the matching gate stays shut.

| Recipe item | Checklist entry to read |
|---|---|
| Stage 2 — overfit one batch | Entry 1, overfit one batch first — the master switch on the whole path |
| Stage 2 — skeleton and path | Entry 2, train and eval mode; entry 3, `zero_grad`; entry 4, the logits contract |
| Stage 2 — backprop dependency probe and input visualization | Entry 6, `view` used as `permute` — the usual source of a cross-sample leak; entry 10, normalization leak |
| Stage 2 — fixed seed | Entry 11, random seed and reproducibility |
| Stage 3 — learning rate, Adam, no copied decay | Entry 9, warmup, scheduler, and learning rate scale |
| Stage 4 — regularize | Entry 8, loss reduction; entry 14, weight decay scope |
