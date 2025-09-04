import builtins

import pytest

from src.orchestrator.math_agent import app as math_app
from src.orchestrator.math_agent import parse_math_query


def test_parse_integrate_symbolic():
    result = parse_math_query("integrate x**2")
    assert str(result) == "x**3/3"


def test_parse_differentiate():
    result = parse_math_query("differentiate sin(x)")
    assert str(result) == "cos(x)"


def test_parse_solve():
    result = parse_math_query("solve x**2 - 4")
    assert set(map(str, result)) == {"-2", "2"}


def test_parse_definite_integral():
    result = parse_math_query("integrate sin(x) from 0 to pi")
    assert result == pytest.approx(2.0, rel=1e-6)


def test_parse_definite_integral_without_scipy(monkeypatch):
    original_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "scipy" or name.startswith("scipy."):
            raise ImportError
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    result = parse_math_query("integrate sin(x) from 0 to pi")
    assert result == pytest.approx(2.0, rel=1e-6)


def test_math_app_invoke():
    res = math_app.invoke({"query": "differentiate x**2"})
    assert str(res["result"]) == "2*x"


def test_invalid_symbol_rejected():
    with pytest.raises(ValueError):
        parse_math_query("solve y + 1")


def test_malicious_expression_rejected():
    with pytest.raises(ValueError):
        parse_math_query("__import__('os')")


def test_invalid_integral_bound():
    with pytest.raises(ValueError):
        parse_math_query("integrate x from 0 to y")


def test_parse_simplify():
    result = parse_math_query("simplify sin(x)**2 + cos(x)**2")
    assert str(result) == "1"
