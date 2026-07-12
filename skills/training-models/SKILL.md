---
name: training-models
description: Neural-network training discipline and silent-failure debugging. Use when loss stalls, accuracy is stuck, gradients explode or vanish, train/eval results disagree, inference is wrong, a one-batch overfit check fails, an existing loop needs review, or a new training pipeline needs staged setup. Chinese triggers include loss 不下降, acc 卡住, 梯度异常, 训练验证不一致, 推理错误, 检查训练循环, and 从零搭训练流程.
---

# Training Neural Networks Reliably

Silent failures are normal in neural-network training. Establish a minimal reproducible feedback loop,
then add data complexity, regularization, and model capacity one change at a time.

## Route

- **Existing failure**: freeze one symptom and reproduction command, then run the diagnostic loop.
- **Loop review**: audit modes, gradient lifecycle, output/loss contracts, and the smallest sanity check.
- **New pipeline**: follow the [six-stage recipe](references/karpathy-recipe.md), proving each stage
  before adding the next.

## Diagnostic loop

1. Fix the random seed; disable augmentation, dropout, and weight decay; record initial loss,
   training loss, and the primary metric under one command.
2. Check expected initial loss. Uniform `n`-class cross entropy should be near `log(n)`; otherwise
   inspect labels, initialization, final bias, logit scale, and the loss input contract.
3. Overfit 2–8 fixed examples until loss approaches zero, then compare predictions with labels.
4. Retrain with zeroed inputs. Similar performance points to leakage, index misalignment, or a model
   that ignores its inputs.
5. Localize the first failed contract using the [failure checklist](references/checklist.md), apply
   the smallest repair, and rerun the identical reproduction.

When small-batch overfit fails, check `train()`/`eval()`, `zero_grad()` → forward → `backward()` →
`step()`, logits-versus-probability loss contracts, tensor axis transforms, and label alignment first.

## Runnable checks

- [`sanity_check.py`](sample_codes/getting-started/sanity_check.py): initial loss and
  input-independent baselines.
- [`correct_training_loop.py`](sample_codes/getting-started/correct_training_loop.py): training and
  validation loop template.
- [`six_pitfalls_before_after.py`](sample_codes/common-patterns/six_pitfalls_before_after.py) and
  [`extra_pitfalls_before_after.py`](sample_codes/common-patterns/extra_pitfalls_before_after.py):
  broken/fixed examples.

## Completion

Report the reproduction command, applicable sanity-check results, defect evidence, repair, and
before/after comparison. Existing failures are complete only when the original reproduction passes
without weakened validation. New pipelines must also name the current recipe stage and the evidence
that permits entering the next one.
