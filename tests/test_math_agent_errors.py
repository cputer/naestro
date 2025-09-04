import pytest

from src.orchestrator.math_agent import parse_math_query


def test_parse_math_query_error() -> None:
    with pytest.raises(Exception):
        parse_math_query("this is not a math expression")
