"""Run the trading pipeline with governance and debate gating."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Sequence, cast

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from naestro.agents import Role, RoleRegistry
from naestro.core.debate import DebateOrchestrator
from naestro.core.schemas import Message
from naestro.governance import Decision, Governor, Policy, PolicyResult

from packs.trading import (
    DebateGate,
    ExecutionAgent,
    RiskAgent,
    SignalAgent,
    TradingPipeline,
)


def build_gate() -> DebateGate:
    def analyst(history: Sequence[Message]) -> str:
        confidence = len(history) + 1
        if confidence > 1:
            return f"Approve with confidence {confidence}"
        return "Approve trade"

    def risk(history: Sequence[Message]) -> str:
        if any("drawdown" in message.content.lower() for message in history):
            return "Reject trade"
        return "Approve trade"

    registry = RoleRegistry(
        [
            Role("analyst", "Quant analyst", analyst),
            Role("risk", "Risk supervisor", risk),
        ]
    )
    orchestrator = DebateOrchestrator(registry)
    return DebateGate(orchestrator, ["analyst", "risk"])


def build_governor() -> Governor:
    governor = Governor()

    def max_drawdown(decision: Decision) -> PolicyResult:
        raw_drawdown = decision.metadata.get("max_drawdown", 0.0)
        drawdown = float(cast(float, raw_drawdown))
        passed = drawdown <= 2.5
        if passed:
            reason = "Within drawdown limit"
        else:
            reason = f"Drawdown {drawdown:.2f} exceeds limit"
        return PolicyResult(name="max_drawdown", passed=passed, reason=reason)

    def min_return(decision: Decision) -> PolicyResult:
        passed = decision.score >= 0.5
        reason = "Return target met" if passed else "Return target missed"
        return PolicyResult(name="min_return", passed=passed, reason=reason)

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
