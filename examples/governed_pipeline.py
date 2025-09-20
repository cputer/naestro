"""Execute the trading pipeline with both debate gating and governance."""

from pathlib import Path
import sys
from typing import cast, Sequence

import yaml

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from naestro import (
    DebateOrchestrator,
    Decision,
    Governor,
    Message,
    Policy,
    PolicyInput,
    Role,
    Roles,
)

from packs.trading import (
    DebateGate,
    ExecutionAgent,
    RiskAgent,
    SignalAgent,
    TradingPipeline,
)

CONFIG_ROOT = Path(__file__).resolve().parents[1] / "configs"
TRADING_CONFIG = CONFIG_ROOT / "trading_demo.yaml"
POLICY_CONFIG = CONFIG_ROOT / "policies_basic.yaml"


def _load_trading_config() -> dict[str, object]:
    return yaml.safe_load(TRADING_CONFIG.read_text()) or {}


def _load_policy_thresholds() -> tuple[float, float]:
    data = yaml.safe_load(POLICY_CONFIG.read_text()) or {}
    policies = data.get("policies", {})
    max_drawdown = float(policies.get("max_drawdown", 0.0))
    min_return = float(policies.get("min_return", 0.0))
    return max_drawdown, min_return


def build_gate() -> DebateGate:
    """Configure a deterministic gate with analyst and risk roles."""

    def analyst(history: Sequence[Message]) -> str:
        confidence = len(history) + 1
        return (
            f"Approve with confidence {confidence}"
            if confidence > 1
            else "Approve trade"
        )

    def risk(history: Sequence[Message]) -> str:
        if any("drawdown" in message.content.lower() for message in history):
            return "Reject trade"
        return "Approve trade"

    roles = Roles()
    roles.register(Role("analyst", "Quant analyst", analyst))
    roles.register(Role("risk", "Risk supervisor", risk))
    orchestrator = DebateOrchestrator(roles)
    return DebateGate(orchestrator, ["analyst", "risk"])


def build_governor() -> Governor:
    """Create a governor enforcing drawdown and return policies."""

    max_drawdown_limit, min_return_threshold = _load_policy_thresholds()
    governor = Governor()

    def max_drawdown(payload: PolicyInput) -> Decision:
        raw_drawdown = payload.metadata.get("max_drawdown", 0.0)
        drawdown = float(cast(float, raw_drawdown))
        passed = drawdown <= max_drawdown_limit
        reason = (
            "Within drawdown limit"
            if passed
            else f"Drawdown {drawdown:.2f} exceeds limit {max_drawdown_limit:.2f}"
        )
        return Decision(name="max_drawdown", passed=passed, reason=reason)

    def min_return(payload: PolicyInput) -> Decision:
        score = payload.score or 0.0
        passed = score >= min_return_threshold
        reason = (
            "Return target met"
            if passed
            else f"Return {score:.2f} below target {min_return_threshold:.2f}"
        )
        return Decision(name="min_return", passed=passed, reason=reason)

    governor.register(Policy("max_drawdown", "Limit drawdowns", max_drawdown))
    governor.register(Policy("min_return", "Ensure positive returns", min_return))
    return governor


def main() -> None:
    prices = [100.0, 101.0, 102.5, 101.5, 103.0, 104.5]
    trading_config = _load_trading_config()
    window = int(trading_config.get("signal_window", 2))
    max_exposure = int(trading_config.get("max_exposure", 1))
    min_confidence = float(trading_config.get("min_confidence", 0.1))
    pipeline = TradingPipeline(
        SignalAgent(window=window),
        RiskAgent(max_exposure=max_exposure, min_confidence=min_confidence),
        ExecutionAgent(),
        debate_gate=build_gate(),
        governor=build_governor(),
    )
    result = pipeline.run(prices)
    print("Approved trades:")
    for trade in result.trades:
        print(f"  index={trade.index} price={trade.price:.2f} note={trade.note}")
    print("Rejected trades:")
    for trade in result.rejected_trades:
        print(f"  index={trade.index} price={trade.price:.2f} note={trade.note}")
    print("Metrics:", result.backtest.metrics)
    print("Governance:")
    for policy_result in result.governance_results:
        status = "PASS" if policy_result.passed else "FAIL"
        print(f"  {policy_result.name}: {status} - {policy_result.reason}")
    print("Pipeline approved:", result.approved)


if __name__ == "__main__":
    main()
