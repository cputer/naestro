import math
import runpy
import sys

import pytest

from src.examples import scipy_demo, sympy_demo
from src.examples.scipy_demo import integrate_sin
from src.examples.sympy_demo import solve_quadratic


def test_sympy_demo():
    assert solve_quadratic(1, 0, -4) == [-2, 2]


def test_scipy_demo():
    result = integrate_sin()
    assert result == pytest.approx(2.0, abs=1e-6)


def test_sympy_demo_main(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["prog", "1", "0", "-4"])
    sympy_demo.main()
    out = capsys.readouterr().out
    assert "-2" in out and "2" in out


def test_scipy_demo_main(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["prog", "0", str(math.pi)])
    scipy_demo.main()
    out = capsys.readouterr().out.strip()
    assert float(out) == pytest.approx(2.0, abs=1e-6)


def test_sympy_demo_run_module(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["prog", "1", "0", "-4"])
    runpy.run_module("src.examples.sympy_demo", run_name="__main__")
    out = capsys.readouterr().out
    assert "-2" in out and "2" in out


def test_scipy_demo_run_module(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["prog", "0", str(math.pi)])
    runpy.run_module("src.examples.scipy_demo", run_name="__main__")
    out = capsys.readouterr().out.strip()
    assert float(out) == pytest.approx(2.0, abs=1e-6)
