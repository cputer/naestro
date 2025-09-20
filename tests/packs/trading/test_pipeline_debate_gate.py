from __future__ import annotations

from typing import Sequence

from naestro.agents import Role, RoleRegistry
from naestro.core.debate import DebateOrchestrator
from naestro.core.schemas import Message

from packs.trading import (
    DebateGate,
    ExecutionAgent,
    RiskAgent,
    SignalAgent,
    TradingPipeline,
)


def test_pipeline_debate_gate_filters_trades() -> None:
    prices = [100.0, 100.2, 100.5, 100.4, 100.7]

    def analyst(history: Sequence[Message]) -> str:
        return "Approve trade"

    def risk(history: Sequence[Message]) -> str:
        prompt = history[0].content if history else ""
        return "Reject trade" if "100.50" in prompt else "Approve trade"

    registry = RoleRegistry(
        [
            Role("analyst", "Analyst", analyst),
            Role("risk", "Risk", risk),
        ]
    )
    gate = DebateGate(DebateOrchestrator(registry), ["analyst", "risk"])
    pipeline = TradingPipeline(
        SignalAgent(window=2),
        RiskAgent(max_exposure=2, min_confidence=0.05),
        ExecutionAgent(),
        debate_gate=gate,
    )
    result = pipeline.run(prices)
    assert len(result.trades) == 1
    assert len(result.rejected_trades) == 1
    assert result.rejected_trades[0].price == 100.5
