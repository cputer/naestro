"""Trading pack built on the Naestro runtime."""

from __future__ import annotations

from .agents import ExecutionAgent, RiskAgent, SignalAgent
from .backtest import BacktestResult, run_backtest
from .pipeline import DebateGate, TradingPipeline

__all__ = [
    "BacktestResult",
    "DebateGate",
    "ExecutionAgent",
    "RiskAgent",
    "SignalAgent",
    "TradingPipeline",
    "run_backtest",
]
