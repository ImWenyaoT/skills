"""Six classic defects, each as a broken example and a repaired example.

This file backs checklist entries 1 to 6. Each pitfall_N() function shows the broken code
first, then the repair, and returns the numbers that separate the two. Use the file as a
card deck during a loop review, and run it to see the evidence.

Requirement: torch. Run: python six_pitfalls_before_after.py
"""

from __future__ import annotations

import torch
import torch.nn as nn


def make_separable_batch(n_per_class=64, in_features=10, num_classes=3, seed=0):
    """Build a separable batch from one Gaussian blob for each class.

    Args:
        n_per_class: The number of samples for each class.
        in_features: The number of input features.
        num_classes: The number of classes.
        seed: The seed of the generator. It makes the reproduction exact.
    Returns:
        A tuple (x, y). The tensor y holds long class indices.
    Note:
        A defect that costs accuracy needs learnable data. Random labels hide the cost,
        because no model can beat chance on them.
    """
    generator = torch.Generator().manual_seed(seed)
    centers = torch.randn(num_classes, in_features, generator=generator) * 3.0
    y = torch.arange(num_classes).repeat_interleave(n_per_class)
    x = centers[y] + torch.randn(y.numel(), in_features, generator=generator)
    return x, y


def train_to_convergence(model, x, y, *, steps=300, lr=1e-2):
    """Train a model on one batch, then report its loss and its accuracy in eval mode.

    Args:
        model: The nn.Module to train.
        x: The input batch.
        y: The label batch.
        steps: The number of optimizer steps.
        lr: The learning rate.
    Returns:
        A tuple (loss, accuracy) of two floats.
    Note:
        Compare two models after this function, not at init. At init the two models hold
        random weights, and the comparison then reports noise.
    """
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    model.train()
    for _ in range(steps):
        optimizer.zero_grad()
        loss = criterion(model(x), y)
        loss.backward()
        optimizer.step()
    model.eval()
    with torch.no_grad():
        out = model(x)
        return criterion(out, y).item(), (out.argmax(dim=-1) == y).float().mean().item()


# ──────────────────────────────────────────────────────────────────────
# Entry 1: the run skips the overfit of one batch
# ──────────────────────────────────────────────────────────────────────
def pitfall_1_overfit_single_batch():
    """Entry 1. Broken: the run starts on the full set with augmentation and regularization.

    A stall then has too many causes, and you cannot localize the defect. Repair: train on
    one fixed small batch first, and prove that the loss reaches almost zero.

    Returns:
        The final loss as a float. A value near zero opens Stage 2 gate 5.
    """
    model = nn.Linear(10, 3)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-2)

    xb = torch.randn(4, 10)  # One fixed small batch.
    yb = torch.randint(0, 3, (4,))
    model.train()
    loss = None
    for _ in range(300):
        optimizer.zero_grad()
        loss = criterion(model(xb), yb)
        loss.backward()
        optimizer.step()
    # A loss that stays high reports a defect. Read entries 2, 3, and 4 next.
    return loss.item()


# ──────────────────────────────────────────────────────────────────────
# Entry 2: the run forgets train() or eval()
# ──────────────────────────────────────────────────────────────────────
def pitfall_2_train_eval():
    """Entry 2. Broken: the evaluation runs in train mode.

    The dropout layer still drops, and the BatchNorm layer still reads batch statistics,
    so the same batch gives a different answer on every call. Repair: call model.eval()
    and torch.no_grad() before you evaluate.

    Returns:
        A dict that shows the random answer in train mode and the stable answer in eval mode.
    """
    model = nn.Sequential(nn.Linear(10, 10), nn.Dropout(0.5), nn.Linear(10, 3))
    xb = torch.randn(8, 10)

    # Broken: the mode stays on train, and two passes disagree.
    model.train()
    wrong1, wrong2 = model(xb), model(xb)
    inconsistent = not torch.allclose(wrong1, wrong2)

    # Repair: eval mode plus no_grad. Two passes agree.
    model.eval()
    with torch.no_grad():
        right1, right2 = model(xb), model(xb)
    consistent = torch.allclose(right1, right2)
    return {"train_mode_inconsistent": inconsistent, "eval_mode_consistent": consistent}


# ──────────────────────────────────────────────────────────────────────
# Entry 3: the loop forgets zero_grad()
# ──────────────────────────────────────────────────────────────────────
def pitfall_3_zero_grad():
    """Entry 3. Broken: the loop never clears the gradient.

    PyTorch adds each new gradient to the old one, so the old gradient pollutes every
    update. Repair: keep the order zero_grad, forward, backward, step.

    Returns:
        A dict with the gradient norm after three backward calls in each variant.
    Note:
        The evidence here is the gradient, not the loss. On easy data an accumulated
        gradient acts like a larger learning rate, and the broken loop can then reach the
        lower loss by accident. The size of the gradient tells the truth: after k backward
        calls the broken variant carries k times the correct gradient.
    """
    xb, yb = make_separable_batch(n_per_class=8, in_features=10, num_classes=3, seed=1)
    criterion = nn.CrossEntropyLoss()
    torch.manual_seed(0)
    model = nn.Linear(10, 3)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
    weight = model.weight

    # Broken: three backward calls without zero_grad(). PyTorch adds every new gradient
    # to the old one, so .grad now holds three times the gradient of one step.
    for _ in range(3):
        criterion(model(xb), yb).backward()
    bad_grad_norm = weight.grad.norm().item()

    # Repair: clear the gradient at the start of every step.
    for _ in range(3):
        optimizer.zero_grad()  # The key line.
        criterion(model(xb), yb).backward()
    good_grad_norm = weight.grad.norm().item()

    return {
        "grad_norm_without_zero_grad": round(bad_grad_norm, 4),
        "grad_norm_with_zero_grad": round(good_grad_norm, 4),
        "ratio": round(bad_grad_norm / good_grad_norm, 3),
        "note": "The ratio must equal the number of backward calls, here 3.",
    }


# ──────────────────────────────────────────────────────────────────────
# Entry 4: the code confuses logits with probabilities
# ──────────────────────────────────────────────────────────────────────
def pitfall_4_logits_vs_softmax():
    """Entry 4. Broken: the model ends with a Softmax, and CrossEntropyLoss adds a second one.

    The loss then reads a probability as a logit. The gradient flattens, and the loss
    stops at a floor. Repair: let the model give logits, and let the loss apply the
    softmax. Compute a probability separately when the inference needs one.

    Returns:
        A dict with the loss and the accuracy of each model after training.
    Note:
        Compare the two models after training. At init both models hold random weights,
        and the broken model can then show the lower loss by accident.
    """
    x, y = make_separable_batch()

    # Broken: two softmax calls in a row.
    torch.manual_seed(0)
    bad_model = nn.Sequential(nn.Linear(10, 3), nn.Softmax(dim=-1))
    bad_loss, bad_acc = train_to_convergence(bad_model, x, y)

    # Repair: the model gives logits.
    torch.manual_seed(0)
    good_model = nn.Sequential(nn.Linear(10, 3))
    good_loss, good_acc = train_to_convergence(good_model, x, y)

    # Compute the probabilities under no_grad. A conversion of a tensor that carries a
    # graph raises the warning of entry 12.
    with torch.no_grad():
        probs = good_model(x).softmax(dim=-1)
    return {
        "bad_loss_double_softmax": round(bad_loss, 4),
        "good_loss_logits": round(good_loss, 4),
        "bad_acc": round(bad_acc, 3),
        "good_acc": round(good_acc, 3),
        "probs_sum_to_one": round(probs.sum(dim=-1).mean().item(), 4),
        "note": "The repaired model must reach the lower loss after the same training.",
    }


# ──────────────────────────────────────────────────────────────────────
# Entry 5: a layer in front of a BatchNorm layer keeps its bias
# ──────────────────────────────────────────────────────────────────────
def pitfall_5_bias_with_bn():
    """Entry 5. Broken: a Conv layer or a Linear layer in front of a BatchNorm layer keeps bias=True.

    The BatchNorm layer removes the mean and cancels that bias, so the parameter is dead
    weight. Repair: set bias=False on the layer in front of the BatchNorm layer.

    Returns:
        A dict that reports the redundant bias and its removal.
    """
    # Broken: a redundant bias.
    bad = nn.Sequential(nn.Conv2d(3, 16, 3, bias=True), nn.BatchNorm2d(16))
    # Repair: no bias.
    good = nn.Sequential(nn.Conv2d(3, 16, 3, bias=False), nn.BatchNorm2d(16))
    bad_has_bias = bad[0].bias is not None
    good_has_bias = good[0].bias is not None
    return {
        "bad_layer_has_redundant_bias": bad_has_bias,
        "good_layer_bias_removed": not good_has_bias,
    }


# ──────────────────────────────────────────────────────────────────────
# Entry 6: the code uses view in place of permute
# ──────────────────────────────────────────────────────────────────────
def pitfall_6_view_vs_permute():
    """Entry 6. Broken: the code moves NCHW to NHWC with view or reshape.

    Those two functions read the memory in order and push the elements into the new
    shape, so the content becomes wrong while the shape looks right. Repair: move an axis
    with permute. Use view or reshape to merge an axis or to split an axis. Call
    contiguous() before view() on the result of a permute.

    Returns:
        A dict with the roundtrip proof, the corruption proof, and the flat shape.
    """
    x = torch.arange(2 * 3 * 2 * 2).float().reshape(2, 3, 2, 2)  # (N,C,H,W)

    # Broken: reshape imitates a transpose. The shape fits, the content does not.
    wrong_nhwc = x.reshape(2, 2, 2, 3)

    # Repair: permute moves the axis.
    right_nhwc = x.permute(0, 2, 3, 1)  # (N,H,W,C)

    # Proof: the repaired tensor returns to the original tensor, the broken one does not.
    permute_roundtrip_ok = torch.equal(right_nhwc.permute(0, 3, 1, 2), x)
    wrong_is_corrupted = not torch.equal(wrong_nhwc.permute(0, 3, 1, 2), x)

    # The result of a permute is not contiguous, so call contiguous() before view().
    flat = right_nhwc.contiguous().view(2, -1)  # This equals right_nhwc.reshape(2, -1).
    return {
        "permute_roundtrip_ok": permute_roundtrip_ok,
        "reshape_as_transpose_is_corrupted": wrong_is_corrupted,
        "flat_shape": tuple(flat.shape),
    }


if __name__ == "__main__":
    torch.manual_seed(0)
    print("entry 1 overfit one batch :", pitfall_1_overfit_single_batch())
    print("entry 2 train/eval        :", pitfall_2_train_eval())
    print("entry 3 zero_grad         :", pitfall_3_zero_grad())
    print("entry 4 logits vs softmax :", pitfall_4_logits_vs_softmax())
    print("entry 5 bias with BN      :", pitfall_5_bias_with_bn())
    print("entry 6 view vs permute   :", pitfall_6_view_vs_permute())
