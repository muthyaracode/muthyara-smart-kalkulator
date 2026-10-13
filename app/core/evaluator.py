"""Safe expression evaluation without eval()."""

from __future__ import annotations

import ast
import math
import operator
import re
from decimal import Decimal, DivisionByZero, InvalidOperation, localcontext


class ExpressionError(ValueError):
    """Raised when an expression is invalid or cannot be evaluated."""


_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}
_UNARY_OPERATORS = {ast.UAdd: operator.pos, ast.USub: operator.neg}
_FUNCTIONS = {"sin", "cos", "tan", "asin", "acos", "atan", "log", "ln", "sqrt", "abs", "factorial"}


def _decimal(value: Decimal) -> Decimal:
    if not value.is_finite():
        raise ExpressionError("Hasil tidak terdefinisi")
    return value


def _function(name: str, value: Decimal, angle_unit: str) -> Decimal:
    number = float(value)
    if name in {"sin", "cos", "tan"}:
        radians = math.radians(number) if angle_unit == "deg" else number
        result = getattr(math, name)(radians)
    elif name in {"asin", "acos", "atan"}:
        result = getattr(math, name)(number)
        if angle_unit == "deg":
            result = math.degrees(result)
    elif name == "log":
        result = math.log10(number)
    elif name == "ln":
        result = math.log(number)
    elif name == "sqrt":
        result = math.sqrt(number)
    elif name == "abs":
        return abs(value)
    elif name == "factorial":
        if value != value.to_integral_value() or value < 0 or value > 1000:
            raise ExpressionError("Faktorial hanya menerima bilangan bulat 0-1000")
        return Decimal(math.factorial(int(value)))
    else:
        raise ExpressionError("Fungsi tidak dikenal")
    return _decimal(Decimal(format(result, ".15g")))


def evaluate(expression: str, angle_unit: str = "deg") -> Decimal:
    """Evaluate a calculator expression using Decimal for basic arithmetic."""
    if not expression.strip():
        raise ExpressionError("Masukkan ekspresi")
    if len(expression) > 512:
        raise ExpressionError("Ekspresi terlalu panjang")
    if angle_unit not in {"deg", "rad"}:
        angle_unit = "deg"

    normalized = expression.replace("×", "*").replace("÷", "/").replace("−", "-").replace(",", ".").replace("^", "**")
    normalized = re.sub(r"(?<![\w.])π", "pi", normalized)
    normalized = re.sub(r"(?<![\w.])√\s*(?=[\d.(])", "sqrt", normalized)
    normalized = re.sub(r"(?P<value>(?:\d+(?:\.\d*)?|\.\d+)|(?:\([^()]*\)))!", r"factorial(\g<value>)", normalized)
    normalized = re.sub(r"(?<![\w.])(?P<value>(?:\d+(?:\.\d*)?|\.\d+)|(?:\([^()]*\))|(?:[A-Za-z_]\w*\([^()]*\)))%", r"percent(\g<value>)", normalized)
    normalized = re.sub(r"(?<=[0-9.)])\s*([+*/])\s*\1+", r"\1", normalized)

    try:
        tree = ast.parse(normalized, mode="eval")
        with localcontext() as context:
            context.prec = 28
            return _decimal(_visit(tree.body, angle_unit))
    except ZeroDivisionError as error:
        raise ExpressionError("Tidak bisa dibagi nol") from error
    except (DivisionByZero, InvalidOperation, OverflowError, ValueError, SyntaxError) as error:
        if isinstance(error, ExpressionError):
            raise
        raise ExpressionError("Ekspresi tidak valid") from error


def _visit(node: ast.AST, angle_unit: str) -> Decimal:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        return Decimal(str(node.value))
    if isinstance(node, ast.Name):
        if node.id == "pi":
            return Decimal(str(math.pi))
        if node.id == "e":
            return Decimal(str(math.e))
        raise ExpressionError("Nama konstanta tidak dikenal")
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
        return _UNARY_OPERATORS[type(node.op)](_visit(node.operand, angle_unit))
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
        left = _visit(node.left, angle_unit)
        right = _visit(node.right, angle_unit)
        if isinstance(node.right, ast.Call) and isinstance(node.right.func, ast.Name) and node.right.func.id == "percent":
            if isinstance(node.op, (ast.Add, ast.Sub)):
                right = left * right
        if isinstance(node.op, ast.Pow) and abs(right) > 10000:
            raise ExpressionError("Pangkat maksimum adalah 10.000")
        return _decimal(_BINARY_OPERATORS[type(node.op)](left, right))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and len(node.args) == 1 and not node.keywords:
        name = node.func.id
        argument = _visit(node.args[0], angle_unit)
        if name == "percent":
            return argument / Decimal(100)
        if name not in _FUNCTIONS:
            raise ExpressionError("Fungsi tidak dikenal")
        return _function(name, argument, angle_unit)
    raise ExpressionError("Ekspresi tidak valid")