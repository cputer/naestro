import pytest

from src.prompt.composer import add_collab_headers, choose_answer


def test_mode_depth_tokens_injected():
    prefs = {"mode": "collaborate", "depth": 2}
    prompt = add_collab_headers("Solve X", prefs)
    assert prompt.startswith("<<cop.mode:collaborate>> <<cop.depth:2>>")


def test_answer_strategy_self_if_confident():
    responses = [
        {"content": "A", "confidence": 0.9},
        {"content": "B", "confidence": 0.8},
    ]
    prefs = {"answer_strategy": "self_if_confident", "confidence_threshold": 0.7}
    assert choose_answer(responses, prefs) == "A"

    low_conf = [{"content": "A", "confidence": 0.5}, {"content": "B", "confidence": 0.4}]
    assert choose_answer(low_conf, prefs) == "A\nB"


def test_answer_strategy_aggregate_always():
    responses = [
        {"content": "A", "confidence": 0.2},
        {"content": "B", "confidence": 0.1},
    ]
    prefs = {"answer_strategy": "aggregate_always"}
    assert choose_answer(responses, prefs) == "A\nB"


def test_answer_strategy_ask_clarify_below_threshold():
    responses = [
        {"content": "A", "confidence": 0.3},
        {"content": "B", "confidence": 0.2},
    ]
    prefs = {"answer_strategy": "ask_clarify_below_threshold", "confidence_threshold": 0.8}
    assert choose_answer(responses, prefs) == "clarify"

    high_conf = [
        {"content": "A", "confidence": 0.95},
        {"content": "B", "confidence": 0.9},
    ]
    assert choose_answer(high_conf, prefs) == "A\nB"
