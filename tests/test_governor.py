from __future__ import annotations

from naestro.governance import Decision, Governor, Policy, PolicyInput


def test_governor_enforces_policies() -> None:
    governor = Governor()

    def positive_return(payload: PolicyInput) -> Decision:
        score = payload.score or 0.0
        passed = score > 0
        reason = "positive" if passed else "negative"
        return Decision(name="positive_return", passed=passed, reason=reason)

    def drawdown_cap(payload: PolicyInput) -> Decision:
        drawdown = float(payload.metadata.get("max_drawdown", 0.0))
        passed = drawdown <= 1.5
        reason = "ok" if passed else "too high"
        return Decision(name="drawdown_cap", passed=passed, reason=reason)

    governor.register(Policy("return", "Requires positive return", positive_return))
    governor.register(Policy("drawdown", "Caps drawdown", drawdown_cap))

    policy_input = PolicyInput(subject="test", score=0.1, metadata={"max_drawdown": 2.0})
    allowed, results = governor.enforce(policy_input)
    assert not allowed
    assert any(not result.passed for result in results)
