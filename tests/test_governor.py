from __future__ import annotations

from naestro.governance import Decision, Governor, Policy, PolicyResult


def test_governor_enforces_policies() -> None:
    governor = Governor()

    def positive_return(decision: Decision) -> PolicyResult:
        passed = decision.score > 0
        reason = "positive" if passed else "negative"
        return PolicyResult(name="positive_return", passed=passed, reason=reason)

    def drawdown_cap(decision: Decision) -> PolicyResult:
        drawdown = float(decision.metadata.get("max_drawdown", 0.0))
        passed = drawdown <= 1.5
        reason = "ok" if passed else "too high"
        return PolicyResult(name="drawdown_cap", passed=passed, reason=reason)

    governor.register(Policy("return", "Requires positive return", positive_return))
    governor.register(Policy("drawdown", "Caps drawdown", drawdown_cap))

    decision = Decision(subject="test", score=0.1, metadata={"max_drawdown": 2.0})
    allowed, results = governor.enforce(decision)
    assert not allowed
    assert any(not result.passed for result in results)
