"""Plotting helpers for the MNIST notebook."""

from collections.abc import Sequence

import matplotlib.pyplot as plt
import numpy as np


def _image_array(image):
    """Convert a PIL image, NumPy array, or PyTorch tensor to a 2D array."""
    if hasattr(image, "detach"):
        image = image.detach().cpu().numpy()
    array = np.asarray(image)
    if array.ndim == 3 and array.shape[0] == 1:
        array = array[0]
    elif array.ndim == 3 and array.shape[-1] == 1:
        array = array[..., 0]
    if array.ndim != 2:
        raise ValueError("Expected a grayscale image with two spatial dimensions.")
    return array


def display_image(image, label, title, show_values=False):
    """Display an MNIST image and, optionally, its actual pixel values."""
    pixels = _image_array(image)
    fig, ax = plt.subplots(figsize=(10, 10) if show_values else (5, 5))
    ax.imshow(pixels, cmap="gray")
    ax.set_title(f"{title} - Label: {label}")
    ax.axis("off")

    if show_values:
        threshold = (pixels.min() + pixels.max()) / 2
        for row in range(pixels.shape[0]):
            for col in range(pixels.shape[1]):
                value = pixels[row, col]
                text = (
                    f"{value:.2f}"
                    if np.issubdtype(pixels.dtype, np.floating)
                    else str(value)
                )
                ax.text(
                    col, row, text, ha="center", va="center", fontsize=5,
                    color="black" if value > threshold else "white",
                )
    fig.tight_layout()
    plt.show()


def display_predictions(model, test_loader, device, num_images=8):
    """Display randomly selected predictions from the first test batch."""
    import torch

    if num_images < 1:
        raise ValueError("num_images must be at least 1.")
    try:
        images, labels = next(iter(test_loader))
    except StopIteration as exc:
        raise ValueError("The test loader is empty.") from exc
    if len(images) == 0:
        raise ValueError("The test batch is empty.")

    indices = torch.randperm(len(images))[:num_images]
    images, labels = images[indices], labels[indices]
    was_training = model.training
    try:
        model.eval()
        with torch.no_grad():
            predictions = model(images.to(device)).argmax(dim=1).cpu()
    finally:
        model.train(was_training)

    fig, axes = plt.subplots(1, len(images), figsize=(2 * len(images), 3), squeeze=False)
    for ax, image, label, prediction in zip(axes[0], images, labels, predictions):
        ax.imshow(_image_array(image), cmap="gray")
        ax.set_title(
            f"Pred: {prediction.item()}\nTrue: {label.item()}",
            color="green" if prediction.item() == label.item() else "red",
        )
        ax.axis("off")
    fig.tight_layout()
    plt.show()


def plot_metrics(train_loss: Sequence[float], test_acc: Sequence[float]):
    """Plot per-epoch training loss and test accuracy (as percentages)."""
    if len(train_loss) != len(test_acc):
        raise ValueError("Training loss and test accuracy must have the same length.")
    if len(train_loss) == 0:
        raise ValueError("At least one epoch of metrics is required.")

    epochs = range(1, len(train_loss) + 1)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(epochs, train_loss, marker="o")
    axes[0].set(title="Training Loss", xlabel="Epoch", ylabel="Loss")
    axes[1].plot(epochs, test_acc, marker="o")
    axes[1].set(title="Test Accuracy", xlabel="Epoch", ylabel="Accuracy (%)")
    for ax in axes:
        ax.set_xticks(list(epochs))
        ax.grid(True, alpha=0.3)
    fig.tight_layout()
    plt.show()
