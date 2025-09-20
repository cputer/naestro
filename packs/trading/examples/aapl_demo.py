"""Run the TradingAgents demo pipeline with bundled sample data."""
from __future__ import annotations

import csv
from importlib import resources
from typing import Sequence

from naestro.agents import DebateOrchestrator, Message, Role, Roles
from packs.trading import DebateGate, trading_demo


def _build_gate() -> DebateGate:
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
    sample_path = resources.files("packs.trading.examples").joinpath("sample.csv")
    with sample_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        prices = [float(row["close"]) for row in reader]
    result = trading_demo(prices, debate_gate=_build_gate())
    print("Approved trades:")
    for trade in result.trades:
        print(
            f"  idx={trade.index} price={trade.price:.2f} note={trade.note}"
            f" conf={trade.confidence:.2f}"
        )
    print("Backtest metrics:", result.backtest.metrics)


if __name__ == "__main__":
    main()
