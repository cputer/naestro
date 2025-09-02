import re
from typing import Any, Dict

import sympy as sp
from langgraph.graph import StateGraph


# Allowed symbols and functions for safe evaluation
x = sp.symbols("x")
ALLOWED_NAMES = {
    "x": x,
    "pi": sp.pi,
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "log": sp.log,
    "exp": sp.exp,
    "sqrt": sp.sqrt,
}

# Regular expressions for validating user supplied expressions
_ALLOWED_CHAR_RE = re.compile(r"^[0-9a-zA-Z+\-*/^().,\s]*$")
_TOKEN_RE = re.compile(r"[A-Za-z]+")


def _validate_expr(expr: str) -> None:
    """Validate that an expression contains only whitelisted tokens.

    Parameters
    ----------
    expr: str
        The expression string to validate.

    Raises
    ------
    ValueError
        If the expression contains invalid characters or tokens.
    """

    if not _ALLOWED_CHAR_RE.fullmatch(expr):
        raise ValueError("Invalid characters in expression")

    for token in _TOKEN_RE.findall(expr):
        if token not in ALLOWED_NAMES:
            raise ValueError(f"Invalid token: {token}")


def _safe_sympify(expr: str) -> sp.Expr:
    """Safely convert a string expression to a SymPy expression."""

    _validate_expr(expr)
    return sp.sympify(expr, locals=ALLOWED_NAMES, evaluate=False)

def parse_math_query(query: str) -> Any:
    """Parse a math query and execute it using SymPy/SciPy.

    Supported commands:
    - ``integrate <expr>`` for symbolic integration
    - ``integrate <expr> from <a> to <b>`` for numeric integration
    - ``differentiate <expr>`` for symbolic differentiation
    - ``solve <expr>`` to solve expressions equal to zero
    - ``simplify <expr>`` to simplify expressions
    Otherwise the expression is evaluated symbolically.
    """
    query = query.strip()
    # definite integral, prefer SciPy but fallback to SymPy if unavailable
    m = re.match(r"integrate\s+(.+)\s+from\s+(.+)\s+to\s+(.+)", query, re.I)
    if m:
        expr, lower, upper = m.groups()
        func = sp.lambdify(x, _safe_sympify(expr), "math")
        a = float(_safe_sympify(lower))
        b = float(_safe_sympify(upper))
        try:
            from scipy import integrate
            val, _ = integrate.quad(func, a, b)
        except ImportError:
            val = float(sp.integrate(_safe_sympify(expr), (x, a, b)))
        return val

    m = re.match(r"integrate\s+(.+)", query, re.I)
    if m:
        expr = m.group(1)
        return sp.integrate(_safe_sympify(expr), x)

    m = re.match(r"(differentiate|derive)\s+(.+)", query, re.I)
    if m:
        expr = m.group(2)
        return sp.diff(_safe_sympify(expr), x)

    m = re.match(r"solve\s+(.+)", query, re.I)
    if m:
        expr = m.group(1)
        return sp.solve(_safe_sympify(expr), x)

    m = re.match(r"simplify\s+(.+)", query, re.I)
    if m:
        expr = m.group(1)
        return sp.simplify(_safe_sympify(expr))

    return sp.simplify(_safe_sympify(query))

def math_agent_fn(state: Dict[str, Any]) -> Dict[str, Any]:
    query = state.get("query", "")
    result = parse_math_query(query)
    return {"result": result}


_graph = StateGraph(dict)
_graph.add_node("math", math_agent_fn)
_graph.set_entry_point("math")
app = _graph.compile()
