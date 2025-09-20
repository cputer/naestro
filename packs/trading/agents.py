"""Deterministic trading agents mirroring the TradingAgents prompt."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

PriceSeries = Sequence[float]


@dataclass(slots=True)
class Signal:
    """Intermediate signal proposed by the signal agent."""

    index: int
    position: int
    confidence: float
    rationale: str


@dataclass(slots=True)
class TradeDecision:
    """Final trade decision emitted by the execution agent."""

    index: int
    position: int
    price: float
    note: str
    confidence: float = 0.0
    rationale: str = ""


class SignalAgent:
    """Generates simple momentum signals using a rolling mean window."""

    def __init__(self, window: int = 3) -> None:
        if window < 1:
            raise ValueError("window must be positive")
        self._window = window

    def generate(self, prices: PriceSeries) -> List[Signal]:
        signals: List[Signal] = []
        if len(prices) <= self._window:
            return signals
        for idx in range(self._window, len(prices)):
            recent = prices[idx - self._window : idx]
            moving_average = sum(recent) / float(self._window)
            price = prices[idx]
            delta = price - moving_average
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
    """Filters signals to enforce exposure and confidence limits."""

    def __init__(
        self,
        max_exposure: int = 1,
        min_confidence: float = 0.2,
        cooldown: int = 0,
    ) -> None:
        if max_exposure < 1:
            raise ValueError("max_exposure must be at least 1")
        self._max_exposure = max_exposure
        self._min_confidence = min_confidence
        self._cooldown = cooldown

    def filter(self, signals: Iterable[Signal]) -> List[Signal]:
        filtered: List[Signal] = []
        exposure = 0
        cooldown_remaining = 0
        for signal in signals:
            if cooldown_remaining:
                cooldown_remaining -= 1
                continue
            if signal.position == 1:
                if signal.confidence < self._min_confidence:
                    continue
                if exposure >= self._max_exposure:
                    continue
                exposure += 1
                cooldown_remaining = self._cooldown
            else:
                exposure = max(0, exposure - 1)
            filtered.append(signal)
        return filtered


class ExecutionAgent:
    """Converts filtered signals into concrete trade decisions."""

    def __init__(self, entry_note: str = "enter", flat_note: str = "flat") -> None:
        self._entry_note = entry_note
        self._flat_note = flat_note

    def execute(
        self, signals: Sequence[Signal], prices: PriceSeries
    ) -> List[TradeDecision]:
        decisions: List[TradeDecision] = []
        for signal in signals:
            price = prices[signal.index]
            note = self._entry_note if signal.position == 1 else self._flat_note
            decisions.append(
                TradeDecision(
                    index=signal.index,
                    position=signal.position,
                    price=price,
                    note=note,
                    confidence=signal.confidence,
                    rationale=signal.rationale,
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
