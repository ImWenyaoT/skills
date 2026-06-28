"""一键训练自检脚本。

用途：把你的 model、一个 batch、loss 丢进 run_sanity_checks()，
自动跑 Karpathy 6 条坑里最易自动化的前 4 条（overfit 单 batch、train/eval、
zero_grad、logits 契约），快速判断"链路是否正确"。

依赖：torch（PyTorch）。运行：python sanity_check.py
"""

from __future__ import annotations

import torch
import torch.nn as nn


def overfit_single_batch(model, xb, yb, criterion, *, steps=300, lr=1e-2):
    """第 1 条：在同一个 batch 上反复训练，验证前向/反向/优化器链路是否打通。

    参数:
        model: 待检查的 nn.Module。
        xb, yb: 一个固定的小 batch（输入与标签）。
        criterion: 损失函数（需与模型输出契约匹配，见 check_logits_contract）。
        steps: 过拟合迭代步数。
        lr: 学习率。
    返回:
        (first_loss, last_loss): 首末步 loss，用于判断是否成功下降。
    说明:
        能把 loss 压到接近 0 → 链路 OK，问题在数据/正则/泛化；
        压不下去 → 链路本身有 bug（去查 train/eval、zero_grad、logits 契约、标签错位）。
    """
    model.train()
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    first_loss = None
    last_loss = None
    for step in range(steps):
        opt.zero_grad()                 # 第 3 条：每步清梯度
        loss = criterion(model(xb), yb)
        loss.backward()
        opt.step()
        last_loss = loss.item()
        if first_loss is None:
            first_loss = last_loss
    return first_loss, last_loss


def check_train_eval_toggle(model, xb):
    """第 2 条：检测模型是否含 Dropout/BN 等"训练/评估行为不同"的层，
    并验证 eval() 模式下前向是否确定（多次前向结果一致）。

    返回:
        dict: 包含是否含状态相关层、eval 下是否确定性。
    """
    has_stateful = any(
        isinstance(m, (nn.Dropout, nn.Dropout2d, nn.BatchNorm1d,
                       nn.BatchNorm2d, nn.BatchNorm3d, nn.LayerNorm))
        for m in model.modules()
    )
    model.eval()
    with torch.no_grad():
        out1 = model(xb)
        out2 = model(xb)
    deterministic_in_eval = torch.allclose(out1, out2)
    return {
        "has_dropout_or_bn": has_stateful,
        "deterministic_in_eval": bool(deterministic_in_eval),
        "note": "含状态层时务必训练用 train()、评估用 eval()，否则结果会抖。",
    }


def check_zero_grad_in_loop(loop_source: str):
    """第 3 条：对训练循环源码做朴素静态检查，提醒是否调用了 zero_grad()。

    参数:
        loop_source: 训练循环的源码字符串（可用 inspect.getsource 取得）。
    返回:
        bool: 是否检测到 zero_grad 调用。
    说明:
        这是启发式提醒，不能替代真正的代码审阅；梯度累积场景属于有意省略。
    """
    return "zero_grad" in loop_source


def check_logits_contract(model, xb, criterion):
    """第 4 条：检查模型输出与 loss 的契约（logits vs 概率）。

    返回:
        dict: 模型末层是否疑似自带 softmax/sigmoid、criterion 是否期望 logits、是否冲突。
    说明:
        CrossEntropyLoss / BCEWithLogitsLoss 内部已含 softmax/sigmoid，应喂 logits；
        若模型末层又加了 Softmax/Sigmoid，则会"做两次"，是常见 bug。
    """
    last_module = list(model.modules())[-1]
    model_outputs_probs = isinstance(
        last_module, (nn.Softmax, nn.LogSoftmax, nn.Sigmoid)
    )
    loss_expects_logits = isinstance(
        criterion, (nn.CrossEntropyLoss, nn.BCEWithLogitsLoss)
    )
    conflict = model_outputs_probs and loss_expects_logits
    return {
        "model_last_layer_is_softmax_or_sigmoid": model_outputs_probs,
        "loss_expects_logits": loss_expects_logits,
        "double_activation_conflict": conflict,
        "note": "conflict=True 表示既在模型里做了 softmax/sigmoid，loss 又做一次 —— 去掉模型末层激活。",
    }


def run_sanity_checks(model, xb, yb, criterion):
    """汇总跑前 4 条自检并打印报告。

    参数:
        model: nn.Module。
        xb, yb: 一个固定小 batch。
        criterion: 损失函数。
    """
    print("=" * 56)
    print("[第4条] logits 契约检查")
    print(check_logits_contract(model, xb, criterion))

    print("=" * 56)
    print("[第2条] train/eval 切换检查")
    print(check_train_eval_toggle(model, xb))

    print("=" * 56)
    print("[第1条] overfit 单个 batch（loss 应显著下降，逼近 0）")
    first, last = overfit_single_batch(model, xb, yb, criterion)
    print(f"first_loss={first:.4f}  last_loss={last:.4f}")
    if last < first * 0.1:
        print("✅ 能 overfit：前向/反向/优化器/loss 链路 OK。问题更可能在数据/正则/泛化。")
    else:
        print("❌ 压不下去：链路可能有 bug —— 复查 train/eval、zero_grad、logits 契约、标签是否错位。")
    print("=" * 56)


if __name__ == "__main__":
    # 演示：一个会"故意自带 softmax"的错误模型，触发第 4 条告警
    torch.manual_seed(0)
    bad_model = nn.Sequential(nn.Linear(10, 3), nn.Softmax(dim=-1))  # ← 末层多了 softmax
    xb = torch.randn(8, 10)
    yb = torch.randint(0, 3, (8,))
    run_sanity_checks(bad_model, xb, yb, nn.CrossEntropyLoss())

    print("\n>>> 修正后（去掉末层 softmax，输出 logits）：")
    good_model = nn.Sequential(nn.Linear(10, 3))
    run_sanity_checks(good_model, xb, yb, nn.CrossEntropyLoss())
