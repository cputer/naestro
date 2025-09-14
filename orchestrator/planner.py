from __future__ import annotations
from typing import Any, Dict, List, Optional
import json
from copy import deepcopy

try:
    import jsonschema  # type: ignore
    _HAS_JSONSCHEMA = True
except Exception:
    _HAS_JSONSCHEMA = False

DEFAULT_COLLAB_PREFS: Dict[str, Any] = {
    "mode": "consult",
    "depth": 1,
    "auto": True,
    "ask_online": True,
    "budget_usd": 0.50,
    "p95_latency_s": 20,
    "answer_strategy": "self_if_confident",
    "confidence_threshold": 0.70,
}

_ALLOWED_MODES = {"solo", "consult", "collaborate", "consensus", "swarm"}
_ALLOWED_STRATS = {"self_if_confident", "aggregate_always", "ask_clarify_below_threshold"}

def clamp_prefs(prefs: Dict[str, Any]) -> Dict[str, Any]:
    out = deepcopy(DEFAULT_COLLAB_PREFS)
    out.update(prefs or {})
    # enums
    if out["mode"] not in _ALLOWED_MODES:
        out["mode"] = DEFAULT_COLLAB_PREFS["mode"]
    if out["answer_strategy"] not in _ALLOWED_STRATS:
        out["answer_strategy"] = DEFAULT_COLLAB_PREFS["answer_strategy"]
    # ints/floats
    out["depth"] = max(0, min(3, int(out.get("depth", 0))))
    out["p95_latency_s"] = max(0, int(out.get("p95_latency_s", 0)))
    out["budget_usd"] = max(0.0, float(out.get("budget_usd", 0.0)))
    # booleans
    out["auto"] = bool(out.get("auto", False))
    out["ask_online"] = bool(out.get("ask_online", False))
    # threshold
    try:
        thr = float(out.get("confidence_threshold", 0.0))
    except Exception:
        thr = DEFAULT_COLLAB_PREFS["confidence_threshold"]
    out["confidence_threshold"] = max(0.0, min(1.0, thr))
    return out

def compose_cop_header(prefs: Dict[str, Any]) -> str:
    b = clamp_prefs(prefs)
    auto = "✓" if b["auto"] else "✗"
    ask = "✓" if b["ask_online"] else "✗"
    return (
        "COP: "
        f"mode={b['mode']} "
        f"depth={b['depth']} "
        f"auto={auto} "
        f"ask_online={ask} "
        f"budget=${b['budget_usd']:.2f} "
        f"p95={b['p95_latency_s']}s "
        f"strategy={b['answer_strategy']}(th={b['confidence_threshold']:.2f})"
    )

def _maybe_validate(plan: Dict[str, Any]) -> None:
    if not _HAS_JSONSCHEMA:
        return
    import pathlib, json  # local import to keep optional
    schema_path = pathlib.Path("schemas/plan.schema.json")
    if schema_path.exists():
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        jsonschema.validate(instance=plan, schema=schema)

def compile_plan(
    goal: str,
    tasks: Optional[List[Dict[str, Any]]] = None,
    inputs: Optional[Dict[str, Any]] = None,
    outputs: Optional[Dict[str, Any]] = None,
    overrides: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    tasks = tasks or []
    inputs = inputs or {}
    outputs = outputs or {}
    overrides = overrides or {}

    collab = clamp_prefs((overrides.get("collaboration") or {}))
    cop_header = compose_cop_header(collab)

    plan: Dict[str, Any] = {
        "goal": goal,
        "tasks": tasks,
        "inputs": inputs,
        "outputs": outputs,
        "collaboration": collab,
        "cop_header": cop_header,
    }

    _maybe_validate(plan)
    # stable (deterministic) keys for tests — consumers can json.dumps(sort_keys=True)
    json.loads(json.dumps(plan, sort_keys=True))
    return plan