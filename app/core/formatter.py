"""Indonesian number formatting helpers."""

from decimal import Decimal


def format_decimal(value: Decimal, decimal_separator: str = ",") -> str:
    text = format(value, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    integer, separator, fraction = text.partition(".")
    sign = ""
    if integer.startswith("-"):
        sign, integer = "-", integer[1:]
    grouped = "_".join(integer[index:index + 3] for index in range(len(integer) % 3, len(integer), 3))
    if len(integer) <= 3:
        grouped = integer
    else:
        first = len(integer) % 3 or 3
        grouped = ".".join([integer[:first]] + [integer[index:index + 3] for index in range(first, len(integer), 3)])
    return sign + grouped + (decimal_separator + fraction if separator and fraction else "")