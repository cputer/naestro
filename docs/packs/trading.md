# Trading Pack Walkthrough

The trading pack translates the TradingAgents prompt into a deterministic Python
module. It bundles signal generation, risk review, execution, and optional debate
gates into a single pipeline that you can reuse or swap for other business
flows.

## Components

- **Signal agent** – Computes trend indicators or domain-specific features.
- **Risk agent** – Applies deterministic heuristics and raises structured vetoes.
- **Execution agent** – Produces final actions, orders, or recommendations.
- **Debate gate** – (Optional) Wraps the agents in the
  [Roles & Debate Protocol](../patterns/roles-and-debate.md) for auditable
  discussion.

## Running the pipeline

```python
from packs.trading import DebateGate, ExecutionAgent, RiskAgent, SignalAgent, TradingPipeline
from naestro.agents import DebateOrchestrator, Role, Roles

roles = Roles()
roles.register(Role("analyst", "Evaluates signals", lambda history: "Approve"))
roles.register(Role("risk", "Applies guard-rails", lambda history: "Approve"))

debate_gate = DebateGate(DebateOrchestrator(roles), ["analyst", "risk"])

pipeline = TradingPipeline(
    signal=SignalAgent(window=3),
    risk=RiskAgent(max_exposure=1, min_confidence=0.2),
    execution=ExecutionAgent(),
    debate_gate=debate_gate,
)

series = [100.0, 100.4, 100.9, 101.2, 100.8]
result = pipeline.run(series)

print(result.trades)
print(result.rejected_trades)
print(result.metrics)
```

The `TradingPipeline` returns approved trades, rejected trades, and a metrics
object that can be forwarded to the
[Governor Policy Board](../governance/governor.md) or persisted for analytics.

## Event integrations

The pack publishes the following events on the
[Message Bus](../core/message-bus.md):

- `signal.generated` – Includes raw indicators.
- `risk.evaluated` – Contains risk scores and veto reasons.
- `trade.executed` – Summarises fills and post-trade metrics.

Subscribe middleware to these events to power dashboards or offline analysis.

## Adapting the pack

- **Swap agents.** Replace the provided callables with domain-specific logic,
  such as lead scoring, content moderation, or support triage.
- **Tune parameters.** Adjust window sizes, thresholds, and scoring weights to
  match your data distributions.
- **Extend metrics.** Add deterministic metrics by inheriting from the bundled
  classes in `packs.trading.metrics`.

## Next steps

Use the pack as the integration point for routing and governance. Feed in
profiles from the [Model Routing Matrix](../routing/model-routing.md) and gate
the outcomes with the governor to reproduce the TradingAgents audit trail in any
other domain.
