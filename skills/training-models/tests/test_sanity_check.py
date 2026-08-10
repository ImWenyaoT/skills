"""Verify that sanity_check.py's gates actually catch the defects they claim to.

Every check here is paired: a model or loop that should pass, and one broken on
purpose that must fail. A gate that only ever reports "pass" is not a gate, and
running the file to see that it prints something is not evidence that it works.

Needs PyTorch, which is the skill's declared runtime and is deliberately not a
dependency of this repository — installing it to test a measurement helper would
cost more than it buys. Without torch every test here skips, and the notebook
beside this file runs the same assertions on Colab, where torch is already there.
"""

from __future__ import annotations

import importlib.util
import inspect
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:  # pragma: no cover - the import is the skip condition
    import torch
    import torch.nn as nn

    HAS_TORCH = True
except ImportError:  # pragma: no cover
    HAS_TORCH = False


def load_sanity_check():
    """Import the bundled script by path, the way a user running it would."""
    spec = importlib.util.spec_from_file_location(
        "sanity_check", ROOT / "scripts" / "sanity_check.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@unittest.skipUnless(HAS_TORCH, "PyTorch is the skill's runtime, not this repo's")
class SanityCheckGateTests(unittest.TestCase):
    N_CLASSES = 4

    @classmethod
    def setUpClass(cls) -> None:
        cls.sc = load_sanity_check()

    def setUp(self) -> None:
        torch.manual_seed(0)
        self.xb = torch.randn(8, 6)
        self.yb = torch.randint(0, self.N_CLASSES, (8,))
        self.criterion = nn.CrossEntropyLoss()

    def linear_model(self) -> nn.Module:
        return nn.Linear(6, self.N_CLASSES)

    # --- gate 1: loss at init matches the prior -------------------------------

    def test_gate1_passes_on_a_model_whose_loss_starts_at_the_prior(self) -> None:
        result = self.sc.verify_loss_at_init(self.linear_model(), self.xb, self.yb, self.criterion)
        self.assertEqual(result["verdict"], "pass", result)
        self.assertAlmostEqual(result["expected"], torch.log(torch.tensor(4.0)).item(), places=4)

    def test_gate1_does_not_false_alarm_on_the_tiny_batch_gate5_asks_for(self) -> None:
        """The skill sends one batch of 2-8 examples through every gate.

        On that few samples the measured cross-entropy scatters well past a fixed
        0.5 band, so a fixed band fails a healthy model — and gate 1 is first in the
        diagnostic order, so a false shut gate sends you hunting a defect that is
        not there.
        """
        torch.manual_seed(0)
        tiny_x = torch.randn(4, 6)
        tiny_y = torch.randint(0, self.N_CLASSES, (4,))
        result = self.sc.verify_loss_at_init(self.linear_model(), tiny_x, tiny_y, self.criterion)
        self.assertEqual(result["verdict"], "pass", result)

    def test_gate1_still_fails_a_wrong_logit_scale_on_a_tiny_batch(self) -> None:
        """Widening the band for noise must not blunt the defect it exists to catch."""
        torch.manual_seed(0)
        tiny_x = torch.randn(4, 6)
        tiny_y = torch.randint(0, self.N_CLASSES, (4,))
        model = self.linear_model()
        with torch.no_grad():
            model.bias[0] += 12.0
        result = self.sc.verify_loss_at_init(model, tiny_x, tiny_y, self.criterion)
        self.assertEqual(result["verdict"], "fail", result)

    def test_gate1_fails_when_the_final_layer_carries_a_wrong_bias(self) -> None:
        """The defect this gate exists for: a logit scale that is nowhere near uniform."""
        model = self.linear_model()
        with torch.no_grad():
            model.bias[0] += 12.0
        result = self.sc.verify_loss_at_init(model, self.xb, self.yb, self.criterion)
        self.assertEqual(result["verdict"], "fail")

    # --- gate 4: the model reads its input ------------------------------------

    def test_gate4_separates_a_model_that_reads_its_input_from_one_that_cannot(self) -> None:
        reads_input = self.sc.input_independent_baseline(
            self.linear_model(), self.xb, self.yb, self.criterion, steps=60
        )

        class IgnoresInput(nn.Module):
            def __init__(self, n_classes: int) -> None:
                super().__init__()
                self.bias = nn.Parameter(torch.zeros(n_classes))

            def forward(self, x):  # noqa: ARG002 - ignoring x is the point
                return self.bias.expand(x.shape[0], -1)

        ignores_input = self.sc.input_independent_baseline(
            IgnoresInput(self.N_CLASSES), self.xb, self.yb, self.criterion, steps=60
        )
        self.assertNotEqual(reads_input["verdict"], ignores_input["verdict"])
        self.assertEqual(ignores_input["verdict"], "fail")

    # --- gate 5: one small batch overfits -------------------------------------

    def test_gate5_reports_a_verdict_like_every_other_gate(self) -> None:
        """A bare (initial, final) tuple leaves the caller to decide whether it opened."""
        # A bare linear layer cannot memorise eight random points in six dimensions;
        # the gate assumes the simplest architecture that *can*.
        model = nn.Sequential(nn.Linear(6, 32), nn.ReLU(), nn.Linear(32, self.N_CLASSES))
        result = self.sc.overfit_single_batch(model, self.xb, self.yb, self.criterion, steps=400)
        self.assertIsInstance(result, dict)
        self.assertLess(result["final_loss"], result["initial_loss"])
        self.assertEqual(result["verdict"], "pass", result)

    def test_gate5_cannot_overfit_a_model_that_ignores_its_input(self) -> None:
        class Constant(nn.Module):
            def __init__(self, n_classes: int) -> None:
                super().__init__()
                self.bias = nn.Parameter(torch.zeros(n_classes))

            def forward(self, x):
                return self.bias.expand(x.shape[0], -1).detach() + self.bias * 0

        result = self.sc.overfit_single_batch(
            Constant(self.N_CLASSES), self.xb, self.yb, self.criterion, steps=400
        )
        self.assertEqual(result["verdict"], "fail", result)

    # --- checklist 2: train/eval mode -----------------------------------------

    def test_mode_check_is_not_applicable_without_a_mode_dependent_layer(self) -> None:
        """A linear model behaves identically in both modes; saying "pass" would lie."""
        verdict = self.sc.check_train_eval_toggle(self.linear_model(), self.xb)
        self.assertEqual(verdict["verdict"], "not_applicable")

    def test_mode_check_passes_when_dropout_makes_the_modes_differ(self) -> None:
        model = nn.Sequential(nn.Linear(6, 16), nn.Dropout(0.5), nn.Linear(16, self.N_CLASSES))
        verdict = self.sc.check_train_eval_toggle(model, self.xb)
        self.assertEqual(verdict["verdict"], "pass")

    # --- checklist 3: zero_grad in the loop -----------------------------------

    def test_zero_grad_check_fails_on_a_loop_that_omits_it(self) -> None:
        broken = (
            "for xb, yb in loader:\n"
            "    loss = criterion(model(xb), yb)\n"
            "    loss.backward()\n"
            "    opt.step()\n"
        )
        self.assertEqual(self.sc.check_zero_grad_in_loop(broken)["verdict"], "fail")

    def test_zero_grad_check_passes_on_a_real_function_read_by_inspect(self) -> None:
        """The documented usage is inspect.getsource, so exercise that path."""

        def train_one_epoch(model, loader, criterion, opt):
            for xb, yb in loader:
                opt.zero_grad()
                loss = criterion(model(xb), yb)
                loss.backward()
                opt.step()

        source = inspect.getsource(train_one_epoch)
        self.assertEqual(self.sc.check_zero_grad_in_loop(source)["verdict"], "pass")

    # --- checklist 4: the logits contract -------------------------------------

    def test_logits_contract_passes_on_raw_logits(self) -> None:
        verdict = self.sc.check_logits_contract(self.linear_model(), self.xb, self.criterion)
        self.assertEqual(verdict["verdict"], "pass")

    def test_logits_contract_fails_when_softmax_is_applied_before_the_loss(self) -> None:
        """Double-softmax: the classic silent one, since the loss still decreases."""
        model = nn.Sequential(nn.Linear(6, self.N_CLASSES), nn.Softmax(dim=-1))
        verdict = self.sc.check_logits_contract(model, self.xb, self.criterion)
        self.assertEqual(verdict["verdict"], "fail")

    # --- the whole report runs -------------------------------------------------

    def test_run_sanity_checks_completes_on_a_correct_setup(self) -> None:
        import contextlib
        import io

        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            self.sc.run_sanity_checks(
                self.linear_model(), self.xb, self.yb, self.criterion, loop_source=None
            )
        printed = buffer.getvalue()
        for gate in ("gate 1", "gate 4", "gate 5"):
            self.assertIn(gate, printed)


if __name__ == "__main__":
    unittest.main()
