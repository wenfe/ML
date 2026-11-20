"""Tests for the MNIST plotting helpers."""

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

_path = Path(__file__).resolve().parents[1] / "src" / "agent" / "helper_utils.py"
_spec = importlib.util.spec_from_file_location("helper_utils", _path)
helper_utils = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(helper_utils)


class PlottingTests(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_metrics_use_epoch_numbers_and_percentages(self):
        with patch.object(plt, "show"):
            helper_utils.plot_metrics([1.0, 0.5], [75.0, 90.0])

        loss_ax, accuracy_ax = plt.gcf().axes
        self.assertEqual(list(loss_ax.lines[0].get_xdata()), [1, 2])
        self.assertEqual(list(loss_ax.lines[0].get_ydata()), [1.0, 0.5])
        self.assertEqual(list(accuracy_ax.lines[0].get_ydata()), [75.0, 90.0])
        self.assertEqual(accuracy_ax.get_ylabel(), "Accuracy (%)")

    def test_metrics_reject_missing_or_mismatched_data(self):
        for loss, accuracy in [([], []), ([1.0], [])]:
            with self.subTest(loss=loss, accuracy=accuracy):
                with self.assertRaises(ValueError):
                    helper_utils.plot_metrics(loss, accuracy)

    def test_display_image_shows_values_and_label(self):
        image = Image.fromarray(np.array([[0, 255], [128, 64]], dtype=np.uint8))
        with patch.object(plt, "show"):
            helper_utils.display_image(image, 5, "Digit", show_values=True)

        ax = plt.gcf().axes[0]
        self.assertEqual(ax.get_title(), "Digit - Label: 5")
        self.assertEqual([text.get_text() for text in ax.texts], ["0", "255", "128", "64"])

    def test_notebook_can_import_helper_from_its_directory(self):
        subprocess.run(
            [sys.executable, "-c", "import helper_utils"],
            cwd=_path.parent,
            check=True,
        )

    @unittest.skipUnless(importlib.util.find_spec("torch"), "PyTorch is not installed")
    def test_display_tensor_and_predictions_restore_model_mode(self):
        import torch
        from torch.utils.data import DataLoader, TensorDataset

        class Model(torch.nn.Module):
            def forward(self, images):
                self.assert_eval_without_grad()
                return torch.tensor([[0.0, 1.0]] * len(images))

            def assert_eval_without_grad(self):
                if self.training or torch.is_grad_enabled():
                    raise AssertionError("Predictions must use evaluation without gradients.")

        model = Model()
        images = torch.zeros(3, 1, 2, 2)
        labels = torch.tensor([1, 1, 1])
        loader = DataLoader(TensorDataset(images, labels), batch_size=3)

        with patch.object(plt, "show"):
            helper_utils.display_image(images[0], labels[0], "Tensor")
            helper_utils.display_predictions(model, loader, torch.device("cpu"), num_images=2)

        self.assertTrue(model.training)
        self.assertEqual(len(plt.gcf().axes), 2)
        self.assertTrue(all(ax.get_title() == "Pred: 1\nTrue: 1" for ax in plt.gcf().axes))

    @unittest.skipUnless(importlib.util.find_spec("torch"), "PyTorch is not installed")
    def test_display_predictions_rejects_empty_loader(self):
        import torch

        with self.assertRaisesRegex(ValueError, "empty"):
            helper_utils.display_predictions(torch.nn.Linear(1, 1), [], torch.device("cpu"))


if __name__ == "__main__":
    unittest.main()
