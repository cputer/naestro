import re
from typing import Any, Dict

import sympy as sp
from langgraph.graph import StateGraph

x = sp.symbols("x")


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
    # definite integral using SciPy
    m = re.match(r"integrate\s+(.+)\s+from\s+(.+)\s+to\s+(.+)", query, re.I)
    if m:
        expr, lower, upper = m.groups()
        func = sp.lambdify(x, sp.sympify(expr), "math")
        a = float(sp.sympify(lower))
        b = float(sp.sympify(upper))
        try:
            from scipy import integrate  # type: ignore

            val, _ = integrate.quad(func, a, b)
        except ImportError:
            val = float(sp.integrate(sp.sympify(expr), (x, a, b)).evalf())
        return val

    m = re.match(r"integrate\s+(.+)", query, re.I)
    if m:
        expr = m.group(1)
        return sp.integrate(sp.sympify(expr), x)

    m = re.match(r"(differentiate|derive)\s+(.+)", query, re.I)
    if m:
        expr = m.group(2)
        return sp.diff(sp.sympify(expr), x)

    m = re.match(r"solve\s+(.+)", query, re.I)
    if m:
        expr = m.group(1)
        return sp.solve(sp.sympify(expr), x)

    m = re.match(r"simplify\s+(.+)", query, re.I)
    if m:
        expr = m.group(1)
        return sp.simplify(sp.sympify(expr))

    return sp.simplify(sp.sympify(query))


def math_agent_fn(state: Dict[str, Any]) -> Dict[str, Any]:
    query = state.get("query", "")
    result = parse_math_query(query)
    return {"result": result}


_graph = StateGraph(dict)
_graph.add_node("math", math_agent_fn)
_graph.set_entry_point("math")
app = _graph.compile()
