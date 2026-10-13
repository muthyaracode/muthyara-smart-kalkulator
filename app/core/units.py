"""Offline unit conversion data and logic."""

from __future__ import annotations


UNIT_FACTORS = {
    "Panjang": {"Milimeter": 0.001, "Sentimeter": 0.01, "Meter": 1, "Kilometer": 1000, "Inci": 0.0254, "Kaki": 0.3048, "Mil": 1609.344},
    "Berat": {"Miligram": 0.000001, "Gram": 0.001, "Kilogram": 1, "Ton": 1000, "Ons": 0.1, "Pon": 0.45359237},
    "Luas": {"Meter persegi": 1, "Kilometer persegi": 1000000, "Hektare": 10000, "Are": 100, "Kaki persegi": 0.09290304},
    "Volume": {"Mililiter": 0.001, "Liter": 1, "Meter kubik": 1000, "Galon (AS)": 3.785411784, "Cangkir": 0.2365882365},
    "Kecepatan": {"m/s": 1, "km/jam": 1 / 3.6, "Mil/jam": 0.44704, "Knot": 0.514444},
    "Data": {"Bit": 0.125, "Byte": 1, "Kilobyte": 1000, "Megabyte": 1000000, "Gigabyte": 1000000000, "Kibibyte": 1024, "Mebibyte": 1048576},
}
UNIT_FACTORS["Suhu"] = {"Celsius": 1, "Fahrenheit": 1, "Kelvin": 1}
UNIT_CATEGORIES = list(UNIT_FACTORS)


def convert_value(value: float, category: str, from_unit: str, to_unit: str) -> float:
    if category not in UNIT_FACTORS or from_unit not in UNIT_FACTORS[category] or to_unit not in UNIT_FACTORS[category]:
        raise ValueError("Satuan tidak dikenal")
    if category == "Suhu":
        celsius = value if from_unit == "Celsius" else (value - 32) * 5 / 9 if from_unit == "Fahrenheit" else value - 273.15
        return celsius if to_unit == "Celsius" else celsius * 9 / 5 + 32 if to_unit == "Fahrenheit" else celsius + 273.15
    base_value = value * UNIT_FACTORS[category][from_unit]
    return base_value / UNIT_FACTORS[category][to_unit]