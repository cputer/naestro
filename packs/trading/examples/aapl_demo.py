"""Small end-to-end trading demo using bundled price data."""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import List, Sequence

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[3]))

from naestro.agents import DebateOrchestrator, Message, Role, Roles

from packs.trading import (
    DebateGate,
    ExecutionAgent,
    RiskAgent,
    SignalAgent,
    TradingPipeline,
)


def load_prices() -> List[float]:
    path = Path(__file__).with_name("sample.csv")
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [float(row["close"]) for row in reader]


def build_gate() -> DebateGate:
    def analyst(history: Sequence[Message]) -> str:
        return "Approve trade" if len(history) % 2 == 0 else "Approve with caution"

    def risk(history: Sequence[Message]) -> str:
        return "Reject trade" if len(history) == 0 else "Approve trade"

    roles = Roles()
    roles.register(Role("analyst", "Analyst", analyst))
    roles.register(Role("risk", "Risk", risk))
    orchestrator = DebateOrchestrator(roles)
    return DebateGate(orchestrator, ["analyst", "risk"])


def main() -> None:
    prices = load_prices()
    pipeline = TradingPipeline(
        SignalAgent(window=3),
        RiskAgent(max_exposure=1, min_confidence=0.1),
        ExecutionAgent(),
        debate_gate=build_gate(),
    )
    result = pipeline.run(prices)
    print("Approved trades:")
    for trade in result.trades:
        print(f"  idx={trade.index} price={trade.price:.2f} note={trade.note}")
    print("Backtest metrics:", result.backtest.metrics)


if __name__ == "__main__":
    main()
