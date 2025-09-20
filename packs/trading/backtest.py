"""Deterministic backtesting utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence

from .agents import PriceSeries, TradeDecision
from .metrics import cumulative_return, equity_curve, max_drawdown, win_rate


@dataclass(slots=True)
class BacktestResult:
    trades: List[TradeDecision]
    returns: List[float]
    equity_curve: List[float]
    metrics: Dict[str, float]


def run_backtest(
    prices: PriceSeries, trades: Sequence[TradeDecision]
) -> BacktestResult:
    realised_returns: List[float] = []
    for trade in trades:
        if trade.index >= len(prices) - 1:
            continue
        next_price = prices[trade.index + 1]
        current_price = prices[trade.index]
        realised_returns.append((next_price - current_price) * float(trade.position))
    curve = equity_curve(realised_returns)
    metrics = {
        "cumulative_return": cumulative_return(realised_returns),
        "win_rate": win_rate(realised_returns),
        "max_drawdown": max_drawdown(curve) if curve else 0.0,
    }
    return BacktestResult(
        trades=list(trades),
        returns=realised_returns,
        equity_curve=curve,
        metrics=metrics,
    )


__all__ = ["BacktestResult", "run_backtest"]
