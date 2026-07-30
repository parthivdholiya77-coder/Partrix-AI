import ast
import operator as op
from langchain_core.tools import tool

# Supported operators
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.FloorDiv: op.floordiv,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}


def evaluate(node):
    if isinstance(node, ast.Constant):  # Numbers
        return node.value

    elif isinstance(node, ast.BinOp):  # Binary operations
        operator = OPERATORS.get(type(node.op))
        if operator is None:
            raise ValueError("Unsupported operator")
        return operator(evaluate(node.left), evaluate(node.right))

    elif isinstance(node, ast.UnaryOp):  # Unary operations
        operator = OPERATORS.get(type(node.op))
        if operator is None:
            raise ValueError("Unsupported operator")
        return operator(evaluate(node.operand))

    raise ValueError("Invalid mathematical expression")


@tool
def calculator(expression: str) -> str:
    """
    Evaluate mathematical expressions accurately.

    Use this tool whenever:
    - The calculation is complex.
    - High numerical accuracy is important.
    - The expression contains multiple operations, parentheses, exponents, percentages, or decimals.

    Do NOT use this tool for very simple arithmetic (e.g. 2+2, 5*3) that can be answered reliably without external computation.
    """

    try:
        tree = ast.parse(expression, mode="eval")
        result = evaluate(tree.body)

        # Return integer if possible
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return str(result)

    except ZeroDivisionError:
        return "Error: Division by zero."

    except Exception:
        return "Error: Invalid mathematical expression."