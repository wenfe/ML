"""Tests for local tools."""

import unittest

from src.tools.calculator import calculate


class CalculatorTests(unittest.TestCase):
    def test_calculates_arithmetic_with_precedence(self) -> None:
        self.assertEqual(calculate("2 + 3 * 4"), 14)

    def test_rejects_non_arithmetic_expressions(self) -> None:
        with self.assertRaises(ValueError):
            calculate("__import__('os').getcwd()")

    def test_rejects_large_exponents(self) -> None:
        with self.assertRaises(ValueError):
            calculate("2 ** 101")


if __name__ == "__main__":
    unittest.main()
