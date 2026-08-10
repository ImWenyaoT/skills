"""Eight more defects, entries 7 to 14, each as a broken example and a repaired example.

This file backs checklist entries 7 to 14. Karpathy does not list these eight, but they
appear as often in real work, and most of them fail in the same silent way. Each
pitfall_N() function shows the defect and the repair, and returns the numbers that
separate the two. Run the file to see the evidence.

Requirement: torch. Run: python extra_pitfalls_before_after.py
"""

from __future__ import annotations

import math

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset


# ──────────────────────────────────────────────────────────────────────
# Entry 7: the train DataLoader misses shuffle=True
# ──────────────────────────────────────────────────────────────────────
def pitfall_7_shuffle():
    """Entry 7. Broken: the data sits in label order, and the loader does not shuffle it.

    One batch then holds one class alone. That batch pulls the gradient to one side, and
    it also poisons the BatchNorm statistics. Repair: set shuffle=True on the train
    loader, and shuffle=False on the validation loader and the test loader.

    Returns:
        A dict with the labels of the first batch in each variant.
    """
    x = torch.arange(8).float().unsqueeze(1)
    y = torch.tensor([0, 0, 0, 0, 1, 1, 1, 1])  # The labels sit in order on purpose.
    ds = TensorDataset(x, y)

    no_shuffle = DataLoader(ds, batch_size=4, shuffle=False)
    shuffled = DataLoader(ds, batch_size=4, shuffle=True)

    first_no = next(iter(no_shuffle))[1].tolist()  # Broken: one class alone.
    first_sh = next(iter(shuffled))[1].tolist()  # Repair: the classes mix.
    return {
        "no_shuffle_first_batch_labels": first_no,
        "shuffled_first_batch_labels": first_sh,
        "note": "A single-class batch bends the gradient and the BatchNorm statistics.",
    }


# ──────────────────────────────────────────────────────────────────────
# Entry 8: the loss does not average over the batch
# ──────────────────────────────────────────────────────────────────────
def pitfall_8_loss_reduction():
    """Entry 8. Broken: the loss uses reduction='sum', or the code adds the losses without a divide.

    The size of the gradient then scales with the batch size, so a new batch size makes
    the run diverge. Repair: use reduction='mean'. For a variable-length sequence, divide
    by the number of valid tokens.

    Returns:
        A dict with the batch size and the ratio between the two gradients.
    Note:
        The evidence: the gradient of the sum equals the gradient of the mean times the
        batch size.
    """
    torch.manual_seed(0)
    x = torch.randn(16, 4)
    t = torch.randn(16, 1)
    w = torch.randn(4, 1, requires_grad=True)
    se = (x @ w - t) ** 2

    g_mean = torch.autograd.grad(se.mean(), w, retain_graph=True)[0]
    g_sum = torch.autograd.grad(se.sum(), w)[0]
    ratio = (g_sum / g_mean).mean().item()  # This equals the batch size, 16.
    return {"batch_size": x.size(0), "grad_ratio_sum_over_mean": round(ratio, 3)}


# ──────────────────────────────────────────────────────────────────────
# Entry 9: the run has no warmup and no scheduler
# ──────────────────────────────────────────────────────────────────────
def pitfall_9_warmup():
    """Entry 9. Broken: a large batch or a Transformer starts at the target learning rate.

    The first few hundred steps then diverge, or they produce a NaN. Repair: raise the
    learning rate linearly to the target, then lower it along a cosine curve.

    Returns:
        A dict with the first ten learning rates of the schedule.
    """
    model = nn.Linear(4, 2)
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3)

    def warmup_cosine(step, warmup=5, total=20):
        """Return the learning rate factor for one step of the schedule.

        Args:
            step: The index of the current step.
            warmup: The number of warmup steps.
            total: The total number of steps.
        Returns:
            The factor as a float. It rises linearly, then it falls along a cosine curve.
        """
        if step < warmup:
            return step / max(1, warmup)
        progress = (step - warmup) / max(1, total - warmup)
        return 0.5 * (1.0 + math.cos(math.pi * progress))

    sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_lambda=warmup_cosine)
    lrs = []
    for _ in range(20):
        opt.zero_grad()
        model(torch.randn(2, 4)).sum().backward()
        opt.step()
        sched.step()  # Call the scheduler after the optimizer.
        lrs.append(round(opt.param_groups[0]["lr"], 6))
    return {
        "lr_curve_first10": lrs[:10],
        "note": "The first five steps rise, and the rest fall along a cosine curve.",
    }


# ──────────────────────────────────────────────────────────────────────
# Entry 10: the normalization statistics leak, or the inference skips them
# ──────────────────────────────────────────────────────────────────────
def pitfall_10_normalization():
    """Entry 10. Broken: the code fits mean and std on the train split and the test split together.

    The test split then leaks into the train statistics. A second version of the same
    defect skips the normalization at inference. Repair: fit mean and std on the train
    split alone. Save the two values, and apply them at every later stage.

    Returns:
        A dict that reports the correct fit, the effect of the leak, and the test mean.
    """
    torch.manual_seed(0)
    train_x = torch.randn(100, 3) * 5 + 2
    test_x = torch.randn(20, 3) * 5 + 2

    # Repair: fit on the train split, and apply the same values to the test split.
    mu = train_x.mean(0, keepdim=True)
    sd = train_x.std(0, keepdim=True) + 1e-8
    test_norm = (test_x - mu) / sd

    # Broken: the fit reads the test split too.
    mu_leak = torch.cat([train_x, test_x], 0).mean(0, keepdim=True)
    leaked = not torch.allclose(mu, mu_leak)
    return {
        "stats_fit_on_train_only": True,
        "leaking_changes_stats": bool(leaked),
        "test_norm_mean_approx0": round(test_norm.mean().item(), 3),
    }


# ──────────────────────────────────────────────────────────────────────
# Entry 11: the run fixes no seed, so nobody can reproduce it
# ──────────────────────────────────────────────────────────────────────
def pitfall_11_seed(seed=42):
    """Entry 11. Broken: the run fixes no seed, so every result differs.

    You cannot then attribute a change to your edit. Repair: fix the seed of torch, numpy,
    the standard library, and cuda together. Two runs with the same seed must agree.

    Args:
        seed: The seed to apply to every generator.
    Returns:
        A dict that reports whether the two draws agree.
    """

    def seed_everything(s):
        """Fix the seed of every random number generator that the run touches.

        Args:
            s: The seed value.
        Returns:
            None.
        """
        import random

        random.seed(s)
        torch.manual_seed(s)
        torch.cuda.manual_seed_all(s)
        try:
            import numpy as np

            np.random.seed(s)
        except ImportError:
            pass

    seed_everything(seed)
    a = torch.rand(3)
    seed_everything(seed)
    b = torch.rand(3)
    return {"reproducible": bool(torch.equal(a, b))}


# ──────────────────────────────────────────────────────────────────────
# Entry 12: the loop adds a loss tensor and holds the graph
# ──────────────────────────────────────────────────────────────────────
def pitfall_12_loss_accumulation():
    """Entry 12. Broken: the loop runs total_loss += loss, where loss is a tensor with a graph.

    The graph of every batch then stays in memory, and the run ends with an out-of-memory
    error on a GPU. Repair: add loss.item(), which is a plain float. Weight it by the
    number of samples, and divide at the end.

    Returns:
        A dict that reports the graph on the broken value and the type of the repaired value.
    """
    model = nn.Linear(4, 1)
    x, t = torch.randn(8, 4), torch.randn(8, 1)
    loss = ((model(x) - t) ** 2).mean()

    bad_accumulator = loss  # Broken: requires_grad is True, so the graph stays alive.
    good_accumulator = loss.item()  # Repair: a Python float, and no graph.
    return {
        "bad_has_grad_graph": bool(bad_accumulator.requires_grad),
        "good_is_python_float": isinstance(good_accumulator, float),
    }


# ──────────────────────────────────────────────────────────────────────
# Entry 13: the target of CrossEntropyLoss has the wrong dtype or shape
# ──────────────────────────────────────────────────────────────────────
def pitfall_13_target_dtype():
    """Entry 13. Broken: the code passes a one-hot target or a float target to CrossEntropyLoss.

    An old version raises an error. A current version reads the tensor as class
    probabilities, which is a different loss than you intend. Repair: for one label per
    sample, pass a long tensor of shape (N,) that holds class indices. For a multi-label
    task, pass a float tensor of shape (N, C) to BCEWithLogitsLoss.

    Returns:
        A dict that reports the target contract and the loss value.
    """
    logits = torch.randn(8, 3)
    y_idx = torch.randint(0, 3, (8,)).long()  # Repair: a (N,) long index tensor.
    ce = nn.CrossEntropyLoss()(logits, y_idx).item()

    is_valid_target = y_idx.dtype == torch.long and y_idx.dim() == 1
    return {"target_is_long_1d_index": bool(is_valid_target), "ce_loss": round(ce, 4)}


# ──────────────────────────────────────────────────────────────────────
# Entry 14: weight decay reaches the bias and the norm parameters
# ──────────────────────────────────────────────────────────────────────
def split_param_groups(model, weight_decay=1e-2):
    """Split the parameters into a group with weight decay and a group without it.

    Args:
        model: The nn.Module to split.
        weight_decay: The weight decay for the matrix parameters.
    Returns:
        A list of two param group dicts for an optimizer.
    Note:
        A bias and a 1-D norm parameter go into the second group. Weight decay pulls them
        toward zero for no benefit, and it shifts the output of the norm layer.
    """
    decay, no_decay = [], []
    for name, p in model.named_parameters():
        if not p.requires_grad:
            continue
        if p.ndim <= 1 or name.endswith(".bias"):  # A bias, a BatchNorm, or a LayerNorm.
            no_decay.append(p)
        else:
            decay.append(p)
    return [
        {"params": decay, "weight_decay": weight_decay},
        {"params": no_decay, "weight_decay": 0.0},
    ]


def pitfall_14_weight_decay():
    """Entry 14. Broken: one weight decay value reaches every parameter of the model.

    The bias and the norm parameters then decay too, which costs accuracy. Repair: build
    two param groups, and set weight_decay=0.0 on the group that holds them.

    Returns:
        A dict with the size of each group and the weight decay of the second group.
    """
    model = nn.Sequential(nn.Linear(4, 8), nn.BatchNorm1d(8), nn.Linear(8, 2))
    groups = split_param_groups(model, weight_decay=1e-2)
    opt = torch.optim.AdamW(groups, lr=3e-4)
    return {
        "num_decay_params": sum(p.numel() for p in groups[0]["params"]),
        "num_no_decay_params": sum(p.numel() for p in groups[1]["params"]),
        "no_decay_group_wd": opt.param_groups[1]["weight_decay"],
    }


if __name__ == "__main__":
    torch.manual_seed(0)
    print("entry 7  shuffle          :", pitfall_7_shuffle())
    print("entry 8  loss reduction   :", pitfall_8_loss_reduction())
    print("entry 9  warmup           :", pitfall_9_warmup())
    print("entry 10 normalization    :", pitfall_10_normalization())
    print("entry 11 seed             :", pitfall_11_seed())
    print("entry 12 loss accumulation:", pitfall_12_loss_accumulation())
    print("entry 13 target dtype     :", pitfall_13_target_dtype())
    print("entry 14 weight decay     :", pitfall_14_weight_decay())
