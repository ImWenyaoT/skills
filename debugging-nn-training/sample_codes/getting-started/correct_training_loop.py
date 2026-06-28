"""一份"正确"的 PyTorch 训练循环模板。

它一次性规避了 6 条坑里的训练循环类问题：
- 第 2 条：train_one_epoch 开头 model.train()，evaluate 开头 model.eval()
- 第 3 条：每个 step 都 optimizer.zero_grad()，顺序为 zero_grad→forward→backward→step
- 第 4 条：模型输出 logits，loss 用 CrossEntropyLoss（内部含 softmax），不在模型里加 softmax
- 第 5 条：Conv/Linear 接 BatchNorm 时 bias=False
把它当作新项目的训练骨架抄写参考。

依赖：torch。运行：python correct_training_loop.py
"""

from __future__ import annotations

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset


def build_model(in_features: int = 20, num_classes: int = 4) -> nn.Module:
    """构建一个小型分类网络。

    要点：
    - BatchNorm 前的 Linear 设 bias=False（第 5 条），偏移交给 BN 的 β。
    - 输出层直接给 logits，不接 Softmax（第 4 条），softmax 留给 CrossEntropyLoss。
    """
    return nn.Sequential(
        nn.Linear(in_features, 64, bias=False),  # 第 5 条：后接 BN，去 bias
        nn.BatchNorm1d(64),
        nn.ReLU(inplace=True),
        nn.Dropout(0.2),                         # 含 Dropout → 训练/评估行为不同（第 2 条）
        nn.Linear(64, num_classes),              # 输出 logits（第 4 条）
    )


def train_one_epoch(model, loader, criterion, optimizer, device):
    """训练一个 epoch。

    模式切换写进函数开头，避免在外层漏切（第 2 条）。
    每步严格遵循 zero_grad → forward → backward → step（第 3 条）。
    """
    model.train()                                # 第 2 条：训练模式
    total_loss = 0.0
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()                    # 第 3 条：先清梯度
        logits = model(xb)                       # 前向，输出 logits（第 4 条）
        loss = criterion(logits, yb)             # CrossEntropyLoss 内部做 softmax
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * xb.size(0)
    return total_loss / len(loader.dataset)


@torch.no_grad()
def evaluate(model, loader, criterion, device):
    """在验证/测试集上评估。

    eval() + no_grad()：关闭 Dropout、BN 用 running stats，结果确定且省显存（第 2 条）。
    """
    model.eval()                                 # 第 2 条：评估模式
    total_loss, correct, n = 0.0, 0, 0
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        logits = model(xb)
        total_loss += criterion(logits, yb).item() * xb.size(0)
        correct += (logits.argmax(dim=-1) == yb).sum().item()  # 对 logits 直接 argmax
        n += xb.size(0)
    return total_loss / n, correct / n


def main():
    """端到端跑通：造数据 → 建模 → 训练 → 评估。"""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(0)

    # 合成数据集（真实项目替换为你的 Dataset）
    X = torch.randn(512, 20)
    y = torch.randint(0, 4, (512,))
    train_ds = TensorDataset(X[:400], y[:400])
    val_ds = TensorDataset(X[400:], y[400:])
    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=64)

    model = build_model().to(device)
    criterion = nn.CrossEntropyLoss()            # 吃 logits（第 4 条）
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    for epoch in range(5):
        tr_loss = train_one_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        print(f"epoch {epoch}: train_loss={tr_loss:.4f} "
              f"val_loss={val_loss:.4f} val_acc={val_acc:.3f}")


if __name__ == "__main__":
    main()
