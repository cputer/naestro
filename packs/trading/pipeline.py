"""End-to-end trading pipeline with optional debate gating and governance."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Sequence

from naestro.agents import DebateOrchestrator, DebateSettings
from naestro.governance import Decision, Governor, PolicyInput

from .agents import ExecutionAgent, PriceSeries, RiskAgent, SignalAgent, TradeDecision
from .backtest import BacktestResult, run_backtest


@dataclass(slots=True)
class DebateGate:
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
        if not messages:
            return True
        if len(messages) <= 1:
            return True
        if messages[-1].role == "system":
            return True
        final_message = messages[-1].content.lower()
        if "reject" in final_message:
            return False
        if "approve" in final_message or "proceed" in final_message:
            return True
        return "buy" in final_message or "yes" in final_message


@dataclass(slots=True)
class PipelineResult:
    trades: List[TradeDecision]
    rejected_trades: List[TradeDecision]
    backtest: BacktestResult
    approved: bool
    governance_results: List[Decision] = field(default_factory=list)


class TradingPipeline:
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
        risk_screened = self._risk_agent.filter(signals)
        trades = self._execution_agent.execute(risk_screened, prices)
        approved_trades: List[TradeDecision] = []
        rejected_trades: List[TradeDecision] = []
        for trade in trades:
            if self._debate_gate is None or self._debate_gate.approve(trade):
                approved_trades.append(trade)
            else:
                rejected_trades.append(trade)
        backtest = run_backtest(prices, approved_trades)
        governance_results: List[Decision] = []
        approved = True
        if self._governor is not None:
            policy_input = PolicyInput(
                subject="trading-pipeline",
                score=backtest.metrics.get("cumulative_return", 0.0),
                metadata={"max_drawdown": backtest.metrics.get("max_drawdown", 0.0)},
            )
            approved, governance_results = self._governor.enforce(policy_input)
        return PipelineResult(
            trades=approved_trades,
            rejected_trades=rejected_trades,
            backtest=backtest,
            approved=approved,
            governance_results=governance_results,
        )


__all__ = ["DebateGate", "PipelineResult", "TradingPipeline"]
