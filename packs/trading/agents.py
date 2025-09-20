"""Trading oriented agents built on top of the debate primitives."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence

PriceSeries = Sequence[float]


@dataclass(slots=True)
class Signal:
    index: int
    position: int
    confidence: float
    rationale: str


@dataclass(slots=True)
class TradeDecision:
    index: int
    position: int
    price: float
    note: str


class SignalAgent:
    def __init__(self, window: int = 3) -> None:
        self._window = window

    def generate(self, prices: PriceSeries) -> List[Signal]:
        signals: List[Signal] = []
        if len(prices) <= self._window:
            return signals
        for idx in range(self._window, len(prices)):
            recent = prices[idx - self._window : idx]
            moving_average = sum(recent) / float(self._window)
            delta = prices[idx] - moving_average
            position = 1 if delta > 0 else 0
            confidence = min(1.0, abs(delta))
            rationale = (
                "above moving average" if position == 1 else "below moving average"
            )
            signals.append(
                Signal(
                    index=idx,
                    position=position,
                    confidence=confidence,
                    rationale=rationale,
                )
            )
        return signals


class RiskAgent:
    def __init__(self, max_exposure: int = 1, min_confidence: float = 0.15) -> None:
        self._max_exposure = max_exposure
        self._min_confidence = min_confidence

    def filter(self, signals: Sequence[Signal]) -> List[Signal]:
        filtered: List[Signal] = []
        exposure = 0
        for signal in signals:
            if signal.position == 1:
                if signal.confidence < self._min_confidence:
                    continue
                if exposure >= self._max_exposure:
                    continue
                exposure += 1
            else:
                exposure = 0
            filtered.append(signal)
        return filtered


class ExecutionAgent:
    def execute(
        self, signals: Sequence[Signal], prices: PriceSeries
    ) -> List[TradeDecision]:
        decisions: List[TradeDecision] = []
        for signal in signals:
            price = prices[signal.index]
            note = "enter" if signal.position == 1 else "flat"
            decisions.append(
                TradeDecision(
                    index=signal.index,
                    position=signal.position,
                    price=price,
                    note=note,
                )
            )
        return decisions


__all__ = [
    "ExecutionAgent",
    "PriceSeries",
    "RiskAgent",
    "Signal",
    "SignalAgent",
    "TradeDecision",
]
