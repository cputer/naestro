import math

import pytest

from src.examples.sympy_demo import solve_quadratic
from src.examples.scipy_demo import integrate_sin


def test_sympy_demo():
    assert solve_quadratic(1, 0, -4) == [-2, 2]


def test_scipy_demo():
    result = integrate_sin()
    assert result == pytest.approx(2.0, abs=1e-6)
