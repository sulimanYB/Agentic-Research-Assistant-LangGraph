# Unit tests for the calculator tool

import pytest
from src.tools.math_tools import calculator


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("2 + 3", 5),
        ("10 - 4", 6),
        ("3 * 7", 21),
        ("12 / 4", 3),
        ("2 ** 3", 8),
        ("(10 + 12) / 2", 11),
    ],
)
def test_basic_calculations(expression, expected):
    result = calculator.invoke({"expression": expression})
    assert float(result) == pytest.approx(expected)


def test_division_by_zero():
    result = calculator.invoke({"expression": "10 / 0"})
    assert "Calculation error" in result


def test_unsafe_expression():
    result = calculator.invoke({
        "expression": "__import__('os').system('echo unsafe')"
    })
    assert "Calculation error" in result