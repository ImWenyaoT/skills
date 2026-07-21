"""One command that runs the Stage 2 gates and three loop checks.

This file backs Stage 2 gate 1 (loss at init), gate 4 (input-independent baseline), and
gate 5 (one batch overfits). It also backs checklist entries 2, 3, and 4.

Give `run_sanity_checks()` your model, one small batch, and your loss function. The
function prints one report. Read the report from the top. The first gate that stays shut
localizes the defect.

Requirement: torch. Run: python sanity_check.py
"""

from __future__ import annotations

import copy
import math

import torch
import torch.nn as nn

# The layers that change their behaviour between train mode and eval mode.
# LayerNorm is not in this list, because LayerNorm acts the same in both modes.
MODE_DEPENDENT_LAYERS = (
    nn.Dropout,
    nn.Dropout1d,
    nn.Dropout2d,
    nn.Dropout3d,
    nn.AlphaDropout,
    nn.BatchNorm1d,
    nn.BatchNorm2d,
    nn.BatchNorm3d,
)


def overfit_single_batch(model, xb, yb, criterion, *, steps=300, lr=1e-2):
    """Stage 2 gate 5: train on one batch many times, and report the loss.

    Args:
        model: The nn.Module to check. This function updates its weights.
        xb: The input of one small batch.
        yb: The label of one small batch.
        criterion: The loss function. It must match the output contract of the model.
        steps: The number of optimizer steps.
        lr: The learning rate.
    Returns:
        A tuple (first_loss, last_loss) that shows how far the loss fell.
    Note:
        A loss near zero opens the gate. The forward path, the backward path, and the
        optimizer are then correct, so look at the data, the regularization, or the
        generalization. A loss that stays high shuts the gate and reports a defect in the
        pipeline itself.
    """
    model.train()
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    first_loss = None
    last_loss = None
    for _ in range(steps):
        opt.zero_grad()  # Checklist entry 3: clear the gradient at every step.
        loss = criterion(model(xb), yb)
        loss.backward()
        opt.step()
        last_loss = loss.item()
        if first_loss is None:
            first_loss = last_loss
    return first_loss, last_loss


def check_train_eval_toggle(model, xb):
    """Checklist entry 2: prove that the model answers to train mode and to eval mode.

    The check runs a copy of the model in both modes and compares the four outputs. A
    model with a dropout layer or a batchnorm layer must give a different output in each
    mode. A model without such a layer cannot show the difference, and the check then
    reports that it does not apply.

    Args:
        model: The nn.Module to check. The check copies it, so the weights, the mode, and
            the batchnorm statistics of your model do not change.
        xb: The input of one small batch.
    Returns:
        A dict with the layer names, the two comparisons, a verdict, and a note.
    Note:
        The verdict is one of "pass", "fail", or "not_applicable". This check reads the
        model alone. It cannot see your training loop, so it cannot prove that the loop
        calls model.train() and that the evaluation calls model.eval(). Read those two
        lines yourself.
    """
    probe = copy.deepcopy(model)
    layer_names = sorted(
        {
            type(m).__name__
            for m in probe.modules()
            if isinstance(m, MODE_DEPENDENT_LAYERS)
        }
    )

    probe.train()
    with torch.no_grad():
        train_out_1 = probe(xb)
        train_out_2 = probe(xb)
    probe.eval()
    with torch.no_grad():
        eval_out_1 = probe(xb)
        eval_out_2 = probe(xb)

    eval_is_stable = bool(torch.allclose(eval_out_1, eval_out_2))
    train_is_random = not bool(torch.allclose(train_out_1, train_out_2))
    modes_differ = not bool(torch.allclose(train_out_1, eval_out_1))

    if not layer_names:
        verdict = "not_applicable"
        note = (
            "This model holds no dropout layer and no batchnorm layer. The two modes are "
            "equal by design, so this check proves nothing. Read your loop instead."
        )
    elif modes_differ and eval_is_stable:
        verdict = "pass"
        note = (
            "The two modes differ, and eval mode repeats itself. Call model.train() "
            "before you train, and call model.eval() before you evaluate."
        )
    elif not eval_is_stable:
        verdict = "fail"
        note = (
            "Eval mode gives a different answer on the same batch. A layer stays random "
            "after model.eval(). Look for a manual dropout call or a custom module."
        )
    else:
        verdict = "fail"
        note = (
            "The model holds a mode-dependent layer, but the two modes agree. The mode "
            "switch does not reach that layer. Look for a detached submodule."
        )

    return {
        "mode_dependent_layers": layer_names,
        "train_mode_is_random": train_is_random,
        "eval_mode_is_stable": eval_is_stable,
        "modes_differ": modes_differ,
        "verdict": verdict,
        "note": note,
    }


def check_zero_grad_in_loop(loop_source):
    """Checklist entry 3: search the source of a training loop for zero_grad().

    Args:
        loop_source: The source text of your training loop, or None. Use
            inspect.getsource(your_train_function) to get the text.
    Returns:
        A dict with the tokens that the check found, a verdict, and a note.
    Note:
        This check is a heuristic on text. It is not a code review, and it cannot follow a
        helper function. A loop with gradient accumulation omits zero_grad() on purpose,
        so read the loop before you trust the verdict "fail".
    """
    if loop_source is None:
        return {
            "verdict": "not_run",
            "note": (
                "No source arrived. Pass inspect.getsource(your_train_function) to run "
                "this check. Until then, no evidence exists for checklist entry 3."
            ),
        }

    found_zero_grad = "zero_grad" in loop_source
    found_backward = "backward" in loop_source
    found_step = ".step(" in loop_source

    if found_zero_grad:
        verdict = "pass"
        note = "The source calls zero_grad(). Confirm the order: zero_grad, forward, backward, step."
    elif found_backward:
        verdict = "fail"
        note = (
            "The source calls backward() but never zero_grad(). PyTorch adds each new "
            "gradient to the old one, so every step uses a wrong gradient."
        )
    else:
        verdict = "not_applicable"
        note = "The source calls neither zero_grad() nor backward(). This text is not a training loop."

    return {
        "found_zero_grad": found_zero_grad,
        "found_backward": found_backward,
        "found_optimizer_step": found_step,
        "verdict": verdict,
        "note": note,
    }


def check_logits_contract(model, xb, criterion):
    """Checklist entry 4: compare the output of the model with the input of the loss.

    Args:
        model: The nn.Module to check.
        xb: The input of one small batch. The signature keeps it for a future shape check.
        criterion: The loss function.
    Returns:
        A dict that reports the last layer, the demand of the loss, and the conflict.
    Note:
        CrossEntropyLoss and BCEWithLogitsLoss hold a softmax or a sigmoid inside, so they
        want raw logits. A model that ends with Softmax or Sigmoid applies the same
        function a second time. The loss then flattens, and the run stalls in silence.
    """
    del xb  # The check needs the modules alone, not a forward pass.
    last_module = list(model.modules())[-1]
    model_outputs_probs = isinstance(last_module, (nn.Softmax, nn.LogSoftmax, nn.Sigmoid))
    loss_expects_logits = isinstance(criterion, (nn.CrossEntropyLoss, nn.BCEWithLogitsLoss))
    conflict = model_outputs_probs and loss_expects_logits
    return {
        "model_last_layer_is_softmax_or_sigmoid": model_outputs_probs,
        "loss_expects_logits": loss_expects_logits,
        "double_activation_conflict": conflict,
        "verdict": "fail" if conflict else "pass",
        "note": (
            "Remove the last activation from the model, because the loss applies it."
            if conflict
            else "The model output and the loss input agree."
        ),
    }


def verify_loss_at_init(model, xb, yb, criterion, *, expected=None):
    """Stage 2 gate 1: compare the loss at init with the theoretical prior.

    Args:
        model: An untrained nn.Module. Call this function before you train.
        xb: The input of one small batch.
        yb: The label of one small batch.
        criterion: The loss function.
        expected: The expected loss at init. Leave it as None with CrossEntropyLoss, and
            the function derives log(num_classes).

    Returns:
        A dict with the measured loss, the expected loss, and the verdict.
    Note:
        A uniform n-class softmax starts near -log(1/n) = log(n). A large gap points at
        the labels, the final layer, the logit scale, or the loss input contract.
    """
    model.eval()
    with torch.no_grad():
        out = model(xb)
        loss = criterion(out, yb).item()
    note = "No prior arrived. The function reports the measured value alone."
    if expected is None and isinstance(criterion, nn.CrossEntropyLoss):
        n_classes = out.shape[-1]
        expected = math.log(n_classes)
        note = f"CrossEntropy at init must sit near log({n_classes}) = {expected:.4f}"
    close = expected is not None and abs(loss - expected) <= 0.5
    return {
        "loss_at_init": loss,
        "expected": expected,
        "close_to_prior": bool(close),
        "verdict": "pass" if close else ("fail" if expected is not None else "not_run"),
        "note": note,
    }


def input_independent_baseline(model, xb, yb, criterion, *, steps=100, lr=1e-2):
    """Stage 2 gate 4: prove that the model reads its input.

    Args:
        model: An nn.Module. The function copies it twice, so your weights do not change.
        xb: The input of one small batch.
        yb: The label of one small batch.
        criterion: The loss function.
        steps: The number of optimizer steps for each copy.
        lr: The learning rate for each copy.
    Returns:
        A dict with the two final losses and the verdict.
    Note:
        The second copy trains on a zeroed input. A healthy model cannot separate the
        labels without the input, so its loss must stay clearly higher. A similar loss
        means that the model ignores the input, or that a label leaks into the batch.
    """
    real = copy.deepcopy(model)
    zeroed = copy.deepcopy(model)
    _, real_last = overfit_single_batch(real, xb, yb, criterion, steps=steps, lr=lr)
    _, zero_last = overfit_single_batch(
        zeroed, torch.zeros_like(xb), yb, criterion, steps=steps, lr=lr
    )
    uses_input = zero_last > real_last * 1.2
    return {
        "real_input_last_loss": real_last,
        "zeroed_input_last_loss": zero_last,
        "uses_input_signal": bool(uses_input),
        "verdict": "pass" if uses_input else "fail",
        "note": (
            "The zeroed run is clearly worse, so the model reads its input."
            if uses_input
            else "The zeroed run is not worse. The model ignores the input, or a label leaks."
        ),
    }


def run_sanity_checks(model, xb, yb, criterion, *, loop_source=None):
    """Run every check in this file, and print one report.

    Args:
        model: The nn.Module to check.
        xb: The input of one fixed small batch.
        yb: The label of one fixed small batch.
        criterion: The loss function.
        loop_source: The source text of your training loop, or None. Pass
            inspect.getsource(your_train_function) to run the zero_grad check.
    Returns:
        None. The function prints the report.
    Note:
        Gate 1 and gate 4 need untrained weights, so they run before gate 5. Gate 5
        trains the model that you pass in, and it therefore runs last.
    """
    rule = "=" * 72
    print(rule)
    print("[Stage 2 gate 1] loss at init against the prior")
    print(verify_loss_at_init(model, xb, yb, criterion))

    print(rule)
    print("[Stage 2 gate 4] input-independent baseline")
    print(input_independent_baseline(model, xb, yb, criterion))

    print(rule)
    print("[checklist 4] logits contract")
    print(check_logits_contract(model, xb, criterion))

    print(rule)
    print("[checklist 2] train mode against eval mode")
    print(check_train_eval_toggle(model, xb))

    print(rule)
    print("[checklist 3] zero_grad in the loop")
    print(check_zero_grad_in_loop(loop_source))

    print(rule)
    print("[Stage 2 gate 5] one batch overfits")
    first, last = overfit_single_batch(model, xb, yb, criterion)
    print(f"first_loss={first:.4f}  last_loss={last:.4f}")
    if last < first * 0.1:
        verdict = "PASS: the gate is open. Look at the data, the regularization, or the generalization."
    else:
        verdict = "FAIL: the gate is shut. Check the mode, zero_grad, the logits contract, and the labels."
    print(verdict)
    print(rule)


def _demo_train_loop(model, xb, yb, criterion, steps=10):
    """Train a model for a few steps. The zero_grad check reads the source of this function.

    Args:
        model: The nn.Module to train.
        xb: The input of one batch.
        yb: The label of one batch.
        criterion: The loss function.
        steps: The number of optimizer steps.
    Returns:
        The loss of the last step as a float.
    """
    opt = torch.optim.Adam(model.parameters(), lr=1e-2)
    model.train()
    loss_value = 0.0
    for _ in range(steps):
        opt.zero_grad()
        loss = criterion(model(xb), yb)
        loss.backward()
        opt.step()
        loss_value = loss.item()
    return loss_value


if __name__ == "__main__":
    import inspect

    source = inspect.getsource(_demo_train_loop)

    # Demo 1: a model that ends with a Softmax. The logits contract check must report a
    # conflict, and the overfit gate must stay shut.
    torch.manual_seed(0)
    bad_model = nn.Sequential(nn.Linear(10, 3), nn.Softmax(dim=-1))
    xb = torch.randn(8, 10)
    yb = torch.randint(0, 3, (8,))
    print(">>> Model A: the last layer holds a Softmax. Expect a shut gate.")
    run_sanity_checks(bad_model, xb, yb, nn.CrossEntropyLoss(), loop_source=source)

    # Demo 2: the repair. The model gives logits, and every gate must open.
    print("\n>>> Model B: the repair. The model gives logits. Expect an open gate.")
    good_model = nn.Sequential(nn.Linear(10, 3))
    run_sanity_checks(good_model, xb, yb, nn.CrossEntropyLoss(), loop_source=source)

    # Demo 3: checklist entry 2 alone. The first model holds a dropout layer, so the two
    # modes must differ. The second model holds none, so the check cannot apply.
    print("\n>>> checklist 2 on two models:")
    with_dropout = nn.Sequential(nn.Linear(10, 16), nn.ReLU(), nn.Dropout(0.5), nn.Linear(16, 3))
    print("  with dropout   :", check_train_eval_toggle(with_dropout, xb))
    print("  without dropout:", check_train_eval_toggle(nn.Sequential(nn.Linear(10, 3)), xb))

    # Demo 4: checklist entry 3 on a loop that forgets zero_grad().
    print("\n>>> checklist 3 on a loop without zero_grad():")
    broken_loop = "for xb, yb in loader:\n    loss = criterion(model(xb), yb)\n    loss.backward()\n    opt.step()\n"
    print(" ", check_zero_grad_in_loop(broken_loop))
