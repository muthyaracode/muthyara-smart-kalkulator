import unittest
from decimal import Decimal

from app.core.evaluator import ExpressionError, evaluate


class EvaluatorTests(unittest.TestCase):
    def test_decimal_arithmetic_and_precedence(self):
        self.assertEqual(evaluate("0.1 + 0.2"), Decimal("0.3"))
        self.assertEqual(evaluate("2 + 3 * 4"), Decimal("14"))
        self.assertEqual(evaluate("(2 + 3) * 4"), Decimal("20"))

    def test_smart_percent(self):
        self.assertEqual(evaluate("100 + 10%"), Decimal("110.00"))
        self.assertEqual(evaluate("100 - 10%"), Decimal("90.00"))
        self.assertEqual(evaluate("50 * 10%"), Decimal("5.0"))

    def test_scientific_functions(self):
        self.assertEqual(evaluate("sin(30)"), Decimal("0.5"))
        self.assertEqual(evaluate("sqrt(144)"), Decimal("12"))
        self.assertEqual(evaluate("5!"), Decimal("120"))

    def test_friendly_errors_and_rejects_code(self):
        with self.assertRaisesRegex(ExpressionError, "Tidak bisa dibagi nol"):
            evaluate("5 / 0")
        with self.assertRaises(ExpressionError):
            evaluate("__import__('os')")


if __name__ == "__main__":
    unittest.main()