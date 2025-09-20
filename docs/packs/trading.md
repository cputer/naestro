# Trading Pack

The trading pack bundles a signal generator, risk filter, execution agent and
optional debate gate. It demonstrates how Naestro's orchestration primitives can
coordinate deterministic decisions.

```python
from typing import Sequence

from naestro.agents import Role, RoleRegistry
from naestro.core.debate import DebateOrchestrator
from naestro.core.schemas import Message
from packs.trading import DebateGate, ExecutionAgent, RiskAgent, SignalAgent, TradingPipeline


def analyst(history: Sequence[Message]) -> str:
    return "Approve" if len(history) else "Approve with caution"


def risk(history: Sequence[Message]) -> str:
    return "Reject" if "100.50" in history[0].content else "Approve"


registry = RoleRegistry([
    Role("analyst", "Evaluates momentum", analyst),
    Role("risk", "Manages risk", risk),
])

pipeline = TradingPipeline(
    SignalAgent(window=2),
    RiskAgent(max_exposure=1, min_confidence=0.1),
    ExecutionAgent(),
    debate_gate=DebateGate(DebateOrchestrator(registry), ["analyst", "risk"]),
)

prices = [100.0, 100.2, 100.5, 100.4]
result = pipeline.run(prices)
print(result.trades)
print(result.rejected_trades)
```

The pipeline returns a :class:`~packs.trading.pipeline.PipelineResult` containing
approved trades, rejected trades and backtest metrics that can be fed into the
:mod:`naestro.governance` layer.
