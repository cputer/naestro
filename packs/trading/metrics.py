"""Performance metrics used by the trading pack."""

from __future__ import annotations

from typing import List, Sequence


def cumulative_return(returns: Sequence[float]) -> float:
    return float(sum(returns))


def equity_curve(returns: Sequence[float]) -> List[float]:
    total = 0.0
    curve: List[float] = []
    for value in returns:
        total += value
        curve.append(total)
    return curve


def max_drawdown(curve: Sequence[float]) -> float:
    peak = 0.0
    drawdown = 0.0
    for value in curve:
        peak = max(peak, value)
        drawdown = max(drawdown, peak - value)
    return drawdown


def win_rate(returns: Sequence[float]) -> float:
    wins = sum(1 for value in returns if value > 0)
    total = len(returns)
    if total == 0:
        return 0.0
    return wins / float(total)


__all__ = ["cumulative_return", "equity_curve", "max_drawdown", "win_rate"]
