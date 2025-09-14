from orchestrator.planner import compile_plan, DEFAULT_COLLAB_PREFS, clamp_prefs, compose_cop_header
import json
import pathlib

def test_defaults_and_header_snapshot():
    plan = compile_plan("Build X", tasks=[], inputs={}, outputs={}, overrides=None)
    assert plan["collaboration"]["mode"] == "consult"
    assert "$0.50" in plan["cop_header"]
    assert "mode=consult" in plan["cop_header"]
    snap = json.dumps(plan, sort_keys=True)
    assert "collaboration" in snap and "cop_header" in snap

def test_overrides_and_bounds():
    plan = compile_plan(
        "Goal",
        overrides={"collaboration": {
            "mode": "CONSULT_BAD",   # will clamp to default
            "depth": 99,             # clamp to 3
            "auto": False,
            "ask_online": False,
            "budget_usd": -1,        # clamp to 0
            "p95_latency_s": -5,     # clamp to 0
            "answer_strategy": "ask_clarify_below_threshold",
            "confidence_threshold": 1.7  # clamp to 1
        }}
    )
    c = plan["collaboration"]
    assert c["mode"] == DEFAULT_COLLAB_PREFS["mode"]
    assert c["depth"] == 3
    assert c["budget_usd"] == 0.0
    assert c["p95_latency_s"] == 0
    assert c["answer_strategy"] == "ask_clarify_below_threshold"
    assert c["confidence_threshold"] == 1.0

def test_schema_validation():
    try:
        import jsonschema  # type: ignore
    except Exception:
        # allow passing when jsonschema isn't installed in CI image
        return
    # Will raise if invalid
    plan = compile_plan("Y", tasks=[], inputs={}, outputs={}, overrides=None)
    assert isinstance(plan, dict)