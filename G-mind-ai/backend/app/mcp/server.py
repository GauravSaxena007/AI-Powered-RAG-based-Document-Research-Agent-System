import ast
import operator
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocMind Tools")

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate(expression: str) -> str:
    """Evaluate a basic arithmetic expression without executing Python."""
    if not expression.strip() or len(expression) > 100:
        raise ValueError("Enter an arithmetic expression of at most 100 characters.")

    def evaluate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
            if isinstance(node.op, ast.Pow) and abs(evaluate(node.right)) > 100:
                raise ValueError("Exponent is too large.")
            return _OPERATORS[type(node.op)](evaluate(node.left), evaluate(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
            return _OPERATORS[type(node.op)](evaluate(node.operand))
        raise ValueError("Only basic arithmetic is allowed.")

    try:
        result = evaluate(ast.parse(expression, mode="eval").body)
    except (SyntaxError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError("Invalid arithmetic expression.") from exc
    if isinstance(result, (int, float)) and abs(result) > 1e100:
        raise ValueError("Result is too large.")
    return str(result)


def get_current_datetime() -> str:
    """Return the current UTC date and time."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@mcp.tool()
def calculator(expression: str) -> str:
    """Calculate a basic arithmetic expression, for example '125 * 48'."""
    return calculate(expression)


@mcp.tool()
def current_datetime() -> str:
    """Get the current date and time in UTC."""
    return get_current_datetime()


if __name__ == "__main__":
    mcp.run(transport="stdio")
