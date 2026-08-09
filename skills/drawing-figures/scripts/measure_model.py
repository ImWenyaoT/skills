#!/usr/bin/env python3
"""
measure_model.py — general-purpose model efficiency measurement

Three project-agnostic measurement functions:
  - count_params:     count parameters (M)
  - measure_runtime:  measure inference latency (ms)
  - measure_flops:    compute GMACs (thop returns MAC counts, FLOPs≈2×MAC; needs thop)

Plus main(), which is not bound to any project's ConfigLoader/create_model;
project-specific model loading is the caller's job (a thin wrapper script).
"""

import argparse
import time
from typing import Optional, Tuple

import torch
import torch.nn as nn


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def count_params(model: nn.Module) -> dict:
    """
    Count the model's parameters, returning the total and the trainable count (in millions, M).

    Args:
        model: any nn.Module.

    Returns:
        {"total_M": float, "trainable_M": float}
        —— both values are in millions (multiply by 1e6 for the actual parameter count).
    """
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return {
        "total_M": total / 1e6,
        "trainable_M": trainable / 1e6,
    }


def measure_runtime(
    model: nn.Module,
    input_shape: Tuple[int, ...],
    device: str = "cpu",
    iters: int = 50,
    warmup: int = 5,
) -> float:
    """
    Measure the average time of one forward pass through the model (milliseconds).

    Runs `warmup` warm-up passes first (excluded from the statistics), then times `iters` passes
    for real; on CUDA devices, torch.cuda.synchronize() is called around each timed pass to keep
    the measurement honest.

    Args:
        model:       the nn.Module under test.
        input_shape: input tensor shape, e.g. (1, 3, 256, 256).
        device:      "cpu" or "cuda" (string).
        iters:       number of timed passes, default 50.
        warmup:      number of warm-up passes, default 5.

    Returns:
        Average time per inference, in milliseconds (ms).
    """
    dev = torch.device(device)
    dummy = torch.randn(*input_shape).to(dev)
    model = model.to(dev)
    model.eval()

    use_cuda = dev.type == "cuda"

    # Warm-up phase: let the GPU/CPU settle into a steady state
    with torch.no_grad():
        for _ in range(warmup):
            model(dummy)
            if use_cuda:
                torch.cuda.synchronize()

    # Timed runs
    times = []
    with torch.no_grad():
        for _ in range(iters):
            if use_cuda:
                torch.cuda.synchronize()
            t0 = time.perf_counter()
            model(dummy)
            if use_cuda:
                torch.cuda.synchronize()
            t1 = time.perf_counter()
            times.append((t1 - t0) * 1000.0)  # convert to milliseconds

    return sum(times) / len(times)


def measure_flops(
    model: nn.Module,
    input_shape: Tuple[int, ...],
) -> Optional[float]:
    """
    Compute the model's compute cost with the thop library, returning GMACs (thop returns MAC
    counts, FLOPs≈2×MAC); returns None when thop is unavailable.

    thop registers hooks on the model, so if you still need measure_runtime afterwards,
    call this function first and time the latency second (or call it on a copy).

    Args:
        model:       the nn.Module under test (temporarily moved to CPU).
        input_shape: input tensor shape, e.g. (1, 3, 256, 256).

    Returns:
        GMACs (thop returns MAC counts, FLOPs≈2×MAC) as a float; None if thop is not installed
        or profiling fails.
    """
    try:
        from thop import profile  # type: ignore[import]
    except ImportError:
        return None

    dummy = torch.randn(*input_shape)
    model_cpu = model.cpu().eval()

    try:
        flops, _ = profile(model_cpu, inputs=(dummy,), verbose=False)
        return flops / 1e9
    except Exception:
        return None


# ---------------------------------------------------------------------------
# CLI entry point: not bound to any project's config/model loader
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Command-line entry point, taking the generic arguments.

    Project-specific model creation (create_model, ConfigLoader, and the like)
    is not implemented here——the caller (each paper's thin wrapper script) is
    responsible for instantiating the model and handing it to the three functions above.

    The CLI today only offers --input-shape to show the interface contract; in practice,
    import measure_model in your calling script and invoke the functions directly.
    """
    parser = argparse.ArgumentParser(
        description="General-purpose model efficiency measurement (no project model loader)"
    )
    parser.add_argument(
        "--input-shape",
        type=int,
        nargs="+",
        default=[1, 3, 256, 256],
        metavar="N",
        help="input tensor shape, e.g. --input-shape 1 3 256 256 (the default)",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        help="inference device: cpu or cuda (default cpu)",
    )
    parser.add_argument(
        "--iters",
        type=int,
        default=50,
        help="number of timed passes (default 50)",
    )
    parser.add_argument(
        "--warmup",
        type=int,
        default=5,
        help="number of warm-up passes (default 5)",
    )
    args = parser.parse_args()

    print("measure_model.py：通用效率测量工具")
    print("请在调用脚本中 import measure_model 并传入已实例化的模型。")
    print(f"input-shape = {args.input_shape}")
    print(f"device      = {args.device}")
    print(f"iters       = {args.iters}, warmup = {args.warmup}")
    print()
    print("示例用法：")
    print("  import measure_model as mm")
    print("  params  = mm.count_params(model)")
    print("  runtime = mm.measure_runtime(model, tuple(input_shape), device=device)")
    print("  gmacs   = mm.measure_flops(model, tuple(input_shape))  # GMACs（thop 返回 MAC 数,FLOPs≈2×MAC）")


if __name__ == "__main__":
    main()
