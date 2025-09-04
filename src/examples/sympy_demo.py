"""Solve quadratic equations using SymPy.

Usage:
    python -m src.examples.sympy_demo a b c
    # Solves a*x**2 + b*x + c = 0 and prints roots.
"""
from __future__ import annotations

import argparse
from sympy import Eq, symbols, solve


def solve_quadratic(a: float, b: float, c: float):
    """Return solutions to a*x**2 + b*x + c = 0."""
    x = symbols("x")
    equation = Eq(a * x**2 + b * x + c, 0)
    return solve(equation, x)


def main():
    parser = argparse.ArgumentParser(description="Solve quadratic equation")
    parser.add_argument("a", type=float, help="Quadratic coefficient")
    parser.add_argument("b", type=float, help="Linear coefficient")
    parser.add_argument("c", type=float, help="Constant term")
    args = parser.parse_args()
    roots = solve_quadratic(args.a, args.b, args.c)
    print(roots)


if __name__ == "__main__":  # pragma: no cover
    main()
