"""Deterministic metrics mirroring the TradingAgents prompt behaviour."""

from __future__ import annotations

from math import sqrt
from typing import Dict, Iterable, List, Sequence


def cumulative_return(returns: Sequence[float]) -> float:
    """Total absolute return from a list of period returns."""

    return float(sum(returns))


def equity_curve(returns: Sequence[float]) -> List[float]:
    """Running cumulative return curve for drawdown calculations."""

    total = 0.0
    curve: List[float] = []
    for value in returns:
        total += value
        curve.append(total)
    return curve


def max_drawdown(curve: Sequence[float]) -> float:
    """Maximum peak-to-trough drawdown for a cumulative curve."""

    peak = 0.0
    drawdown = 0.0
    for value in curve:
        peak = max(peak, value)
        drawdown = max(drawdown, peak - value)
    return drawdown


def win_rate(returns: Sequence[float]) -> float:
    """Share of positive returns."""

    wins = sum(1 for value in returns if value > 0)
    total = len(returns)
    if total == 0:
        return 0.0
    return wins / float(total)


def profit_factor(returns: Sequence[float]) -> float:
    """Ratio of gross gains to gross losses."""

    gross_gain = sum(value for value in returns if value > 0)
    gross_loss = -sum(value for value in returns if value < 0)
    if gross_loss == 0.0:
        return float("inf") if gross_gain > 0 else 0.0
    return gross_gain / gross_loss


def expectancy(returns: Sequence[float]) -> float:
    """Average return per trade."""

    if not returns:
        return 0.0
    return float(sum(returns) / len(returns))


def volatility(returns: Sequence[float]) -> float:
    """Sample standard deviation of returns."""

    n = len(returns)
    if n <= 1:
        return 0.0
    mean = sum(returns) / n
    variance = sum((value - mean) ** 2 for value in returns) / (n - 1)
    return sqrt(variance)


def compute_metrics(returns: Iterable[float]) -> Dict[str, float]:
    """Compute the deterministic metrics dictionary used across the pack."""

    realised = list(returns)
    curve = equity_curve(realised)
    metrics = {
        "cumulative_return": cumulative_return(realised),
        "win_rate": win_rate(realised),
        "max_drawdown": max_drawdown(curve) if curve else 0.0,
        "profit_factor": profit_factor(realised),
        "expectancy": expectancy(realised),
        "volatility": volatility(realised),
    }
    return metrics


__all__ = [
    "compute_metrics",
    "cumulative_return",
    "equity_curve",
    "expectancy",
    "max_drawdown",
    "profit_factor",
    "volatility",
    "win_rate",
]
