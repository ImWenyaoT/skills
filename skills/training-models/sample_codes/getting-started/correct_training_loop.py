"""A correct PyTorch train loop and validation loop. Copy it into your own project.

This file backs the Stage 2 loop review. One template avoids four checklist entries:
- entry 2: train_one_epoch() calls model.train(), and evaluate() calls model.eval().
- entry 3: every step follows the order zero_grad, forward, backward, step.
- entry 4: the model gives logits, and CrossEntropyLoss applies the softmax.
- entry 5: a Linear layer in front of a BatchNorm layer sets bias=False.

The demo data holds four separable Gaussian blobs, so a correct loop shows a train loss
that falls, a validation loss that falls, and an accuracy near 1.0. Any other output on
this data reports a defect in your edit.

Requirement: torch. Run: python correct_training_loop.py
"""

from __future__ import annotations

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

# The default device. The template never selects a GPU on its own, because a shared
# machine can hold a GPU that belongs to a different user. Pass device="cuda:1" to main()
# when you own that GPU.
DEFAULT_DEVICE = "cpu"


def make_blobs(n_per_class=128, in_features=20, num_classes=4, seed=0):
    """Build a separable demo dataset from one Gaussian blob for each class.

    Args:
        n_per_class: The number of samples for each class.
        in_features: The number of input features.
        num_classes: The number of classes.
        seed: The seed of the generator. It makes the reproduction exact.
    Returns:
        A tuple (x, y). The tensor x has the shape (n_per_class * num_classes,
        in_features). The tensor y holds long class indices.
    Note:
        Replace this function with your own Dataset. The blobs exist so that a correct
        loop shows a clear success. Random labels would hide a defect behind noise.
    """
    generator = torch.Generator().manual_seed(seed)
    centers = torch.randn(num_classes, in_features, generator=generator) * 2.5
    y = torch.arange(num_classes).repeat_interleave(n_per_class)
    x = centers[y] + torch.randn(y.numel(), in_features, generator=generator)
    order = torch.randperm(y.numel(), generator=generator)
    return x[order], y[order]


def build_model(in_features: int = 20, num_classes: int = 4) -> nn.Module:
    """Build a small classifier.

    Args:
        in_features: The number of input features.
        num_classes: The number of output classes.
    Returns:
        An nn.Module that gives logits.
    Note:
        The Linear layer in front of the BatchNorm layer sets bias=False, because the beta
        parameter of the BatchNorm layer already holds the offset. The output layer gives
        logits, because CrossEntropyLoss applies the softmax itself.
    """
    return nn.Sequential(
        nn.Linear(in_features, 64, bias=False),  # entry 5: a BatchNorm layer follows.
        nn.BatchNorm1d(64),
        nn.ReLU(inplace=True),
        nn.Dropout(0.2),  # entry 2: this layer makes the two modes differ.
        nn.Linear(64, num_classes),  # entry 4: the model gives logits.
    )


def train_one_epoch(model, loader, criterion, optimizer, device):
    """Train the model for one epoch.

    Args:
        model: The nn.Module to train.
        loader: The DataLoader of the train split. Set shuffle=True on it.
        criterion: The loss function.
        optimizer: The optimizer.
        device: The device string, for example "cpu" or "cuda:1".
    Returns:
        The mean train loss of this epoch as a float.
    Note:
        The mode switch sits on the first line, so an outer caller cannot forget it.
    """
    model.train()  # entry 2: train mode.
    total_loss = 0.0
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        optimizer.zero_grad()  # entry 3: clear the gradient first.
        logits = model(xb)  # The forward pass gives logits.
        loss = criterion(logits, yb)  # CrossEntropyLoss applies the softmax.
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * xb.size(0)  # entry 12: add a float, not a tensor.
    return total_loss / len(loader.dataset)


@torch.no_grad()
def evaluate(model, loader, criterion, device):
    """Measure the loss and the accuracy on a validation split or a test split.

    Args:
        model: The nn.Module to evaluate.
        loader: The DataLoader of the split. Set shuffle=False on it.
        criterion: The loss function.
        device: The device string, for example "cpu" or "cuda:1".
    Returns:
        A tuple (mean_loss, accuracy) of two floats.
    Note:
        model.eval() turns the dropout off and switches the BatchNorm layer to its running
        statistics. The no_grad decorator drops the graph and saves memory.
    """
    model.eval()  # entry 2: eval mode.
    total_loss, correct, n = 0.0, 0, 0
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        logits = model(xb)
        total_loss += criterion(logits, yb).item() * xb.size(0)
        correct += (logits.argmax(dim=-1) == yb).sum().item()  # argmax reads the logits.
        n += xb.size(0)
    return total_loss / n, correct / n


def main(device: str = DEFAULT_DEVICE, epochs: int = 5, seed: int = 0):
    """Run the whole template once: build the data, the model, the train loop, the metrics.

    Args:
        device: The device string. The default is "cpu". Name a GPU explicitly, for
            example "cuda:1", and only when you own that GPU.
        epochs: The number of epochs.
        seed: The seed of the run. It makes the reproduction exact.
    Returns:
        None. The function prints one line for each epoch.
    """
    torch.manual_seed(seed)

    x, y = make_blobs()  # Replace this call with your own Dataset.
    train_ds = TensorDataset(x[:400], y[:400])
    val_ds = TensorDataset(x[400:], y[400:])
    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)  # entry 7: shuffle.
    val_loader = DataLoader(val_ds, batch_size=64)

    model = build_model().to(device)
    criterion = nn.CrossEntropyLoss()  # entry 4: it wants logits.
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    print(f"device={device}")
    for epoch in range(epochs):
        tr_loss = train_one_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        print(
            f"epoch {epoch}: train_loss={tr_loss:.4f} "
            f"val_loss={val_loss:.4f} val_acc={val_acc:.3f}"
        )


if __name__ == "__main__":
    # Change the device here, and name the GPU that you own. Example: main("cuda:1").
    main()
