# Fourteen Silent Failure Modes

Each entry has the same four parts: **Symptom**, **Cause**, **Check**, **Repair**. The examples use
PyTorch. The reasoning holds for any framework.

Read [SKILL.md](../SKILL.md) first. Each entry names the Stage 2 gate that it sits behind. A gate
that stays shut therefore points you at a short list of entries.

## Contents

Entries 1 to 6 come from the original Karpathy thread. They decide whether the pipeline is correct.

- [1. No one-batch overfit check](#1-no-one-batch-overfit-check)
- [2. Wrong train mode and eval mode](#2-wrong-train-mode-and-eval-mode)
- [3. Missing zero_grad call](#3-missing-zero_grad-call)
- [4. Confusion of logits and probabilities](#4-confusion-of-logits-and-probabilities)
- [5. Bias in the layer before BatchNorm](#5-bias-in-the-layer-before-batchnorm)
- [6. Use of view in place of permute](#6-use-of-view-in-place-of-permute)
- [Diagnostic route for entries 1 to 6](#diagnostic-route-for-entries-1-to-6)

[Entries 7 to 14](#entries-7-to-14-the-training-strategy) are not in that thread. They are as
frequent, and most of them are as silent. They decide how well a run trains and whether it
reproduces.

- [7. No shuffle in the train DataLoader](#7-no-shuffle-in-the-train-dataloader)
- [8. Wrong loss reduction](#8-wrong-loss-reduction)
- [9. No warmup and no scheduler](#9-no-warmup-and-no-scheduler)
- [10. Normalization statistics leak](#10-normalization-statistics-leak)
- [11. No fixed random seed](#11-no-fixed-random-seed)
- [12. Loss accumulation that holds the graph](#12-loss-accumulation-that-holds-the-graph)
- [13. Wrong CrossEntropyLoss target](#13-wrong-crossentropyloss-target)
- [14. Weight decay on bias and norm parameters](#14-weight-decay-on-bias-and-norm-parameters)
- [Diagnostic route for entries 7 to 14](#diagnostic-route-for-entries-7-to-14)

---

## 1. No one-batch overfit check

This entry sits behind Stage 2 gate 5: one batch of 2 to 8 examples overfits to near zero.

**Symptom**

- The loss stops at a value and does not move. You cannot tell whether the data is wrong, the model
  is too small, the learning rate is wrong, or the code holds a defect.
- You tune hyperparameters for hours without a hypothesis.

**Cause**

- You started on the full dataset with regularization and augmentation. Too many variables move at
  once. You lost the most basic verdict of all: is the pipeline correct?

**Check**

- Take one fixed small batch of 2 to 8 examples. Turn off dropout, augmentation, and weight decay.
- Train on that same batch for several hundred steps.
- Watch whether the loss falls to near zero. A classifier must reach a near-zero train loss and
  100 percent train accuracy.

**Repair**

- **The batch overfits.** The forward pass, the backward pass, the optimizer, and the loss are
  correct. Look at the data scale, the regularization, the generalization, and the learning rate
  schedule. Continue with entries 7 to 14.
- **The batch does not overfit.** The pipeline holds a defect. Read entries 2, 3, and 4 next. Look
  for a missing `zero_grad`, a wrong mode, a wrong loss contract, an offset label, or a parameter
  that receives no gradient.
- Also check the loss at init, which is Stage 2 gate 1. Uniform `n`-class cross entropy starts near
  `log(n)`. Another magnitude points at the logit scale, the initialization, or the labels.

```python
# Take one batch, feed it again and again. The loss must fall.
xb, yb = next(iter(loader))
model.train()
for step in range(500):
    optimizer.zero_grad()
    loss = criterion(model(xb), yb)
    loss.backward()
    optimizer.step()
    if step % 50 == 0:
        print(step, loss.item())   # expect a steady approach to zero
```

---

## 2. Wrong train mode and eval mode

This entry sits behind Stage 2 gate 5. A wrong mode also breaks the reproduction of any run.

**Symptom**

- The validation metric is much worse than the training metric.
- The validation result or the inference result changes on every run.
- The BatchNorm statistics jump on small evaluation batches. Production inference disagrees with
  training.

**Cause**

- `Dropout` and `BatchNorm` behave differently in the two modes.
  - Train mode: Dropout zeroes units at random. BatchNorm uses the statistics of the current batch
    and updates the running statistics.
  - Eval mode: Dropout passes every unit. BatchNorm uses the stored running mean and variance.
- A model that stays in train mode during validation still drops units and still uses batch
  statistics. The result is random and unstable.
- A model that stays in eval mode during training loses its regularization. BatchNorm then never
  updates its statistics.

**Check**

- Confirm that `model.train()` runs before the training section of each epoch.
- Confirm that `model.eval()` runs before each validation, test, or inference section.
- Confirm that inference also runs under `with torch.no_grad():`. It saves memory and states the
  intent.

**Repair**

```python
# Training section
model.train()
for xb, yb in train_loader:
    ...

# Validation or inference section
model.eval()
with torch.no_grad():
    for xb, yb in val_loader:
        ...
```

- The two calls must appear as a pair. Put each call at the top of `train_one_epoch()` and of
  `evaluate()`. No section can then miss its mode.

---

## 3. Missing zero_grad call

This entry sits behind Stage 2 gate 5: one batch of 2 to 8 examples overfits to near zero.

**Symptom**

- The loss does not fall, or it oscillates and diverges.
- The run gets slower, and memory grows slowly with each step.

**Cause**

- `.backward()` adds gradients into `.grad`. It does not overwrite them. Without a reset before
  each step, the current gradient stacks on every earlier gradient. Then `optimizer.step()` uses a
  wrong sum, and the update direction is wrong.

**Check**

- Confirm that `optimizer.zero_grad()` appears before `backward()` in every step.
- Confirm the order: `zero_grad()`, forward, `loss.backward()`, `optimizer.step()`.

**Repair**

```python
for xb, yb in train_loader:
    optimizer.zero_grad()          # 1. clear the gradients (or zero_grad(set_to_none=True))
    out = model(xb)                # 2. forward
    loss = criterion(out, yb)
    loss.backward()                # 3. backward, which adds into .grad
    optimizer.step()               # 4. update
```

- **Exception: gradient accumulation.** With deliberate accumulation, call `step()` and
  `zero_grad()` once every N micro-steps. That sum is intended, so it is not a defect. The test is
  whether you designed it.

---

## 4. Confusion of logits and probabilities

This entry sits behind Stage 2 gate 1: the loss at init matches the prior. A second softmax moves
the loss at init away from `log(n)`.

**Symptom**

- The classification loss is high and does not fall. The run moves, but the numbers are unstable
  and reach NaN.
- The probabilities at inference do not sum to 1, or argmax returns a strange class.

**Cause**

- Each loss states its own input contract. The most common defect is an extra softmax or sigmoid on
  the model output.
  - `nn.CrossEntropyLoss` is `LogSoftmax` plus `NLLLoss`. It already holds the softmax, so feed it
    raw logits. A softmax before it applies the operation twice and distorts the loss.
  - `nn.BCEWithLogitsLoss` already holds the sigmoid. Feed it logits and add no sigmoid of your own.
  - `nn.NLLLoss` takes log probabilities, so put `log_softmax` in front of it.
  - `nn.BCELoss` takes probabilities in `[0, 1]`, so put a sigmoid in front of it. It is less
    stable than `nn.BCEWithLogitsLoss`.

**Check**

- Read the last layer of the model. Look for a `Softmax` or a `Sigmoid` that you added.
- Read the loss class. Decide whether it expects logits or probabilities.
- The operation must appear exactly once: never zero times and never twice.
- Decide separately at inference whether you need a softmax. Most code needs only
  `argmax(logits)`, because a monotonic softmax does not move the argmax.

**Repair**

| Task | Loss | Model output | Do not |
|------|------|--------------|--------|
| Multi-class | `CrossEntropyLoss` | raw logits | Do not add a softmax to the output layer. |
| Binary or multi-label | `BCEWithLogitsLoss` | raw logits | Do not add a sigmoid of your own. |
| Already `log_softmax` | `NLLLoss` | log probabilities | — |

```python
# Correct: the model returns logits, and the loss applies the softmax.
logits = model(xb)                 # no softmax here
loss = nn.CrossEntropyLoss()(logits, yb)

# Probabilities at inference, only when you need them
probs = logits.softmax(dim=-1)
pred  = logits.argmax(dim=-1)      # argmax works directly on the logits
```

---

## 5. Bias in the layer before BatchNorm

No Stage 2 gate covers this entry. The run still trains.

**Symptom**

- The defect is not fatal, and the network trains as usual. The parameters hold redundancy, and the
  code shows an incomplete model of BatchNorm.

**Cause**

- BatchNorm computes `(x - mean) / std`. The subtraction of the mean removes the bias of the
  previous layer, because a bias is a constant offset. That bias therefore never has an effect.
- A `Conv` or `Linear` layer directly before a `BatchNorm` holds a redundant `bias`. It costs
  memory and gradient computation. The affine parameters of BatchNorm, which are gamma and beta,
  already give a learnable scale and offset.

**Check**

- Find each `Conv2d(...) -> BatchNorm2d(...)` or `Linear(...) -> BatchNorm1d(...)` pair. Confirm
  that the first layer sets `bias=False`.

**Repair**

```python
# Turn the bias off in the layer before BatchNorm.
nn.Sequential(
    nn.Conv2d(3, 64, 3, padding=1, bias=False),   # <- bias=False
    nn.BatchNorm2d(64),                           # beta supplies the offset
    nn.ReLU(inplace=True),
)
```

- A layer with no BatchNorm after it keeps its bias.

---

## 6. Use of view in place of permute

This entry sits behind Stage 2 gate 6: the tensors are correct at the last seam.

**Symptom**

- The tensor shape looks correct, but the contents are scrambled. The accuracy collapses, or it
  stays far below the expected value.
- PyTorch raises `view size is not compatible with input tensor's size and stride`, or it asks for
  `.contiguous()`.

**Cause**

- The two operations have different meanings.
  - `permute` and `transpose` exchange the order of the axes. The data stays in place, and only the
    stride and the view change. Use `permute` for `(N, C, H, W) -> (N, H, W, C)`.
  - `view` and `reshape` reinterpret the memory layout in row-major order. They do not exchange the
    semantic axes. They cut the same contiguous memory into a new shape.
- A `view` that stands for an axis exchange packs the elements into the new shape in memory order.
  The result is not a transpose, and the meaning is lost.
- A `permute` that stands for a merge or a split of dimensions gives a wrong rank or raises an
  error.
- After `permute` or `transpose` the tensor is not contiguous, so a direct `view` fails. Call
  `.contiguous()` first, or use `reshape`, which copies when it must.

**Check**

- Ask one question: do I want a new axis order, or a new memory shape?
  - New axis order, such as a transpose: use `permute` or `transpose`.
  - A merge, a split, or a flatten such as `(N, C, H, W) -> (N, C*H*W)`: use `view` or `reshape`.
- Print a few elements after the operation. Confirm the contents, not only the shape.

**Repair**

```python
x = torch.randn(2, 3, 4, 5)        # (N, C, H, W)

# Axis order: NCHW -> NHWC needs permute, which keeps the meaning.
x_nhwc = x.permute(0, 2, 3, 1)     # shape (2, 4, 5, 3)

# The result is not contiguous. Call contiguous before view, or use reshape.
flat = x_nhwc.contiguous().view(2, -1)   # or x_nhwc.reshape(2, -1)

# Flatten a feature map: merge C, H, and W with view or reshape, not with permute.
feat = x.reshape(2, -1)            # (2, 60), row-major
```

Rule of thumb:

- For a transpose or an axis exchange, use `permute` or `transpose`.
- For a new shape, a merge, a split, or a flatten, use `reshape`. Use `view` only when the tensor
  is contiguous.

---

## Diagnostic route for entries 1 to 6

```
The run does not converge.
 └─ Overfit one batch first.                                   (entry 1)
     ├─ It overfits         -> the pipeline is correct. Check the data, the
     │                         regularization, the learning rate, the schedule.
     └─ It does not overfit -> check the pipeline:
         ├─ Do train() and eval() run in the right sections?    (entry 2)
         ├─ Does zero_grad() run in every step?                 (entry 3)
         └─ Does the loss take logits or probabilities?         (entry 4)

The contents are scrambled after a shape operation.
 └─ Is view correct here, or does it need permute? contiguous?  (entry 6)

Cleanup:
 └─ Does the layer before BatchNorm set bias=False?             (entry 5)
```

---

## Entries 7 to 14: the training strategy

The next eight entries are not in the original thread. They are as frequent in practice, and most
of them are as silent. They belong to the training strategy. They do not decide whether the
pipeline is correct. They decide how well the run trains, and whether it reproduces. Walk them
after entries 1 to 6 hold.

---

## 7. No shuffle in the train DataLoader

No Stage 2 gate covers this entry. It belongs to Stage 3, where you overfit the full training set.

**Symptom**

- The loss shows a fixed periodic wobble inside each epoch. Convergence is slow, or it stops.
- Data sorted by class or by time breaks the run at once, because one batch then holds one class.

**Cause**

- SGD assumes that each batch is an approximate i.i.d. sample of the distribution. Without shuffle
  the batches correlate, the gradient is biased, and every epoch sees the same batch order. That
  fixed order adds a false period.
- With data sorted by label, one batch is extremely imbalanced. The BatchNorm statistics and the
  gradient direction both move away from the truth.

**Check**

- Set `shuffle=True` on the train `DataLoader`, or pass a random `Sampler`.
- Set `shuffle=False` on the validation loader and the test loader. Evaluation does not need
  shuffle, and it must reproduce.
- Check whether the data was already sorted by label or by time on disk.

**Repair**

```python
train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)
val_loader   = DataLoader(val_ds,   batch_size=64, shuffle=False)
```

- Time series and grouped data need care. Shuffle inside a legal group. A global shuffle leaks
  across time.

---

## 8. Wrong loss reduction

This entry sits behind Stage 2 gate 1: the loss at init matches the prior. A `sum` reduction
multiplies the loss at init by the batch size.

**Symptom**

- A new batch size forces a new learning rate. The gradient magnitude follows the batch size.
- Several task losses that you add together have unbalanced scales. A hand-written sum forgets the
  division by the sample count.

**Cause**

- `reduction='sum'` and `reduction='mean'` differ by a factor of the batch size. The gradient of
  the sum is exactly `batch_size` times the gradient of the mean. Verify it by hand: `L_sum = Σ Lᵢ`
  and `L_mean = L_sum / N`, so `grad(sum) = N · grad(mean)`.
- With `sum`, the batch size scales the effective learning rate. A new batch size then diverges or
  stalls. Mixed reductions across several losses distort their weights silently.

**Check**

- Read the `reduction` of each loss. The default is `'mean'`. Keep the default.
- With a hand-written loss, confirm the division by the batch size.
- For variable-length sequences, state whether you average over tokens or over samples. Mask the
  padding positions and keep them out of the denominator.

**Repair**

```python
criterion = nn.CrossEntropyLoss()          # reduction='mean' by default

# Variable-length sequences: average over the valid tokens and mask the padding.
loss = (per_token_loss * mask).sum() / mask.sum()

# Gradient accumulation: divide each micro-batch loss by the step count first.
loss = criterion(out, yb) / accum_steps
```

---

## 9. No warmup and no scheduler

No Stage 2 gate covers this entry. It belongs to Stage 3, where the recipe starts at Adam `3e-4`
with the decay off.

**Symptom**

- The run diverges, or the loss reaches NaN in the first few hundred steps. Adam with a large batch
  and a Transformer shows this most often.
- The loss falls a little and then reaches a plateau, and the late accuracy never arrives.

**Cause**

- Early in a run the second-moment estimate of Adam is still unstable, so the step size varies a
  lot. A large batch or a large model also adds gradient noise early. The target learning rate then
  throws the run off course. A warmup raises the rate linearly from 0 to the target and holds the
  early steps steady. A cosine decay or a step decay at the end approaches the optimum.
- The learning rate is the most important hyperparameter. An error of one order of magnitude wastes
  the run.

**Check**

- Confirm that a Transformer run or a large-batch run has a warmup. Several hundred to several
  thousand steps is normal.
- Confirm that a scheduler is attached. Confirm that a learning rate range test found the correct
  magnitude.

**Repair**

- Use the `warmup_cosine` factor in
  [`extra_pitfalls_before_after.py`](../sample_codes/common-patterns/extra_pitfalls_before_after.py)
  as the `lr_lambda` of `torch.optim.lr_scheduler.LambdaLR`. It rises linearly to the target over
  the warmup steps, and then follows a cosine down to zero.
- Call `scheduler.step()` after each `optimizer.step()`.
- HuggingFace offers `get_linear_schedule_with_warmup` and `get_cosine_schedule_with_warmup`
  directly.

---

## 10. Normalization statistics leak

This entry sits behind Stage 2 gate 6: the tensors are correct at the last seam. Print the batch in
denormalized form to expose the defect. Gate 4 catches the related case, where a label leaks into
the input.

**Symptom**

- The validation metric or the test metric is too good, because information leaked.
- Production inference is much worse than offline evaluation, because inference skipped the
  normalization or used the wrong statistics.

**Cause**

- The code computed the mean and the standard deviation over the whole dataset, including
  validation and test. Information leaks from the test set into training, and the metric rises
  falsely.
- Training normalized the input, and inference forgot to reuse the same train statistics. The input
  distribution then shifts.
- The code recomputed the statistics separately on validation or on test. That is both a leak and
  an inconsistency.

**Check**

- Fit the mean and the standard deviation on the training set alone. Reuse that one set everywhere:
  validation, test, and production inference.
- Confirm that the parameters of `transforms.Normalize` for images, or of a tabular scaler, are
  identical in training and in inference.

**Repair**

```python
mu = train_x.mean(0, keepdim=True)      # fit on the training set alone
sd = train_x.std(0, keepdim=True) + 1e-8
# Save mu and sd. Reuse them for train, validation, test, and production.
norm = lambda x: (x - mu) / sd
```

---

## 11. No fixed random seed

This entry sits behind the Stage 2 gate as a whole: all seven gates hold under one reproduction
command. Stage 2 also asks you to fix the seed before you start.

**Symptom**

- The same code gives a different result on every run. You cannot tell whether a metric moved
  because of your change or because of noise. The runs do not compare.

**Cause**

- torch, numpy, python `random`, and CUDA each hold an independent RNG. The DataLoader workers and
  the non-deterministic cudnn algorithms add more randomness.

**Repair**

```python
def seed_everything(seed=42):
    """Fix the torch, numpy, python, and CUDA seeds so that a run reproduces."""
    import os, random
    import numpy as np
    import torch
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    # Turn these on for a strict reproduction. They cost speed.
    # torch.backends.cudnn.deterministic = True
    # torch.backends.cudnn.benchmark = False
```

- A strict reproduction with several DataLoader workers also needs `worker_init_fn` and an explicit
  `generator`.
- A fixed seed gives you a controlled comparison. Do not search for a seed that flatters the
  result. That is self-deception.

---

## 12. Loss accumulation that holds the graph

No Stage 2 gate covers this entry. It appears in the long runs of Stage 3 and Stage 4.

**Symptom**

- Memory grows with each step and each epoch until the run reaches OOM. The run also gets slower.

**Cause**

- `total_loss += loss` adds a tensor that still carries its graph. Every batch graph stays alive, so
  memory accumulates.

**Check and repair**

```python
running_loss = 0.0
for xb, yb in train_loader:
    ...
    loss = criterion(out, yb)
    loss.backward(); optimizer.step()
    running_loss += loss.item() * xb.size(0)   # a scalar, weighted by the sample count (entry 8)
epoch_loss = running_loss / len(train_loader.dataset)
```

- Call `.item()` or `.detach()` for every metric that you record, such as the loss and the accuracy.
- Never add a tensor that still carries a graph.

---

## 13. Wrong CrossEntropyLoss target

This entry sits behind Stage 2 gate 1: the loss at init matches the prior. A wrong target contract
moves the loss at init away from `log(n)`.

**Symptom**

- PyTorch raises a dtype error or a shape error. That case is not silent.
- The silent case is a one-hot target, a float probability target, or a target with one extra
  dimension. The run proceeds and learns the wrong thing.

**Cause**

- `nn.CrossEntropyLoss` expects class indices of dtype `long` with shape `(N,)`. Image segmentation
  uses shape `(N, H, W)`. It does not expect a one-hot target.
- `nn.BCEWithLogitsLoss` expects `float` values with shape `(N, C)`. A swap of the two losses gives
  a wrong meaning or a wrong rank.

**Check and repair**

```python
# Multi-class: the target is a long class index of shape (N,).
yb = yb.long()                       # do not build a one-hot target
loss = nn.CrossEntropyLoss()(logits, yb)     # the logits have shape (N, C)

# Multi-label or binary: the target is a float 0 or 1 of shape (N, C).
loss = nn.BCEWithLogitsLoss()(logits, yb.float())
```

---

## 14. Weight decay on bias and norm parameters

No Stage 2 gate covers this entry. It belongs to Stage 4, where you regularize.

**Symptom**

- The defect is not fatal, but the regularization is slightly wrong. The gamma and beta of the norm
  layers and the bias of each layer decay by mistake, and performance drops a little. Like entry 5,
  it shows an incomplete model of the components.

**Cause**

- Weight decay exists to penalize the magnitude of the weight matrices. A decay on a 1-D bias or on
  a norm affine parameter has no theoretical basis. Most state-of-the-art recipes put these
  parameters in a separate group with `weight_decay=0`.

**Repair**

- Call `split_param_groups` from
  [`extra_pitfalls_before_after.py`](../sample_codes/common-patterns/extra_pitfalls_before_after.py).
  It returns two parameter groups. The weight matrices keep the decay. The bias and the 1-D norm
  parameters get `weight_decay=0`.

```python
optimizer = torch.optim.AdamW(split_param_groups(model), lr=3e-4)
```

---

## Diagnostic route for entries 7 to 14

```
One batch overfits and the pipeline is correct, but the run trains poorly
or does not reproduce. Check the training strategy:
 ├─ Does the train loader shuffle?                        (entry 7)
 ├─ Does the loss average over the samples?               (entry 8)
 ├─ Does the learning rate have a warmup and a scheduler? (entry 9)
 ├─ Do all stages reuse the train statistics?             (entry 10)
 ├─ Is the random seed fixed?                             (entry 11)
 ├─ Does each metric use .item() to free the graph?       (entry 12)
 ├─ Is the CrossEntropy target a long index?              (entry 13)
 └─ Does weight decay skip the bias and norm parameters?  (entry 14)
```
