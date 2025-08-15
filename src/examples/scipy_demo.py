"""Integrate sin(x) using SciPy.

Usage:
    python -m src.examples.scipy_demo [a] [b]
    # Integrates sin(x) from a (default 0) to b (default pi).
"""
from __future__ import annotations

import argparse
import math
from scipy import integrate


def integrate_sin(a: float = 0.0, b: float = math.pi) -> float:
    """Return the integral of sin(x) from a to b."""
    result, _ = integrate.quad(math.sin, a, b)
    return result


def main():
    parser = argparse.ArgumentParser(description="Integrate sin(x) from a to b")
    parser.add_argument("a", nargs="?", type=float, default=0.0)
    parser.add_argument("b", nargs="?", type=float, default=math.pi)
    args = parser.parse_args()
    print(integrate_sin(args.a, args.b))


if __name__ == "__main__":
    main()
