---
name: training-models
description: Neural-network training discipline and silent-failure debugging. Use when training fails silently, loss is not decreasing, accuracy is stuck, gradients explode or vanish, train/eval results disagree, inference is wrong, or a one-batch overfit check fails; also use for reviewing a training loop or setting up a from-scratch training pipeline. 中文触发包括：loss 不下降、acc 卡住、梯度异常、训练/验证不一致、推理错误、过拟合单 batch 失败、检查训练循环、从零搭训练流程。
---

# 神经网络训练：失败诊断与可靠搭建

神经网络常会在代码没有报错时静默失败。先建立最小、可复现的反馈循环，再逐步恢复数据、正则化和模型复杂度；不要用盲目调参代替链路验证。

## 先判断任务类型

- **训练已经异常**：固定一个失败现象和复现命令，按下方热路径定位。
- **审查训练循环**：先核对模式切换、梯度生命周期、输出与 loss 的契约，再运行最小 sanity check。
- **从零搭建训练流程**：按 [完整六阶段训练配方](references/karpathy-recipe.md) 从数据检查推进到调参与集成，每次只增加一种复杂度。

## 热路径：只做最高信号检查

1. **固定最小复现**：固定随机种子，关闭增强、dropout、weight decay 等非必要变量，记录同一命令下的初始 loss、训练 loss 和关键指标。
2. **验证初始 loss**：`n` 类均匀分类的交叉熵应接近 `log(n)`。数量级不符时先查标签、初始化、末层 bias、logits 尺度和 loss 输入契约。
3. **过拟合一个固定小 batch**：反复训练 2～8 个样本，把 loss 压到接近 0，并直接核对 prediction 与 label。失败说明前向、反向、优化器、loss 或标签链路仍有问题；成功后再查数据、正则化与泛化。
4. **做 input-independent baseline**：将输入置零后重训。若表现与真实输入接近，优先排查标签泄漏、索引错位或模型根本没有使用输入。

若第 3 步失败，优先检查：

- 训练前 `model.train()`，验证/推理前 `model.eval()`；
- 每个 step 正确执行 `zero_grad()` → forward → `backward()` → `step()`；
- `CrossEntropyLoss` / `BCEWithLogitsLoss` 接收 logits，没有重复 softmax/sigmoid；
- 张量换轴使用 `permute`/`transpose`，合并或拆分维度使用 `reshape`/`view`，并核对标签没有错位。

完整的症状、原因、检查和修复方式见 [14 条失败自检清单](references/checklist.md)。

## 交付要求

诊断或修复完成时，必须给出：

- 可重复运行的最小复现命令或脚本；
- 初始 loss、单 batch overfit、input-independent baseline 中适用检查的实际结果；
- 命中的陷阱、证据与对应修复；
- 修复后的同条件对比结果；
- 尚未通过的检查及下一步（如有）。

只有当失败现象在原最小复现下消失、相关 sanity check 通过，且没有用关闭验证或放宽断言来掩盖问题时，才算完成。从零搭建任务还需明确当前通过了六阶段中的哪一阶段，以及进入下一阶段的证据。

## 可运行入口

- [sanity_check.py](sample_codes/getting-started/sanity_check.py)：初始 loss、input-independent baseline 等链路检查。
- [correct_training_loop.py](sample_codes/getting-started/correct_training_loop.py)：训练/验证循环模板。
- [six_pitfalls_before_after.py](sample_codes/common-patterns/six_pitfalls_before_after.py)：经典 6 条错误与修复对照。
- [extra_pitfalls_before_after.py](sample_codes/common-patterns/extra_pitfalls_before_after.py)：扩展 8 条错误与修复对照。

## 深入参考

- [完整六阶段训练配方](references/karpathy-recipe.md)：数据检查、骨架与 baseline、过拟合、正则化、调参、榨干余量。
- [完整 14 条失败自检清单](references/checklist.md)：逐条的症状、原因、检查、修复和排查顺序。
