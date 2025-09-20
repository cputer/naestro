"""Trading pipelines and helpers aligned with the TradingAgents prompt."""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from importlib import resources
from typing import List, Sequence

from naestro.agents import DebateOrchestrator, DebateSettings
from naestro.governance import Decision, Governor, PolicyInput

from .agents import ExecutionAgent, PriceSeries, RiskAgent, SignalAgent, TradeDecision
from .backtest import BacktestResult, run_backtest


@dataclass(slots=True)
class DebateGate:
    """Deterministic gate that reuses the Naestro debate orchestrator."""

    orchestrator: DebateOrchestrator
    participants: Sequence[str]
    template: str = (
        "Should we execute a trade at price {price:.2f} with note '{note}'? "
        "Respond with approve or reject."
    )

    def approve(self, trade: TradeDecision) -> bool:
        prompt = self.template.format(price=trade.price, note=trade.note)
        outcome = self.orchestrator.run(
            self.participants,
            prompt,
            settings=DebateSettings(rounds=1),
        )
        messages = outcome.transcript.messages
        if not messages or len(messages) <= 1:
            return True
        final = messages[-1].content.lower()
        if "reject" in final:
            return False
        if "approve" in final or "proceed" in final:
            return True
        return "buy" in final or "yes" in final


@dataclass(slots=True)
class PipelineResult:
    """Structured output combining trades, backtest and governance results."""

    trades: List[TradeDecision]
    rejected_trades: List[TradeDecision]
    backtest: BacktestResult
    approved: bool
    governance_results: List[Decision] = field(default_factory=list)


class TradingPipeline:
    """Deterministic pipeline mirroring the TradingAgents prompt flow."""

    def __init__(
        self,
        signal_agent: SignalAgent,
        risk_agent: RiskAgent,
        execution_agent: ExecutionAgent,
        *,
        debate_gate: DebateGate | None = None,
        governor: Governor | None = None,
    ) -> None:
        self._signal_agent = signal_agent
        self._risk_agent = risk_agent
        self._execution_agent = execution_agent
        self._debate_gate = debate_gate
        self._governor = governor

    def run(self, prices: PriceSeries) -> PipelineResult:
        signals = self._signal_agent.generate(prices)
        screened = self._risk_agent.filter(signals)
        trades = self._execution_agent.execute(screened, prices)
        approved: List[TradeDecision] = []
        rejected: List[TradeDecision] = []
        for trade in trades:
            gate_pass = True
            if self._debate_gate is not None:
                gate_pass = self._debate_gate.approve(trade)
            if gate_pass:
                approved.append(trade)
            else:
                rejected.append(trade)
        backtest = run_backtest(prices, approved)
        approved_flag = True
        governance_results: List[Decision] = []
        if self._governor is not None:
            policy_input = PolicyInput(
                subject="trading-demo",
                score=backtest.metrics.get("cumulative_return", 0.0),
                metadata={
                    "max_drawdown": backtest.metrics.get("max_drawdown", 0.0),
                    "win_rate": backtest.metrics.get("win_rate", 0.0),
                },
            )
            approved_flag, governance_results = self._governor.enforce(policy_input)
        return PipelineResult(
            trades=approved,
            rejected_trades=rejected,
            backtest=backtest,
            approved=approved_flag,
            governance_results=governance_results,
        )


def _load_sample_prices() -> List[float]:
    with resources.files("packs.trading.examples").joinpath("sample.csv").open(
        "r", encoding="utf-8"
    ) as handle:
        reader = csv.DictReader(handle)
        return [float(row["close"]) for row in reader]


def trading_demo(
    prices: Sequence[float] | None = None,
    *,
    window: int = 4,
    max_exposure: int = 1,
    min_confidence: float = 0.2,
    debate_gate: DebateGate | None = None,
    governor: Governor | None = None,
) -> PipelineResult:
    """Run the prompt-aligned trading demo pipeline."""

    if prices is None:
        prices = _load_sample_prices()
    pipeline = TradingPipeline(
        SignalAgent(window=window),
        RiskAgent(max_exposure=max_exposure, min_confidence=min_confidence),
        ExecutionAgent(),
        debate_gate=debate_gate,
        governor=governor,
    )
    return pipeline.run(list(prices))


__all__ = [
    "BacktestResult",
    "DebateGate",
    "PipelineResult",
    "TradingPipeline",
    "trading_demo",
]
