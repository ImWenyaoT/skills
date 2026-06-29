#!/usr/bin/env python3
"""
measure_model.py — 通用模型效率测量工具

提供三个与项目无关的测量函数：
  - count_params:     统计参数量（M）
  - measure_runtime:  测量推理延迟（ms）
  - measure_flops:    计算 GMACs（thop 返回 MAC 数,FLOPs≈2×MAC，需 thop）

以及 main()，不绑定任何项目的 ConfigLoader/create_model；
项目特定的模型加载由调用方（薄壳脚本）负责。
"""

import argparse
import time
from typing import Optional, Tuple

import torch
import torch.nn as nn


# ---------------------------------------------------------------------------
# 公共 API
# ---------------------------------------------------------------------------

def count_params(model: nn.Module) -> dict:
    """
    统计模型参数量，返回总量与可训练量（单位：百万 M）。

    Args:
        model: 任意 nn.Module。

    Returns:
        {"total_M": float, "trainable_M": float}
        —— 两个值均以百万为单位（乘以 1e6 得实际参数个数）。
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
    测量模型单次前向推理的平均耗时（毫秒）。

    先进行 warmup 次热身（不计入统计），再正式计时 iters 次，
    CUDA 设备在每次计时前后调用 torch.cuda.synchronize() 确保精度。

    Args:
        model:       待测 nn.Module。
        input_shape: 输入张量形状，如 (1, 3, 256, 256)。
        device:      "cpu" 或 "cuda"（字符串）。
        iters:       正式计时次数，默认 50。
        warmup:      热身次数，默认 5。

    Returns:
        平均单次推理耗时，单位毫秒（ms）。
    """
    dev = torch.device(device)
    dummy = torch.randn(*input_shape).to(dev)
    model = model.to(dev)
    model.eval()

    use_cuda = dev.type == "cuda"

    # 热身阶段：让 GPU/CPU 进入稳定状态
    with torch.no_grad():
        for _ in range(warmup):
            model(dummy)
            if use_cuda:
                torch.cuda.synchronize()

    # 正式计时
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
            times.append((t1 - t0) * 1000.0)  # 转为毫秒

    return sum(times) / len(times)


def measure_flops(
    model: nn.Module,
    input_shape: Tuple[int, ...],
) -> Optional[float]:
    """
    利用 thop 库计算模型计算量，返回 GMACs（thop 返回 MAC 数,FLOPs≈2×MAC）；
    thop 不可用时返回 None。

    thop 会向模型注册 hook，若后续还需 measure_runtime，
    建议先调用本函数再测延迟（或在副本上调用）。

    Args:
        model:       待测 nn.Module（将被临时移至 CPU）。
        input_shape: 输入张量形状，如 (1, 3, 256, 256)。

    Returns:
        GMACs（thop 返回 MAC 数,FLOPs≈2×MAC）（float）；若 thop 未安装或 profile 失败则返回 None。
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
# CLI 入口：不绑定任何项目 config/model loader
# ---------------------------------------------------------------------------

def main() -> None:
    """
    命令行入口，接收通用参数。

    项目特定的模型创建（create_model、ConfigLoader 等）
    不在此处实现——调用方（各论文的薄壳脚本）负责实例化模型后
    将其传给上述三个函数。

    当前 CLI 仅提供 --input-shape 展示接口规范；实际使用时
    请在调用脚本中 import measure_model 并直接调用函数。
    """
    parser = argparse.ArgumentParser(
        description="通用模型效率测量工具（不含项目 model loader）"
    )
    parser.add_argument(
        "--input-shape",
        type=int,
        nargs="+",
        default=[1, 3, 256, 256],
        metavar="N",
        help="输入张量形状，例如 --input-shape 1 3 256 256（默认）",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        help="推理设备：cpu 或 cuda（默认 cpu）",
    )
    parser.add_argument(
        "--iters",
        type=int,
        default=50,
        help="正式计时次数（默认 50）",
    )
    parser.add_argument(
        "--warmup",
        type=int,
        default=5,
        help="热身次数（默认 5）",
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
