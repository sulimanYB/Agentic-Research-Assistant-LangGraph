# Mathematical calculation tool for the research assistant

import ast
import math
import operator

from langchain_core.tools import tool

# Supported mathematical operations
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# Resource limits for mathematical expressions
MAX_EXPRESSION_LENGTH = 200
MAX_ABS_VALUE = 1e12
MAX_EXPONENT = 100

def evaluate_expression(node):
    """Safely evaluate a restricted mathematical expression."""

    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        left = evaluate_expression(node.left)
        right = evaluate_expression(node.right)

        # Restrict exponentiation to prevent expensive calculations
        if isinstance(node.op, ast.Pow):
            if abs(right) > MAX_EXPONENT:
                raise ValueError("Exponent exceeds the allowed limit")

        # Restrict excessively large intermediate results
        if abs(left) > MAX_ABS_VALUE or abs(right) > MAX_ABS_VALUE:
            raise ValueError("Numerical value exceeds the allowed limit")

        result = OPERATORS[type(node.op)](left, right)

        # Reject complex-number results
        if not isinstance(result, (int, float)):
            raise ValueError("Only real-number results are supported")
        

        if not math.isfinite(result) or abs(result) > MAX_ABS_VALUE:
            raise ValueError("Result exceeds the allowed limit")

        return result

    if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](
            evaluate_expression(node.operand)
        )

    raise ValueError("Unsupported mathematical expression")


@tool
def calculator(expression: str) -> str:
    """
    Evaluate a basic mathematical expression.

    Supports addition, subtraction, multiplication,
    division, powers and parentheses.

    Example: "(0.89 - 0.84) * 100"
    """
    try:
        # Reject excessively long expressions
        if len(expression) > MAX_EXPRESSION_LENGTH:
            return "Calculation error: Expression too long."
        
        tree = ast.parse(expression, mode="eval")
        result = evaluate_expression(tree.body)

        if not math.isfinite(result):
            return "Error: Non-finite result."

        return str(result)

    except (ValueError, SyntaxError, ZeroDivisionError, OverflowError) as e:
        return f"Calculation error: {e}"