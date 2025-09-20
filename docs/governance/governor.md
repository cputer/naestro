# Governor Policy Board

TradingAgents-inspired pipelines rely on a council of deterministic policies to
approve or reject proposals. The Naestro governor recreates that policy board.
Policies are pure callables that receive structured input, return a decision,
and broadcast their findings on the message bus.

## Policy structure

```python
from naestro.governance import Decision, Governor, Policy, PolicyInput

governor = Governor()


def min_confidence(payload: PolicyInput) -> Decision:
    score = payload.score or 0.0
    passed = score >= 0.35
    return Decision(
        name="min_confidence",
        passed=passed,
        reason="meets risk tolerance" if passed else "confidence too low",
    )


def max_drawdown(payload: PolicyInput) -> Decision:
    drawdown = float(payload.metadata.get("max_drawdown", 0.0))
    passed = drawdown <= 2.0
    return Decision(
        name="max_drawdown",
        passed=passed,
        reason="protected" if passed else "drawdown exceeded limit",
    )


governor.register(Policy("confidence", "Require a minimum confidence score", min_confidence))
governor.register(Policy("drawdown", "Limit downside exposure", max_drawdown))

payload = PolicyInput(
    subject="demo-trade",
    score=0.42,
    metadata={"max_drawdown": 1.5},
)
allowed, decisions = governor.enforce(payload)
```

The `governor.enforce` call returns a boolean plus a list of decisions, making it
trivial to expose the results via APIs, dashboards, or audit logs.

## Mapping policies to events

Each enforcement triggers a `policy.check` message on the
[Message Bus](../core/message-bus.md). Middleware can promote the decisions to
storage, trigger alerts, or append them to the transcript maintained by the
[Roles & Debate Protocol](../patterns/roles-and-debate.md).

## Designing effective boards

- **Keep policies pure.** Deterministic inputs and outputs guarantee reproducible
  behaviour.
- **Make reasoning explicit.** Populate the `reason` field with actionable
  details so operators can remediate failed checks.
- **Bundle metadata.** Use the `PolicyInput.metadata` dictionary to supply
  additional context like volatility, compliance flags, or user tiers.
- **Chain outcomes.** Feed the `allowed` flag into subsequent steps such as the
  [Trading Pack Walkthrough](../packs/trading.md) to veto execution.

## Adapting beyond trading

Swap the example policies for domain-specific rules—procurement budgets,
security sign-offs, or editorial guidelines. The deterministic design keeps
regression tests simple and gives auditors a concise, replayable trail.
