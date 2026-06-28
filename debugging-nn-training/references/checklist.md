# 6 条经典坑 · 逐条自检详解

每条遵循统一结构：**症状 → 为什么会错 → 怎么查 → 怎么改**。代码以 PyTorch 为例，思路通用。

---

## 1. 不先 overfit 单个 batch

**症状**
- loss 卡在某个值不动，但你分不清是"数据/标签坏了"、"模型容量不够"、"学习率不对"还是"代码有 bug"。
- 调了半天超参毫无头绪。

**为什么会错**
- 直接上全量数据 + 正则 + 增强训练，一旦不收敛，变量太多无法定位。失去了"链路是否正确"这个最基本的判据。

**怎么查**
- 取**一个固定的小 batch**（比如 2~8 个样本），关闭 dropout/数据增强/weight decay，反复在这同一个 batch 上训练几百步。
- 观察 loss 是否能降到接近 0（分类任务可达到接近 0 的 train loss、100% train acc）。

**怎么改**
- **能 overfit** → 前向、反向、优化器、loss 链路是通的。问题在数据规模、正则、泛化或学习率调度，往后排查第 2~6 条之外的"训练策略层"。
- **不能 overfit** → 链路本身有 bug。立刻去查第 2/3/4 条（没 `zero_grad`、没切 `train()`、loss 与输出契约不对、标签错位、梯度没回传到该更新的参数等）。
- 顺手检查：loss 初始值是否合理（N 分类交叉熵初始 loss 应约为 `ln(N)`，不是这个数量级说明 logits 尺度/初始化/标签有问题）。

```python
# 取一个 batch，反复喂，loss 必须能掉下去
xb, yb = next(iter(loader))
model.train()
for step in range(500):
    optimizer.zero_grad()
    loss = criterion(model(xb), yb)
    loss.backward()
    optimizer.step()
    if step % 50 == 0:
        print(step, loss.item())   # 期望：稳步逼近 0
```

---

## 2. 忘记切换 `model.train()` / `model.eval()`

**症状**
- 验证集指标比训练集差很多，或验证/推理结果**每次跑都不一样**（有随机性）。
- BatchNorm 在小 batch 评估时统计量乱跳；模型在生产推理时表现和训练时对不上。

**为什么会错**
- `Dropout`、`BatchNorm` 等层在训练和评估时**行为不同**：
  - 训练模式：Dropout 随机置零；BN 用当前 batch 的均值/方差并更新 running stats。
  - 评估模式：Dropout 关闭（全保留）；BN 用累积的 running mean/var。
- 验证/推理时仍处于 `train()` 模式 → Dropout 仍在丢、BN 用 batch 统计 → 结果有随机性且不稳。
- 反过来，训练时误处于 `eval()` → 正则失效、BN 不更新统计。

**怎么查**
- 检查训练循环：每个 epoch 训练段前是否 `model.train()`，验证/测试/推理段前是否 `model.eval()`。
- 推理时是否同时用了 `with torch.no_grad():`（省显存、加速，且明确意图）。

**怎么改**
```python
# 训练阶段
model.train()
for xb, yb in train_loader:
    ...

# 验证/推理阶段
model.eval()
with torch.no_grad():
    for xb, yb in val_loader:
        ...
```
- 二者要**成对出现**。封装成 `train_one_epoch()` / `evaluate()` 函数，把模式切换写进函数开头，避免漏切。

---

## 3. 忘记 `optimizer.zero_grad()`

**症状**
- loss 不降、或出现诡异的震荡/发散。
- 训练越跑越慢、显存随 step 缓慢上涨（梯度图/累积相关）。

**为什么会错**
- PyTorch 的 `.backward()` 是**累加**梯度到 `.grad`，不是覆盖。若不在每个 step 前清零，本 step 的梯度会叠加上之前所有 step 的旧梯度 → `optimizer.step()` 用的是错误的累积梯度 → 更新方向错乱。

**怎么查**
- 确认训练循环里 `optimizer.zero_grad()` 出现在每个 step 的 `backward()` **之前**。
- 注意顺序：`zero_grad()` → `forward` → `loss.backward()` → `optimizer.step()`。

**怎么改**
```python
for xb, yb in train_loader:
    optimizer.zero_grad()          # 1. 清梯度（或 zero_grad(set_to_none=True)）
    out = model(xb)                # 2. 前向
    loss = criterion(out, yb)
    loss.backward()                # 3. 反向（累加到 .grad）
    optimizer.step()               # 4. 更新
```
- **例外（梯度累积）**：若刻意做 gradient accumulation，则每 N 个 micro-step 才 `step()` + `zero_grad()` 一次——这是有意的累加，不是 bug。区别在于"是否是你主动设计的"。

---

## 4. logits 与 softmax / 概率搞混

**症状**
- 分类 loss 偏高且降不动；或训练能动但数值不稳、容易 NaN。
- 推理输出的"概率"加起来不为 1，或被 argmax 出奇怪结果。

**为什么会错**
- 不同 loss 对输入的约定不同，最常见的是**对模型输出做了多余的 softmax/sigmoid**：
  - `nn.CrossEntropyLoss` = `LogSoftmax` + `NLLLoss`，**内部已含 softmax**，必须喂**原始 logits**。若你先 `softmax` 再传进去，等于做了两次 → loss 失真。
  - `nn.BCEWithLogitsLoss` **内部含 sigmoid**，喂 logits；用了它就别再自己 sigmoid。
  - `nn.NLLLoss` 吃的是 **log 概率**（前面要接 `log_softmax`）。
  - `nn.BCELoss` 吃 **[0,1] 概率**（前面要 sigmoid）——数值稳定性不如 `BCEWithLogitsLoss`。

**怎么查**
- 看模型最后一层：有没有自己加 `Softmax`/`Sigmoid`？
- 看 loss 类型：它期望 logits 还是概率？二者必须**正好对上一次**，不能零次也不能两次。
- 推理时再单独决定是否需要 softmax（多数只需 `argmax(logits)` 即可，argmax 不受单调的 softmax 影响）。

**怎么改**

| 任务 | 推荐 loss | 模型输出应是 | 不要做 |
|------|-----------|-------------|--------|
| 多分类 | `CrossEntropyLoss` | 原始 logits | 别在输出层加 softmax |
| 二分类/多标签 | `BCEWithLogitsLoss` | 原始 logits | 别自己 sigmoid |
| 已 log_softmax | `NLLLoss` | log 概率 | — |

```python
# 正确：输出 logits，loss 内部处理 softmax
logits = model(xb)                 # 不接 softmax
loss = nn.CrossEntropyLoss()(logits, yb)

# 推理拿概率（需要时才做）
probs = logits.softmax(dim=-1)
pred  = logits.argmax(dim=-1)      # 取类别可直接对 logits argmax
```

---

## 5. BatchNorm 前面的层带了 bias

**症状**
- 不致命：网络照常训练。但参数有冗余，且属于"对 BN 理解不到位"的信号。

**为什么会错**
- BatchNorm 会对输入做 `(x - mean) / std`，其中的均值减法**会抵消掉前一层的 bias**——bias 是个常数偏移，被 BN 的去均值直接消掉，永远不起作用。
- 所以 `Conv`/`Linear` 紧接 `BatchNorm` 时，前面那层的 `bias` 是**多余参数**（白占显存、白算梯度）。BN 自身的 `affine` 参数（γ、β）已经提供了可学习的缩放和偏移。

**怎么查**
- 找形如 `Conv2d(...) -> BatchNorm2d(...)` 或 `Linear(...) -> BatchNorm1d(...)` 的结构，看前一层是否设了 `bias=False`。

**怎么改**
```python
# 推荐：BN 前的层关掉 bias
nn.Sequential(
    nn.Conv2d(3, 64, 3, padding=1, bias=False),   # ← bias=False
    nn.BatchNorm2d(64),                            # β 充当偏移
    nn.ReLU(inplace=True),
)
```
- 反过来：如果某层后面**没有** BN，则正常保留 bias。

---

## 6. 用 `view` 当 `permute`（或反之）

**症状**
- 张量"shape 看着对，但内容是乱的"，模型精度莫名其妙崩掉或远低于预期。
- 报错 `view size is not compatible with input tensor's size and stride` / 提示需要 `.contiguous()`。

**为什么会错**
- 两类操作语义完全不同：
  - `permute` / `transpose`：**交换维度顺序**（换轴），数据在内存里**不搬动**，只改变 stride/视图。`(N, C, H, W) -> (N, H, W, C)` 用 `permute`。
  - `view` / `reshape`：**重新解释内存布局**，按行优先（C-order）重新分块。它**不交换语义轴**，只是把同一段连续内存切成新形状。
- 把"想换轴"的需求用 `view` 写 → 元素被按内存顺序硬塞进新形状，语义全乱（比如想把 `(N,C,H,W)` 变 `(N,H,W,C)` 却用 view，得到的根本不是转置）。
- 把"想合并/拆分维度"的需求用 `permute` 写 → 维度数对不上或报错。
- 额外坑：`permute`/`transpose` 后张量**非 contiguous**，直接 `view` 会报错，需先 `.contiguous()`（或改用 `reshape`，它会在必要时自动拷贝）。

**怎么查**
- 问自己一句话：**我是要"换轴顺序"还是"重排内存形状"？**
  - 换轴顺序（转置类）→ `permute` / `transpose`。
  - 合并/拆分维度、展平（如 `(N, C, H, W) -> (N, C*H*W)`）→ `view` / `reshape`。
- 变换后抽样打印几个元素，确认内容符合预期，别只看 shape。

**怎么改**
```python
x = torch.randn(2, 3, 4, 5)        # (N, C, H, W)

# 换轴：NCHW -> NHWC，用 permute（内容语义正确）
x_nhwc = x.permute(0, 2, 3, 1)     # shape (2, 4, 5, 3)

# permute 后非 contiguous，要 view 须先 contiguous，或直接用 reshape
flat = x_nhwc.contiguous().view(2, -1)   # 或 x_nhwc.reshape(2, -1)

# 展平特征图：合并 C,H,W，用 view/reshape（不是 permute）
feat = x.reshape(2, -1)            # (2, 60)，行优先展平
```

经验法则：
- **要"转置/换轴" → `permute`/`transpose`**
- **要"改形状/合并拆分/展平" → `reshape`（最省心）或 `view`（需保证 contiguous）**

---

## 排查流程图（口诀）

```
不收敛？
 └─ 先 overfit 一个 batch（第1条）
     ├─ 能 overfit → 链路OK，查数据/正则/学习率/调度
     └─ 不能 overfit → 查链路：
         ├─ train()/eval() 切了吗？        (第2条)
         ├─ 每步 zero_grad() 了吗？         (第3条)
         └─ loss 吃 logits 还是概率？对上没？(第4条)

结果错乱/精度怪、维度操作后变乱？
 └─ view vs permute 用对了吗？contiguous？ (第6条)

整洁性收尾：BN 前的层 bias=False 了吗？   (第5条)
```

---

# 扩展：Karpathy 推文未列但同样高频的坑（第 7~14 条）

> 以下 8 条**不在原推文**中，但实战同样高频、且多数同样"静默"。它们多属"训练策略层"——不决定"链路对不对"，而决定"训得好不好、能不能复现"。建议在跑通前 6 条后照此复查。

---

## 7. 训练 DataLoader 没 `shuffle=True`

**症状**
- 每个 epoch 内 loss 呈现固定的周期性抖动；收敛慢或卡住。
- 数据若按类别/时间排序，训练直接崩坏（一个 batch 全是同一类）。

**为什么会错**
- SGD 假定每个 batch 是从分布里近似 i.i.d. 采样的。不 shuffle → batch 间高度相关、梯度有偏，且每个 epoch 看到的 batch 序列完全相同，引入伪周期。
- 按 label 排序的数据不 shuffle 时，单个 batch 类别极不均衡，BN 统计与梯度方向都被带偏。

**怎么查**
- 训练 `DataLoader(..., shuffle=True)`（或用随机 `Sampler`）；验证/测试集 `shuffle=False`（评估不需要、且要可复现）。
- 检查数据是否在落盘时就按 label/时间排好序了。

**怎么改**
```python
train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)
val_loader   = DataLoader(val_ds,   batch_size=64, shuffle=False)
```
- 时序/分组数据要小心：不能跨时间泄漏，应在合法分组内 shuffle，而不是全局打乱。

---

## 8. loss 没对 batch 取平均 / reduction 不一致

**症状**
- 换了 batch_size 后必须重调学习率；梯度量级随 batch 变化。
- 多任务把几个 loss 相加时尺度失衡；手动累加 loss 忘了除以样本数。

**为什么会错**
- `reduction='sum'` 与 `'mean'` 差一个 batch_size 因子：**sum 的梯度量级恰好是 mean 的 batch_size 倍**（可手算验证：`L_sum = Σ Lᵢ`，`L_mean = L_sum / N`，故 `grad(sum) = N · grad(mean)`）。
- 用 sum，等效学习率被 batch_size 放大，换 batch 就发散或学不动。多个 loss 相加时若各自 reduction 不一致，权重被隐式扭曲。

**怎么查**
- 确认 loss 的 `reduction`（默认 `'mean'`，一般保持默认）。
- 手写 loss 时确认除以了 batch 大小。
- 变长序列（NLP）：明确是按 token 数还是样本数平均，padding 的位置用 mask 排除、别算进分母。

**怎么改**
```python
criterion = nn.CrossEntropyLoss()          # 默认 reduction='mean'

# 变长序列：按有效 token 数平均（mask 掉 padding）
loss = (per_token_loss * mask).sum() / mask.sum()

# 梯度累积：每个 micro-batch 的 loss 先除以累积步数，再 backward
loss = criterion(out, yb) / accum_steps
```

---

## 9. 学习率没 warmup / 没 scheduler / 量级离谱

**症状**
- 训练前几百步就发散或 loss 爆成 NaN（尤其 Adam + 大 batch + Transformer）。
- 或 loss 降一点就进平台、后期榨不出精度。

**为什么会错**
- 训练初期 Adam 的二阶矩估计还不稳，步长方差大；大 batch/大模型初期梯度噪声大，直接用目标 LR 容易冲飞。warmup 让 LR 从 0 线性升到目标值，稳住初期；后期 cosine/step decay 收尾才能逼近最优。
- LR 是最重要的超参，量级错一个数量级基本等于白训。

**怎么查**
- Transformer/大 batch 训练是否有 warmup（几百~几千 step）。
- 是否挂了 LR scheduler；有没有用 LR range test 粗扫过合理量级。

**怎么改**
```python
from torch.optim.lr_scheduler import LambdaLR

def warmup_cosine(step, warmup, total):
    """线性 warmup + 余弦衰减的 LR 系数。step<warmup 时线性升，之后余弦降。"""
    import math
    if step < warmup:
        return step / max(1, warmup)
    progress = (step - warmup) / max(1, total - warmup)
    return 0.5 * (1.0 + math.cos(math.pi * progress))

scheduler = LambdaLR(optimizer, lr_lambda=lambda s: warmup_cosine(s, 500, 10000))
# 每个 optimizer.step() 后调用 scheduler.step()
```
- HuggingFace 可直接用 `get_linear_schedule_with_warmup` / `get_cosine_schedule_with_warmup`。

---

## 10. 归一化统计量泄漏 / 推理忘了同样的归一化

**症状**
- 验证/测试指标虚高（泄漏），或线上推理比线下评估差很多（推理没归一化或用错 stats）。

**为什么会错**
- ① 用**整个数据集**（含 val/test）算 mean/std → 信息从测试集泄漏进训练，指标虚高。
- ② 训练做了 normalize，推理却忘了用**同一套** train 统计量 → 输入分布错位。
- ③ 对 val/test 各自重新算 stats 归一化，也是泄漏/不一致。

**怎么查**
- 归一化的 mean/std **只用训练集**拟合；val/test/线上推理一律复用这同一组。
- `transforms.Normalize`（图像）或标准化器（表格）的参数，训练与推理必须一致。

**怎么改**
```python
mu = train_x.mean(0, keepdim=True)      # 只在训练集上拟合
sd = train_x.std(0, keepdim=True) + 1e-8
# 保存 mu, sd；train/val/test/线上推理全部复用：
norm = lambda x: (x - mu) / sd
```

---

## 11. 没固定随机种子 → 不可复现

**症状**
- 同样代码每次结果不同，无法判断"指标变化是改动有效还是随机波动"，实验无法对比。

**为什么会错**
- torch、numpy、python `random`、CUDA 各有独立 RNG；DataLoader worker、cudnn 的非确定算法都引入随机。

**怎么改**
```python
def seed_everything(seed=42):
    """统一固定 torch/numpy/python/CUDA 的随机种子，保证实验可复现可对比。"""
    import os, random
    import numpy as np
    import torch
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    # 需严格复现再开（会牺牲速度）：
    # torch.backends.cudnn.deterministic = True
    # torch.backends.cudnn.benchmark = False
```
- DataLoader 多 worker 严格复现还需 `worker_init_fn` + 显式 `generator`。
- 注意：固定种子是为了**可控对比**，不是为了挑一个"好看的种子"——那是自欺。

---

## 12. 在 GPU 上累加 loss 不 `.item()` / `.detach()` → 显存泄漏

**症状**
- 显存随 step/epoch 持续上涨直到 OOM；训练越跑越慢。

**为什么会错**
- `total_loss += loss`，其中 `loss` 是带计算图的 tensor。这样会把每个 batch 的计算图都挂住不释放，显存不断累积。

**怎么查/改**
```python
running_loss = 0.0
for xb, yb in train_loader:
    ...
    loss = criterion(out, yb)
    loss.backward(); optimizer.step()
    running_loss += loss.item() * xb.size(0)   # 取标量；并按样本数加权（呼应第 8 条）
epoch_loss = running_loss / len(train_loader.dataset)
```
- 统计任何指标（loss/acc）时都用 `.item()` 或 `.detach()`，别直接累加带图的 tensor。

---

## 13. `CrossEntropyLoss` 的 target 类型/形状不对

**症状**
- 报 dtype/形状错（这条不算 silent）；或更隐蔽——把 one-hot/float 概率当 target、target 多一维，训练能跑但学错。

**为什么会错**
- `nn.CrossEntropyLoss` 的 target 默认期望 **`long` 类型的类别索引**，形状 `(N,)`（图像分割等是 `(N, H, W)`），**不是 one-hot**。
- `nn.BCEWithLogitsLoss` 才吃 `float` 的 `(N, C)`。两者混用会语义错或维度错。

**怎么查/改**
```python
# 多分类：target 是 (N,) 的 long 类别索引
yb = yb.long()                       # 别做 one-hot
loss = nn.CrossEntropyLoss()(logits, yb)     # logits 形状 (N, C)

# 多标签/二分类：target 是 (N, C) 的 float（0/1）
loss = nn.BCEWithLogitsLoss()(logits, yb.float())
```

---

## 14. weight decay 误加到 bias / BatchNorm / LayerNorm 参数上

**症状**
- 不致命，但正则略偏；norm 层的 γ、β 和各层 bias 被错误衰减，轻微伤性能。与第 5 条同属"对组件理解不到位"的信号。

**为什么会错**
- weight decay 的本意是惩罚**权重矩阵**的幅度。对 1-D 的 bias / norm 仿射参数做衰减缺乏理论依据，多数 SOTA 配方都把这些参数单列为 `weight_decay=0`。

**怎么改**
```python
def split_param_groups(model, weight_decay=1e-2):
    """把参数分两组：weight 走 weight_decay，bias/norm 参数 weight_decay=0。"""
    decay, no_decay = [], []
    for name, p in model.named_parameters():
        if not p.requires_grad:
            continue
        # bias 及 1-D 参数（BN/LayerNorm 的 weight 也是 1-D）不做 weight decay
        if p.ndim <= 1 or name.endswith(".bias"):
            no_decay.append(p)
        else:
            decay.append(p)
    return [
        {"params": decay, "weight_decay": weight_decay},
        {"params": no_decay, "weight_decay": 0.0},
    ]

optimizer = torch.optim.AdamW(split_param_groups(model), lr=3e-4)
```

---

## 扩展坑排查口诀

```
能 overfit 单 batch、链路也通，但训得不好 / 不可复现？查训练策略层：
 ├─ 训练数据 shuffle 了吗？            (第7条)
 ├─ loss 按样本数平均了吗？reduction 一致？(第8条)
 ├─ LR 有 warmup + scheduler 吗？量级合理？(第9条)
 ├─ 归一化 stats 只用训练集、各阶段复用？  (第10条)
 ├─ 随机种子固定了吗（能复现/可对比）？     (第11条)
 ├─ 统计 loss 用 .item() 防显存泄漏？      (第12条)
 ├─ CrossEntropy 的 target 是 long 索引？  (第13条)
 └─ weight decay 排除了 bias/norm？        (第14条)
```
