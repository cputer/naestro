from __future__ import annotations

from pathlib import Path
from sys import path as sys_path
from typing import Mapping

if __package__ in {None, ""}:
    sys_path.append(str(Path(__file__).resolve().parents[1]))

import pytest

pytest.importorskip("jsonschema")

from naestro.core.bus import MessageBus
from naestro.governance.governor import apply_patches, Governor
from naestro.governance.policies import Policy
from naestro.governance.schemas import Decision, PolicyInput


def _governor_schema() -> Mapping[str, object]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "events": {
            "governor.evaluated": {
                "type": "object",
                "additionalProperties": False,
                "required": ["input", "results", "approved"],
                "properties": {
                    "input": {"type": "object"},
                    "results": {"type": "array"},
                    "approved": {"type": "boolean"},
                },
            }
        },
    }


def test_governor_enforces_policies_and_publishes_results() -> None:
    bus = MessageBus(schema=_governor_schema())
    published: list[Mapping[str, object]] = []
    bus.subscribe("governor.evaluated", lambda payload: published.append(payload))

    def positive_return(payload: PolicyInput) -> Decision:
        score = payload.score or 0.0
        passed = score > 0
        reason = "positive" if passed else "negative"
        return Decision(name="positive_return", passed=passed, reason=reason)

    def drawdown_cap(payload: PolicyInput) -> Decision:
        drawdown = float(payload.metadata.get("max_drawdown", 0.0))
        passed = drawdown <= 1.5
        patches: tuple[dict[str, object], ...] = ()
        if not passed:
            patches = ({"op": "set", "path": ("status",), "value": "review"},)
        decision = Decision(
            name="drawdown_cap",
            passed=passed,
            reason="ok" if passed else "too high",
            patches=patches,
        )
        return decision

    policies = [
        Policy("return", "Requires positive return", positive_return),
        Policy("drawdown", "Caps drawdown", drawdown_cap),
    ]
    governor = Governor(policies, bus=bus)

    policy_input = PolicyInput(
        subject="test",
        score=-0.1,
        metadata={"max_drawdown": 2.0},
        plan={"status": "proposed"},
    )
    allowed, results, updated_input = governor.enforce(
        policy_input, apply_policy_patches=True, return_input=True
    )

    assert not allowed
    assert [result.passed for result in results] == [False, False]
    assert updated_input.plan["status"] == "review"
    assert bus.envelopes[0].event == "governor.evaluated"
    assert published and published[0]["approved"] is False
    assert len(published[0]["results"]) == 2


def test_apply_patches_supports_merge_and_remove() -> None:
    plan = {"status": "pending", "steps": [{"name": "a"}, {"name": "b"}]}
    patches = (
        {"op": "set", "path": ("steps", 0, "name"), "value": "approved"},
        {"op": "remove", "path": ("steps", 1)},
        {"op": "merge", "path": ("metadata",), "value": {"owner": "alice"}},
    )

    updated = apply_patches(plan, patches)
    assert updated["steps"][0]["name"] == "approved"
    assert len(updated["steps"]) == 1
    assert updated["metadata"]["owner"] == "alice"
    assert "metadata" not in plan
