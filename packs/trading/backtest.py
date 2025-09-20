"""Backtesting utilities aligned with the TradingAgents prompt."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence

from .agents import PriceSeries, TradeDecision
from .metrics import compute_metrics, equity_curve


@dataclass(slots=True)
class BacktestResult:
    """Structured output returned by ``run_backtest``."""

    trades: List[TradeDecision]
    returns: List[float]
    equity_curve: List[float]
    metrics: Dict[str, float]


def _realised_returns(
    prices: PriceSeries,
    trades: Iterable[TradeDecision],
) -> List[float]:
    realised: List[float] = []
    price_count = len(prices)
    for trade in trades:
        if trade.index >= price_count - 1:
            continue
        entry = prices[trade.index]
        exit_price = prices[trade.index + 1]
        realised.append((exit_price - entry) * float(trade.position))
    return realised


def run_backtest(
    prices: PriceSeries,
    trades: Sequence[TradeDecision],
) -> BacktestResult:
    """Replay trades against prices and compute deterministic metrics."""

    realised_returns = _realised_returns(prices, trades)
    curve = equity_curve(realised_returns)
    metrics = compute_metrics(realised_returns)
    if curve:
        metrics.setdefault("max_drawdown", metrics["max_drawdown"])
    return BacktestResult(
        trades=list(trades),
        returns=realised_returns,
        equity_curve=curve,
        metrics=metrics,
    )


__all__ = ["BacktestResult", "run_backtest"]
