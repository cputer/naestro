from src.prompt.composer import add_collab_headers, choose_answer
from src.telemetry import metrics


def test_add_collab_headers_records_metrics():
    metrics.collab_prompts.reset()
    metrics.collab_prompt_depth.reset()
    add_collab_headers("hi", {"mode": "consult", "depth": 2})
    assert metrics.collab_prompts.get("consult") == 1
    assert metrics.collab_prompt_depth.get("consult") == 2


def test_choose_answer_empty_responses_returns_blank(monkeypatch):
    called = False

    def fake(p):
        nonlocal called
        called = True
        return p

    monkeypatch.setattr("src.prompt.composer.clamp_prefs", fake)
    assert choose_answer([], {}) == ""
    assert called is False


def test_choose_answer_unknown_strategy_aggregates():
    responses = [{"content": "A", "confidence": 0.1}]
    assert choose_answer(responses, {"answer_strategy": "mystery"}) == "A"


def test_choose_answer_fallback(monkeypatch):
    responses = [{"content": "A"}]
    monkeypatch.setattr(
        "src.prompt.composer.clamp_prefs", lambda p: p  # bypass clamping
    )
    prefs = {"answer_strategy": "unknown", "confidence_threshold": 0.0}
    assert choose_answer(responses, prefs) == "A"
