"""Trading pack primitives aligned with the TradingAgents prompt."""

from __future__ import annotations

from .agents import ExecutionAgent, RiskAgent, SignalAgent, TradeDecision
from .backtest import BacktestResult, run_backtest
from .pipelines import DebateGate, PipelineResult, TradingPipeline, trading_demo

__all__ = [
    "BacktestResult",
    "DebateGate",
    "ExecutionAgent",
    "PipelineResult",
    "RiskAgent",
    "SignalAgent",
    "TradeDecision",
    "TradingPipeline",
    "run_backtest",
    "trading_demo",
]
