from __future__ import annotations

from pathlib import Path
import sys

import pytest

try:
    from packs.trading import run_backtest
    from packs.trading.agents import TradeDecision
except Exception:
    sys.path.append(str(Path(__file__).resolve().parents[3]))
    from packs.trading import run_backtest
    from packs.trading.agents import TradeDecision


def test_backtest_runs_and_computes_metrics() -> None:
    prices = [100.0, 101.0, 100.0, 103.0]
    trades = [
        TradeDecision(index=0, position=1, price=100.0, note="enter"),
        TradeDecision(index=1, position=1, price=101.0, note="hold"),
        TradeDecision(index=2, position=1, price=100.0, note="reenter"),
    ]
    result = run_backtest(prices, trades)

    assert [round(value, 6) for value in result.returns] == [1.0, -1.0, 3.0]
    assert result.equity_curve == [1.0, 0.0, 3.0]
    assert result.metrics["cumulative_return"] == pytest.approx(3.0)
    assert result.metrics["win_rate"] == pytest.approx(2 / 3)
    assert result.metrics["max_drawdown"] == pytest.approx(1.0)
    assert result.metrics["profit_factor"] == pytest.approx(4.0)
