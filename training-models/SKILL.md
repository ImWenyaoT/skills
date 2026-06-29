---
name: training-models
description: Engineers neural-network/deep-learning training end-to-end and debugs its silent failures — the full Karpathy lifecycle (inspect data, build an end-to-end skeleton with dumb baselines, overfit, regularize, tune, squeeze). Default stack Python + PyTorch with uv/ruff/ty/pytest; also JAX/TF. Use when loss does not decrease, train/eval metrics disagree, gradients explode/vanish, accuracy is stuck, inference is wrong, a model cannot overfit one batch, or when setting up / sanity-checking / structuring a training run from scratch; also for training-loop code review. Covers Karpathy's full "Recipe for Training Neural Networks" (6 stages) plus an extended engineering checklist, minimal reproductions, and fixes.
---

# 神经网络训练:配方 + 错误自检

训练神经网络会**静默失败**。Karpathy 在《A Recipe for Training Neural Networks》里点出两个根因:① 它是 **leaky abstraction**——`backprop + SGD` 不会自动让网络 work,一旦偏离标准任务(如 ImageNet 分类),隐藏的复杂度就冒出来;② 它**不报错地失败**——语法全对、照常训练,只是悄悄学错(翻转的标签、off-by-one、初始化不当)。对策是他那句方法论:**从简单到复杂地搭,保持 thorough/defensive/paranoid、对几乎每一件事都痴迷可视化;suffering 是自然的,但能靠这些品质缓解——与成功最相关的是耐心与对细节的执着。**

本 skill 因此分两半,配合使用:
- **训练配方(6 阶段)**——预防并定位 bug 的**搭建顺序**(下一节)。很多 bug 其实是**跳过了某个阶段**。
- **bug 自检清单(14 条)**——已经出事时的**反向排查**(再下面),每条「症状 → 为什么 → 怎么查 → 怎么改」。

> 用法:从零搭训练用「训练配方」按阶段推进;现场"训练不对劲"则跳到「自检清单」逐条排查——多数收敛类问题命中前 3 条,多数"结果错乱/精度怪"命中后 3 条。

## 技术栈约定

本 skill 默认 **Python ML/DL 栈**(示例、脚本、修复都按此):

- **语言/框架**:Python + **PyTorch**(主);JAX/TF 仅在个别 tip 处做 API 旁注。
- **工程工具**:`uv`(依赖/虚拟环境)、`ruff`(lint + format)、`ty`(类型检查)、`pytest`(测试);跑脚本优先 `uv run`,提交前 `ruff check` + `ty` 应过。

> 这是 ML/DL/AI 域的栈;web 域(TypeScript + Node/Bun)是另一回事,不在本 skill。

## 训练配方:从简单到复杂(Karpathy 6 阶段)

> 核心纪律:**别一上来就堆复杂度。** 每个阶段先建立一个"可信赖的状态",再小步加复杂度;**每加一步前先写下"具体假设"(预期会发生什么),再用实验验证或调查到找到问题**——这样一旦指标变坏,你立刻知道是刚加的那一步。逐 tip 的「为什么 + 怎么做」详解见 [references/karpathy-recipe.md](references/karpathy-recipe.md)。

**阶段 1 · 与数据合二为一(become one with the data)**
- 写代码前先**人肉看几千个样本**:分布、模式、类别不平衡、标签质量、离群点、重复/损坏样本。
- 写脚本去搜索 / 过滤 / 可视化分布与异常值——**离群点几乎总能直接暴露数据/预处理 bug**(最高性价比探针)。
- **留意"你自己怎么人工分类"→ 暗示该用什么架构/预处理**(局部 vs 全局特征、空间位置是否重要、能下采样多少、标签多吵)。
- **网络=数据集的压缩版**:训练后回看 mispredictions 与数据对照,把"看数据"做成贯穿训练前后的闭环。

**阶段 2 · 搭端到端骨架 + 拿到"笨 baseline"(skeleton + dumb baselines)** —— sanity check 最密集的一阶段:
- **固定随机种子**(可复现)。
- **先简化**:关掉数据增强等一切花活。
- **eval 加足有效位**,并在整个测试集上评(别只看一个 batch)。
- **验证 init 时的 loss**:n 类 softmax 在 init 时 CrossEntropy 应 ≈ `log(n)`(回归 L2 ≈ 标签方差、Huber 同理可推),对不上就是初始化/末层 bias 不对。
- **init well**:把末层 bias 设成合理先验(回归设为标签均值、不平衡分类按基频),省得前几百步只在"学先验"。
- **human baseline**:评估你自己的人类准确率作为目标上限,或把测试集标两遍(一份当预测、一份当 ground truth)估人类水平。
- **input-independent baseline**:把输入置零再训,若 loss 仍能降到和真实输入差不多 → 模型根本没在用输入(信息泄漏/记忆标签)。
- **overfit 一个 batch**:压到接近 0,证明前向/反向/优化器/loss 链路是通的(本 skill 的第一性检查);**同图叠画 label 与 prediction,确认最低 loss 时逐点对齐**,不齐=有 bug、别进下一步。
- **验证训练 loss 随容量增加而下降**。
- **在"喂进网络前一刻"可视化**真正进网络的 `x`/`y`(不是 dataset 里的,是 `y_hat = model(x)` 那一刻的张量)。
- **可视化预测的动态**:固定一批测试样本,看训练过程中预测怎么演化——抖得厉害说明不稳定。
- **用 backprop 画依赖**:故意只对某个样本的 loss 求导,确认只有它的输入有非零梯度——专抓"批次间信息串漏"。
- **从特例泛化**:先把一个具体小情形硬写对,再泛化成通用循环,别一上来写通用版。

**阶段 3 · 过拟合(overfit)** —— 先做到"训练集上能压到很低",再谈泛化:
- **别逞英雄(don't be a hero)**:抄相关论文里跑通的成熟架构,别自创。
- **Adam 安全**:先用 Adam、`lr≈3e-4`。
- **一次只加一个复杂度**(信号/模块/数据源逐个加,别一把梭)。
- **别照搬别领域的 lr decay 默认值**:衰减常和数据集大小绑定,照抄会过早衰减。

**阶段 4 · 正则化(regularize)** —— 牺牲一点训练拟合换泛化,大致优先级:
- **拿更多真实数据(最有效)** → 数据增强 → 预训练 → **坚持监督学习**(无监督在 CV 至今无强结果,NLP/BERT 例外)→ 降输入维度 → 减小模型 → 减小 batch → **dropout**(ConvNet 用 `dropout2d`,且与 BN 不太合)→ 调大 **weight decay** → **early stopping**;之后可再试更大的模型(其 early-stopped 性能常优于小模型)。
- **收尾确认**:可视化第一层权重(应有合理边缘,像噪声=有问题)、查内部 activations 有无怪异 artifact。

**阶段 5 · 调参(tune)**
- **随机搜索 > 网格搜索**(网络对某些超参远比另一些敏感)。贝叶斯超参优化工具有人用得好,但 Karpathy 本人更靠人工经验——别当银弹。

**阶段 6 · 榨干余量(squeeze out the juice)**
- **模型集成**几乎稳赚 ~2%;**让模型训练得比你以为的更久**(常常还在涨)。

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

## 出问题后的排查顺序(逆向口诀)

> 上面「训练配方」讲的是"怎么搭才不长 bug";这里讲的是"**已经有 bug 了怎么快速定位**"。两者共用同一把钥匙——**overfit 单 batch**(配方阶段 2 的 sanity check,也是这里的分水岭)。

1. **先建立信任的基线**：固定随机种子，关掉数据增强，用最简模型。
2. **第 1 条：overfit 一个 batch**。这是分水岭——能 overfit 说明前向/反向/优化器/loss 链路是通的，问题在数据或正则；不能 overfit 说明链路本身有 bug（往往就是第 2~4 条）。
3. **第 2、3 条**：检查训练循环骨架（`train()/eval()`、`zero_grad()`），它们是"代码看着对但就是不收敛"的头号嫌疑。
4. **第 4 条**：核对 loss 与模型输出的契约（logits vs 概率）。
5. **第 6 条**：若是"维度操作后结果错乱"，查 `view`/`reshape`/`permute`/`transpose` 用法。
6. **第 5 条**：收尾的整洁性检查（BN 前去 bias）。
7. **扩展坑（7~14）**：上面跑通后，按"训练策略层"复查——数据 `shuffle`、loss 是否按样本平均、LR 是否有 warmup/调度、归一化统计量有没有泄漏、随机种子是否固定。这些不影响"链路对不对"，但直接决定"训得好不好、能不能复现"。

## Quick Start

- 一键自检脚本（把你的 model + 一个 batch 丢进去，自动跑链路 4 条 + 配方阶段 2 的两条
  sanity check：**验证 init loss** 与 **input-independent baseline**）：
  [sample_codes/getting-started/sanity_check.py](sample_codes/getting-started/sanity_check.py)
- 一份"正确的"训练循环模板（同时规避第 2/3/4 条）：
  [sample_codes/getting-started/correct_training_loop.py](sample_codes/getting-started/correct_training_loop.py)
- 原 6 条坑的"错误 vs 正确"对照代码：
  [sample_codes/common-patterns/six_pitfalls_before_after.py](sample_codes/common-patterns/six_pitfalls_before_after.py)
- 扩展 8 条（7~14）的"错误 vs 正确"对照代码（含 reduction、warmup、param group 等可运行演示）：
  [sample_codes/common-patterns/extra_pitfalls_before_after.py](sample_codes/common-patterns/extra_pitfalls_before_after.py)

## 核心要点（必记）

- **静默失败是常态**：训练 bug 通常不抛异常。不要相信"没报错=对了"，要相信指标和最小复现。
- **从简单到复杂、一次只加一个变量**：每阶段先建立可信赖状态再加复杂度,指标一坏就知道是刚加的那步;能抄成熟架构就别逞英雄。
- **init 阶段两条必做 sanity check**：`验证 init loss ≈ log(n_classes)`(对不上=初始化/末层 bias 错)、`input-independent baseline`(置零输入仍能学好=模型没在用输入)。
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
