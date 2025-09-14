import json
from pathlib import Path

import pytest

from orchestrator.planner import DEFAULT_COLLAB_PREFS, clamp_prefs, compile_plan


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
        overrides={
            "collaboration": {
                "mode": "CONSULT_BAD",  # will clamp to default
                "depth": 99,  # clamp to 3
                "auto": False,
                "ask_online": False,
                "budget_usd": -1,  # clamp to 0
                "p95_latency_s": -5,  # clamp to 0
                "answer_strategy": "ask_clarify_below_threshold",
                "confidence_threshold": 1.7,  # clamp to 1
            }
        },
    )
    c = plan["collaboration"]
    assert c["mode"] == DEFAULT_COLLAB_PREFS["mode"]
    assert c["depth"] == 3
    assert c["budget_usd"] == 0.0
    assert c["p95_latency_s"] == 0
    assert c["answer_strategy"] == "ask_clarify_below_threshold"
    assert c["confidence_threshold"] == 1.0


def test_schema_validation():
    jsonschema = pytest.importorskip("jsonschema")
    plan = compile_plan("Y", tasks=[], inputs={}, outputs={}, overrides=None)
    schema_path = Path(__file__).resolve().parents[2] / "schemas" / "plan.schema.json"
    with open(schema_path) as f:
        schema = json.load(f)
    jsonschema.validate(plan, schema)
    assert isinstance(plan, dict)


def test_unknown_pref_keys_removed():
    prefs = {"mode": "solo", "extra": 42}
    clamped = clamp_prefs(prefs)
    assert clamped["mode"] == "solo"
    assert "extra" not in clamped
