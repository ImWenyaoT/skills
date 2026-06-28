"""6 条经典坑 · "错误写法 vs 正确写法"对照。

每个 pitfall_N() 函数先展示常见的错误写法（注释标出问题），再给出修正版。
当作 code review 时的对照卡片。可直接运行查看第 6 条的数值演示。

依赖：torch。运行：python six_pitfalls_before_after.py
"""

from __future__ import annotations

import torch
import torch.nn as nn


# ──────────────────────────────────────────────────────────────────────
# 第 1 条：不先 overfit 单个 batch
# ──────────────────────────────────────────────────────────────────────
def pitfall_1_overfit_single_batch():
    """错误：一上来就全量 + 增强 + 正则训练，不收敛时无法定位。
    正确：先用一个固定小 batch 反复训，确认链路能把 loss 压到接近 0。"""
    model = nn.Linear(10, 3)
    criterion = nn.CrossEntropyLoss()
    opt = torch.optim.Adam(model.parameters(), lr=1e-2)

    xb = torch.randn(4, 10)              # 固定一个小 batch
    yb = torch.randint(0, 3, (4,))
    model.train()
    for step in range(300):
        opt.zero_grad()
        loss = criterion(model(xb), yb)
        loss.backward()
        opt.step()
    # 期望 loss 逼近 0；做不到说明链路有 bug（去查第 2/3/4 条）
    return loss.item()


# ──────────────────────────────────────────────────────────────────────
# 第 2 条：忘记 train()/eval()
# ──────────────────────────────────────────────────────────────────────
def pitfall_2_train_eval():
    """错误：验证/推理时仍处于 train() —— Dropout 还在丢、BN 用 batch 统计，结果有随机性。
    正确：评估前 model.eval() + torch.no_grad()。"""
    model = nn.Sequential(nn.Linear(10, 10), nn.Dropout(0.5), nn.Linear(10, 3))
    xb = torch.randn(8, 10)

    # ❌ 错误：忘了切 eval，两次前向结果不同
    model.train()
    wrong1, wrong2 = model(xb), model(xb)
    inconsistent = not torch.allclose(wrong1, wrong2)

    # ✅ 正确：eval + no_grad，结果确定
    model.eval()
    with torch.no_grad():
        right1, right2 = model(xb), model(xb)
    consistent = torch.allclose(right1, right2)
    return {"train_mode_inconsistent": inconsistent, "eval_mode_consistent": consistent}


# ──────────────────────────────────────────────────────────────────────
# 第 3 条：忘记 zero_grad()
# ──────────────────────────────────────────────────────────────────────
def pitfall_3_zero_grad():
    """错误：每步不清梯度 —— .backward() 是累加，旧梯度会污染本步更新。
    正确：每步 zero_grad → forward → backward → step。"""
    model = nn.Linear(10, 3)
    opt = torch.optim.SGD(model.parameters(), lr=0.1)
    criterion = nn.CrossEntropyLoss()
    xb, yb = torch.randn(8, 10), torch.randint(0, 3, (8,))

    # ❌ 错误写法（仅示意，勿用）：
    #   for ...:
    #       loss = criterion(model(xb), yb)
    #       loss.backward()        # 梯度不断累加到 .grad
    #       opt.step()             # 用错误的累积梯度更新

    # ✅ 正确写法：
    for _ in range(5):
        opt.zero_grad()            # 关键：先清零
        loss = criterion(model(xb), yb)
        loss.backward()
        opt.step()
    return loss.item()


# ──────────────────────────────────────────────────────────────────────
# 第 4 条：logits vs softmax 搞混
# ──────────────────────────────────────────────────────────────────────
def pitfall_4_logits_vs_softmax():
    """错误：模型末层加了 Softmax，又用 CrossEntropyLoss（内部再 softmax）→ 做了两次。
    正确：模型输出 logits，softmax 交给 loss；推理需要概率时再单独 softmax。"""
    xb = torch.randn(8, 10)
    yb = torch.randint(0, 3, (8,))
    criterion = nn.CrossEntropyLoss()

    # ❌ 错误：双重 softmax，loss 失真
    bad_model = nn.Sequential(nn.Linear(10, 3), nn.Softmax(dim=-1))
    bad_loss = criterion(bad_model(xb), yb).item()

    # ✅ 正确：输出 logits
    good_model = nn.Sequential(nn.Linear(10, 3))
    logits = good_model(xb)
    good_loss = criterion(logits, yb).item()
    probs = logits.softmax(dim=-1)         # 需要概率时单独算
    preds = logits.argmax(dim=-1)          # 取类别直接对 logits argmax
    return {"bad_loss": bad_loss, "good_loss": good_loss,
            "probs_sum_to_one": float(probs.sum(dim=-1).mean()), "preds": preds.tolist()}


# ──────────────────────────────────────────────────────────────────────
# 第 5 条：BatchNorm 前的层带 bias
# ──────────────────────────────────────────────────────────────────────
def pitfall_5_bias_with_bn():
    """错误：Conv/Linear 接 BN 时仍带 bias —— BN 去均值会抵消它，纯冗余参数。
    正确：BN 前的层 bias=False。"""
    # ❌ 多余的 bias
    bad = nn.Sequential(nn.Conv2d(3, 16, 3, bias=True), nn.BatchNorm2d(16))
    # ✅ 去掉 bias
    good = nn.Sequential(nn.Conv2d(3, 16, 3, bias=False), nn.BatchNorm2d(16))
    bad_has_bias = bad[0].bias is not None
    good_has_bias = good[0].bias is not None
    return {"bad_layer_has_redundant_bias": bad_has_bias,
            "good_layer_bias_removed": not good_has_bias}


# ──────────────────────────────────────────────────────────────────────
# 第 6 条：view 当 permute 用
# ──────────────────────────────────────────────────────────────────────
def pitfall_6_view_vs_permute():
    """错误：想把 NCHW 换轴成 NHWC 却用 view/reshape —— 元素按内存顺序硬塞，内容全乱。
    正确：换轴用 permute；合并/拆分维度才用 view/reshape；permute 后 view 需先 contiguous。"""
    x = torch.arange(2 * 3 * 2 * 2).float().reshape(2, 3, 2, 2)  # (N,C,H,W)

    # ❌ 错误：用 reshape 假装换轴（语义错误，得到的不是转置）
    wrong_nhwc = x.reshape(2, 2, 2, 3)            # shape 凑成 NHWC，但内容是乱的

    # ✅ 正确：用 permute 真正换轴
    right_nhwc = x.permute(0, 2, 3, 1)            # (N,H,W,C)，内容正确

    # 验证：把 right_nhwc 换回来应等于原张量；wrong 则不等
    permute_roundtrip_ok = torch.equal(right_nhwc.permute(0, 3, 1, 2), x)
    wrong_is_corrupted = not torch.equal(wrong_nhwc.permute(0, 3, 1, 2), x)

    # permute 后非 contiguous，要 view 须先 contiguous（或直接 reshape）
    flat = right_nhwc.contiguous().view(2, -1)    # 等价 right_nhwc.reshape(2, -1)
    return {"permute_roundtrip_ok": permute_roundtrip_ok,
            "reshape_as_transpose_is_corrupted": wrong_is_corrupted,
            "flat_shape": tuple(flat.shape)}


if __name__ == "__main__":
    torch.manual_seed(0)
    print("第1条 overfit 后 loss:", pitfall_1_overfit_single_batch())
    print("第2条 train/eval     :", pitfall_2_train_eval())
    print("第3条 zero_grad 后 loss:", pitfall_3_zero_grad())
    print("第4条 logits vs softmax:", pitfall_4_logits_vs_softmax())
    print("第5条 bias + BN       :", pitfall_5_bias_with_bn())
    print("第6条 view vs permute :", pitfall_6_view_vs_permute())
