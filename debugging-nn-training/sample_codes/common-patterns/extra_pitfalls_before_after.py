"""扩展 8 条坑（第 7~14 条）· "错误写法 vs 正确写法"对照。

这 8 条不在 Karpathy 原推文中，但实战同样高频、且多数同样"静默"。
每个 pitfall_N() 函数演示问题与修正，可直接运行查看数值佐证。

依赖：torch。运行：python extra_pitfalls_before_after.py
"""

from __future__ import annotations

import math

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset


# ──────────────────────────────────────────────────────────────────────
# 第 7 条：训练 DataLoader 没 shuffle=True
# ──────────────────────────────────────────────────────────────────────
def pitfall_7_shuffle():
    """错误：训练数据按类别排序却不 shuffle —— 单个 batch 全同类，BN 统计/梯度被带偏。
    正确：训练 loader shuffle=True；验证/测试 shuffle=False。"""
    x = torch.arange(8).float().unsqueeze(1)
    y = torch.tensor([0, 0, 0, 0, 1, 1, 1, 1])      # 故意按类别排序
    ds = TensorDataset(x, y)

    no_shuffle = DataLoader(ds, batch_size=4, shuffle=False)
    shuffled = DataLoader(ds, batch_size=4, shuffle=True)

    first_no = next(iter(no_shuffle))[1].tolist()    # ❌ 首个 batch 全是 0 类
    first_sh = next(iter(shuffled))[1].tolist()      # ✅ 类别被打散
    return {
        "no_shuffle_first_batch_labels": first_no,
        "shuffled_first_batch_labels": first_sh,
        "note": "不 shuffle 时首个 batch 全同类，梯度方向与 BN 统计被带偏",
    }


# ──────────────────────────────────────────────────────────────────────
# 第 8 条：loss 没对 batch 取平均 / reduction 不一致
# ──────────────────────────────────────────────────────────────────────
def pitfall_8_loss_reduction():
    """错误：用 reduction='sum'（或手动累加不除 N）—— 梯度量级被 batch_size 放大，换 batch 就发散。
    正确：用 'mean'；变长序列按有效 token 数平均。
    数值佐证：grad(sum) 恰为 grad(mean) 的 batch_size 倍。"""
    torch.manual_seed(0)
    x = torch.randn(16, 4)
    t = torch.randn(16, 1)
    w = torch.randn(4, 1, requires_grad=True)
    se = (x @ w - t) ** 2

    g_mean = torch.autograd.grad(se.mean(), w, retain_graph=True)[0]
    g_sum = torch.autograd.grad(se.sum(), w)[0]
    ratio = (g_sum / g_mean).mean().item()           # ≈ batch_size = 16
    return {"batch_size": x.size(0), "grad_ratio_sum_over_mean": round(ratio, 3)}


# ──────────────────────────────────────────────────────────────────────
# 第 9 条：学习率没 warmup / 没 scheduler
# ──────────────────────────────────────────────────────────────────────
def pitfall_9_warmup():
    """错误：大 batch/Transformer 直接用目标 LR 起步 —— 前几百步易发散/NaN。
    正确：线性 warmup 升到目标 LR，再余弦衰减收尾。"""
    model = nn.Linear(4, 2)
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3)

    def warmup_cosine(step, warmup=5, total=20):
        """warmup 段线性升、之后余弦降的 LR 系数。"""
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
        sched.step()
        lrs.append(round(opt.param_groups[0]["lr"], 6))
    return {"lr_curve_first10": lrs[:10], "note": "前 5 步线性 warmup 升，之后余弦降"}


# ──────────────────────────────────────────────────────────────────────
# 第 10 条：归一化统计量泄漏 / 推理忘了归一化
# ──────────────────────────────────────────────────────────────────────
def pitfall_10_normalization():
    """错误：用 train+test 合并算 mean/std（信息泄漏），或推理忘用同一套 stats。
    正确：mean/std 只在训练集拟合，保存后各阶段复用。"""
    torch.manual_seed(0)
    train_x = torch.randn(100, 3) * 5 + 2
    test_x = torch.randn(20, 3) * 5 + 2

    # ✅ 只用训练集拟合，复用到 test
    mu = train_x.mean(0, keepdim=True)
    sd = train_x.std(0, keepdim=True) + 1e-8
    test_norm = (test_x - mu) / sd

    # ❌ 泄漏：用全量（含 test）算 stats
    mu_leak = torch.cat([train_x, test_x], 0).mean(0, keepdim=True)
    leaked = not torch.allclose(mu, mu_leak)
    return {
        "stats_fit_on_train_only": True,
        "leaking_changes_stats": bool(leaked),
        "test_norm_mean_approx0": round(test_norm.mean().item(), 3),
    }


# ──────────────────────────────────────────────────────────────────────
# 第 11 条：没固定随机种子 → 不可复现
# ──────────────────────────────────────────────────────────────────────
def pitfall_11_seed(seed=42):
    """错误：不设种子 —— 每次结果不同，改动无法归因。
    正确：统一设 torch/numpy/python/cuda 种子；同样种子下两次随机应完全一致。"""

    def seed_everything(s):
        """统一固定各 RNG，保证实验可复现可对比。"""
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
# 第 12 条：GPU 上累加 loss 不 .item() → 显存泄漏
# ──────────────────────────────────────────────────────────────────────
def pitfall_12_loss_accumulation():
    """错误：total_loss += loss（带计算图的 tensor）—— 每个 batch 的图被挂住，显存涨到 OOM。
    正确：累加 loss.item()（纯 float），按样本数加权后再平均。"""
    model = nn.Linear(4, 1)
    x, t = torch.randn(8, 4), torch.randn(8, 1)
    loss = ((model(x) - t) ** 2).mean()

    bad_accumulator = loss            # ❌ requires_grad=True，累加会驻留计算图
    good_accumulator = loss.item()    # ✅ Python float，无图
    return {
        "bad_has_grad_graph": bool(bad_accumulator.requires_grad),
        "good_is_python_float": isinstance(good_accumulator, float),
    }


# ──────────────────────────────────────────────────────────────────────
# 第 13 条：CrossEntropyLoss 的 target 类型/形状不对
# ──────────────────────────────────────────────────────────────────────
def pitfall_13_target_dtype():
    """错误：把 one-hot/float 当 CrossEntropyLoss 的 target（旧版报错、新版语义可能非预期）。
    正确：多分类 target 是 (N,) 的 long 类别索引；多标签才用 (N,C) 的 float + BCEWithLogitsLoss。"""
    logits = torch.randn(8, 3)
    y_idx = torch.randint(0, 3, (8,)).long()         # ✅ (N,) long 索引
    ce = nn.CrossEntropyLoss()(logits, y_idx).item()

    is_valid_target = (y_idx.dtype == torch.long and y_idx.dim() == 1)
    return {"target_is_long_1d_index": bool(is_valid_target), "ce_loss": round(ce, 4)}


# ──────────────────────────────────────────────────────────────────────
# 第 14 条：weight decay 误加到 bias / BN / LayerNorm 上
# ──────────────────────────────────────────────────────────────────────
def split_param_groups(model, weight_decay=1e-2):
    """把参数分两组：权重矩阵走 weight_decay，bias 与 1-D 的 norm 参数 weight_decay=0。"""
    decay, no_decay = [], []
    for name, p in model.named_parameters():
        if not p.requires_grad:
            continue
        if p.ndim <= 1 or name.endswith(".bias"):    # bias / BN / LayerNorm 的 1-D 参数
            no_decay.append(p)
        else:
            decay.append(p)
    return [
        {"params": decay, "weight_decay": weight_decay},
        {"params": no_decay, "weight_decay": 0.0},
    ]


def pitfall_14_weight_decay():
    """错误：对全部参数施加同一 weight decay —— bias/norm 参数被错误衰减。
    正确：构造两组 param group，bias/norm 排除 weight decay。"""
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
    print("第7条 shuffle          :", pitfall_7_shuffle())
    print("第8条 loss reduction   :", pitfall_8_loss_reduction())
    print("第9条 warmup           :", pitfall_9_warmup())
    print("第10条 normalization   :", pitfall_10_normalization())
    print("第11条 seed            :", pitfall_11_seed())
    print("第12条 loss accumulation:", pitfall_12_loss_accumulation())
    print("第13条 target dtype    :", pitfall_13_target_dtype())
    print("第14条 weight decay    :", pitfall_14_weight_decay())
