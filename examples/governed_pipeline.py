"""Execute the trading pipeline with both debate gating and governance."""

import sys
from pathlib import Path
from typing import Sequence, cast

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from naestro import Decision, DebateOrchestrator, Message, Policy, PolicyInput, Role, Roles
from naestro import Governor

from packs.trading import DebateGate, ExecutionAgent, RiskAgent, SignalAgent, TradingPipeline


def build_gate() -> DebateGate:
    """Configure a deterministic gate with analyst and risk roles."""

    def analyst(history: Sequence[Message]) -> str:
        confidence = len(history) + 1
        return f"Approve with confidence {confidence}" if confidence > 1 else "Approve trade"

    def risk(history: Sequence[Message]) -> str:
        if any("drawdown" in message.content.lower() for message in history):
            return "Reject trade"
        return "Approve trade"

    roles = Roles()
    roles.register(Role("analyst", "Quant analyst", analyst))
    roles.register(Role("risk", "Risk supervisor", risk))
    orchestrator = DebateOrchestrator(roles)
    return DebateGate(orchestrator, ["analyst", "risk"])


def build_governor() -> Governor:
    """Create a governor enforcing drawdown and return policies."""

    governor = Governor()

    def max_drawdown(payload: PolicyInput) -> Decision:
        raw_drawdown = payload.metadata.get("max_drawdown", 0.0)
        drawdown = float(cast(float, raw_drawdown))
        passed = drawdown <= 2.5
        reason = "Within drawdown limit" if passed else f"Drawdown {drawdown:.2f} exceeds limit"
        return Decision(name="max_drawdown", passed=passed, reason=reason)

    def min_return(payload: PolicyInput) -> Decision:
        score = payload.score or 0.0
        passed = score >= 0.5
        reason = "Return target met" if passed else "Return target missed"
        return Decision(name="min_return", passed=passed, reason=reason)

    governor.register(Policy("max_drawdown", "Limit drawdowns", max_drawdown))
    governor.register(Policy("min_return", "Ensure positive returns", min_return))
    return governor


def main() -> None:
    prices = [100.0, 101.0, 102.5, 101.5, 103.0, 104.5]
    pipeline = TradingPipeline(
        SignalAgent(window=2),
        RiskAgent(max_exposure=1, min_confidence=0.1),
        ExecutionAgent(),
        debate_gate=build_gate(),
        governor=build_governor(),
    )
    result = pipeline.run(prices)
    print("Approved trades:")
    for trade in result.trades:
        print(f"  index={trade.index} price={trade.price:.2f} note={trade.note}")
    print("Rejected trades:")
    for trade in result.rejected_trades:
        print(f"  index={trade.index} price={trade.price:.2f} note={trade.note}")
    print("Metrics:", result.backtest.metrics)
    print("Governance:")
    for policy_result in result.governance_results:
        status = "PASS" if policy_result.passed else "FAIL"
        print(f"  {policy_result.name}: {status} - {policy_result.reason}")
    print("Pipeline approved:", result.approved)


if __name__ == "__main__":
    main()
