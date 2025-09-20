from __future__ import annotations

import pytest

from packs.trading import run_backtest
from packs.trading.agents import TradeDecision


def test_backtest_runs() -> None:
    prices = [100.0, 101.0, 102.0, 101.0]
    trades = [
        TradeDecision(index=0, position=1, price=100.0, note="enter"),
        TradeDecision(index=1, position=0, price=101.0, note="flat"),
        TradeDecision(index=2, position=1, price=102.0, note="enter"),
    ]
    result = run_backtest(prices, trades)
    assert result.metrics["cumulative_return"] == pytest.approx(0.0)
    assert result.metrics["win_rate"] == pytest.approx(1 / 3)
    assert result.metrics["max_drawdown"] == pytest.approx(1.0)
