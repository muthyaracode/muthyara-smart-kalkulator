import unittest

from app.core.formatter import format_decimal
from app.core.units import convert_value
from decimal import Decimal


class UnitAndFormatterTests(unittest.TestCase):
    def test_indonesian_number_format(self):
        self.assertEqual(format_decimal(Decimal("1234567.89")), "1.234.567,89")
        self.assertEqual(format_decimal(Decimal("0.3000")), "0,3")

    def test_length_and_temperature_conversion(self):
        self.assertEqual(convert_value(1500, "Panjang", "Meter", "Kilometer"), 1.5)
        self.assertAlmostEqual(convert_value(32, "Suhu", "Fahrenheit", "Celsius"), 0)


if __name__ == "__main__":
    unittest.main()