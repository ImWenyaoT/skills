---
name: debugging-nn-training
description: 神经网络训练常见错误自检清单（基于 Karpathy "A Recipe for Training Neural Networks" 的 6 条经典坑）。当用户的 PyTorch/深度学习训练出现 loss 不下降、train/eval 指标不一致、梯度异常、acc 卡住、推理结果错乱等问题，或在做 code review / 写训练循环 / 排查"明明代码看着对但就是不收敛"时使用。覆盖 overfit-single-batch、train/eval mode、zero_grad、logits-vs-softmax、bias+BatchNorm、view-vs-permute 六大陷阱的症状识别、最小复现与修复。
---

# 神经网络训练常见错误自检

训练神经网络是一个"leaky abstraction"：代码不报错不代表训练正确。大多数 bug 是**静默的**——网络照样跑、loss 照样有数字，只是悄悄学错或学不动。本 skill 把 Karpathy《A Recipe for Training Neural Networks》中最高频的 6 条坑固化成一份**可逐条对照的自检清单**，每条都给出「症状 → 为什么 → 怎么查 → 怎么改」。

> 用法：拿到一个"训练不对劲"的现场，从下面 6 条逐条排查。多数收敛类问题命中前 3 条，多数"结果错乱/精度怪"问题命中后 3 条。

## 自检清单速查表

| # | 陷阱 | 典型症状 | 一句话自检 |
|---|------|----------|-----------|
| 1 | 不先 overfit 单个 batch | loss 卡住、不知道是数据问题还是模型问题 | 喂同一个 batch 反复训，loss 能否降到 ~0？ |
| 2 | 忘记 `model.train()` / `model.eval()` | train 好、eval 差/抖动，或验证集每次跑结果不同 | 验证/推理前是否切到 `eval()`？ |
| 3 | 忘记 `optimizer.zero_grad()` | loss 不降或诡异震荡、显存随 step 上涨 | 每个 step 是否清了梯度？ |
| 4 | logits 与 softmax/概率搞混 | loss 偏高不降、用了双重 softmax、数值不稳 | loss 函数吃的是 logits 还是概率？对上了吗？ |
| 5 | BatchNorm 前的层带了 bias | 不致命但冗余；BN 行为不符预期 | conv/linear 接 BN 时 `bias` 是否设为 False？ |
| 6 | 用 `view` 当 `permute` 用（或反之） | 张量"形状对、内容乱"，精度莫名其妙崩 | 你要的是换轴顺序还是重排内存？用对函数了吗？ |

## 扩展自检清单（推文未列，但同样高频）

Karpathy 原文只列了上面 6 条；下面 8 条**不在原推文里**，但实战中同样高频、且多数同样"静默"——一并纳入排查。

| # | 陷阱 | 典型症状 | 一句话自检 |
|---|------|----------|-----------|
| 7 | 训练 DataLoader 没 `shuffle=True` | loss 周期性抖动、收敛慢、对样本顺序敏感 | 训练 loader shuffle 了吗？数据是否按类别/时间排序？ |
| 8 | loss 没对 batch 取平均 / reduction 不一致 | 换 batch_size 就得重调 LR、多任务 loss 尺度失衡 | loss 是 `mean` 吗？手动累加除以样本数了吗？ |
| 9 | 学习率没 warmup / 没 scheduler / 量级离谱 | 前几百步发散或 NaN、后期不收尾 | 大模型/大 batch 有 warmup 吗？有 LR 调度吗？ |
| 10 | 归一化统计量泄漏 / 推理忘了归一化 | val/test 虚高，或线上比线下差很多 | mean/std 只用训练集算、各阶段复用同一套了吗？ |
| 11 | 没固定随机种子 | 结果每次不同，实验无法对比、改动无法归因 | torch/numpy/python/cuda 的种子都设了吗？ |
| 12 | GPU 上累加 loss 不 `.item()`/`.detach()` | 显存随 step 持续上涨直到 OOM | 统计 loss 用的是 `.item()` 还是带计算图的 tensor？ |
| 13 | `CrossEntropyLoss` 的 target 类型/形状不对 | 报 dtype 错，或把 one-hot/float 当 target 学错 | 多分类 target 是 `(N,)` 的 `long` 类别索引吗？ |
| 14 | weight decay 加到 bias/BN/LayerNorm 上 | 不致命，但正则略偏、norm 参数被错误衰减 | 1-D 的 bias/norm 参数排除 weight decay 了吗？ |

完整 14 条逐条说明见 [references/checklist.md](references/checklist.md)。

## 推荐的排查顺序（Recipe）

1. **先建立信任的基线**：固定随机种子，关掉数据增强，用最简模型。
2. **第 1 条：overfit 一个 batch**。这是分水岭——能 overfit 说明前向/反向/优化器/loss 链路是通的，问题在数据或正则；不能 overfit 说明链路本身有 bug（往往就是第 2~4 条）。
3. **第 2、3 条**：检查训练循环骨架（`train()/eval()`、`zero_grad()`），它们是"代码看着对但就是不收敛"的头号嫌疑。
4. **第 4 条**：核对 loss 与模型输出的契约（logits vs 概率）。
5. **第 6 条**：若是"维度操作后结果错乱"，查 `view`/`reshape`/`permute`/`transpose` 用法。
6. **第 5 条**：收尾的整洁性检查（BN 前去 bias）。
7. **扩展坑（7~14）**：上面跑通后，按"训练策略层"复查——数据 `shuffle`、loss 是否按样本平均、LR 是否有 warmup/调度、归一化统计量有没有泄漏、随机种子是否固定。这些不影响"链路对不对"，但直接决定"训得好不好、能不能复现"。

## Quick Start

- 一键自检脚本（把你的 model + 一个 batch 丢进去，自动跑前 4 条检查）：
  [sample_codes/getting-started/sanity_check.py](sample_codes/getting-started/sanity_check.py)
- 一份"正确的"训练循环模板（同时规避第 2/3/4 条）：
  [sample_codes/getting-started/correct_training_loop.py](sample_codes/getting-started/correct_training_loop.py)
- 原 6 条坑的"错误 vs 正确"对照代码：
  [sample_codes/common-patterns/six_pitfalls_before_after.py](sample_codes/common-patterns/six_pitfalls_before_after.py)
- 扩展 8 条（7~14）的"错误 vs 正确"对照代码（含 reduction、warmup、param group 等可运行演示）：
  [sample_codes/common-patterns/extra_pitfalls_before_after.py](sample_codes/common-patterns/extra_pitfalls_before_after.py)

## 核心要点（必记）

- **静默失败是常态**：训练 bug 通常不抛异常。不要相信"没报错=对了"，要相信指标和最小复现。
- **overfit 单 batch 是第一性检查**：它把"链路 bug"和"泛化/数据问题"一刀切开，永远先做这一步。
- **三件套必须配齐**：`zero_grad()` → `forward` → `loss.backward()` → `optimizer.step()`，且循环外正确切换 `train()/eval()`。
- **明确 logits 契约**：`nn.CrossEntropyLoss` / `BCEWithLogitsLoss` 吃 **logits**（不要自己再 softmax/sigmoid）；`NLLLoss` 吃 **log 概率**。
- **换轴用 `permute`/`transpose`，合并/拆分维度用 `view`/`reshape`**；非 contiguous 张量上 `view` 会报错或需先 `.contiguous()`。
- **工程卫生同样决定成败**（扩展坑）：训练数据要 `shuffle`、loss 要按**样本数**平均、统计指标用 `.item()` 累加、归一化统计量**只用训练集**算并各阶段复用。
- **LR 是头号超参**：大模型/大 batch 配 warmup + scheduler；`reduction='sum'` 的梯度量级是 `'mean'` 的 batch_size 倍，换 batch 务必同步看 LR。
- **固定随机种子**（torch/numpy/python/cuda）是为了**实验可对比、改动可归因**——不是为了挑一个"好种子"。

## Learn More（深入查询）

本 skill 聚焦 PyTorch/通用深度学习实践。以下为按需深挖的查询入口（PyTorch 官方文档 / Karpathy 原文）：

| 主题 | 怎么找 |
|------|--------|
| Karpathy 原始"训练配方"全文 | 搜索：`Karpathy "A Recipe for Training Neural Networks"`（karpathy.github.io/2019/04/25/recipe/） |
| `model.train()` / `eval()` 对 Dropout/BN 的精确影响 | PyTorch 文档：`torch.nn.Module.train` / `nn.Dropout` / `nn.BatchNorm2d` |
| `CrossEntropyLoss` 是否含 softmax、输入约定 | PyTorch 文档：`torch.nn.CrossEntropyLoss` / `BCEWithLogitsLoss` |
| `view` vs `reshape` vs `permute` 的内存语义 | PyTorch 文档：`torch.Tensor.view` / `torch.reshape` / `torch.permute` / `contiguous` |
| 梯度累积、`zero_grad(set_to_none=True)` 细节 | PyTorch 文档：`torch.optim.Optimizer.zero_grad` |
