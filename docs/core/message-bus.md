# Message Bus Signals

The message bus glues Naestro components together. Inspired by the
TradingAgents prompt, each bus event maps to a stage of the deterministic
workflow so observers can replay, audit, or augment behaviour without mutating
the orchestrators themselves.

## Event catalogue

| Event name          | Emitted by                     | Payload focus                                  |
|---------------------|---------------------------------|------------------------------------------------|
| `debate.started`    | Debate orchestrator             | Debate identifier, scheduled roles, settings.  |
| `debate.turn`       | Debate orchestrator             | Role, message content, round number.           |
| `debate.finished`   | Debate orchestrator             | Transcript metadata and summary.               |
| `policy.check`      | [Governor](../governance/governor.md)        | Policy name, decision, supporting evidence.   |
| `routing.evaluated` | [Model router](../routing/model-routing.md) | Profile ID, scored models, ranking metadata.  |
| `trade.executed`    | [Trading pack](../packs/trading.md)         | Execution result, position sizing, telemetry. |

The payloads are simple dictionaries that can be serialised for storage or
transport. Downstream consumers can register middleware to intercept events and
push them to metrics, logs, or real-time dashboards.

## Subscribing middleware

```python
from naestro.core.bus import MessageBus

bus = MessageBus()


def audit(event: str, payload: dict) -> None:
    print("AUDIT", event, payload)


bus.subscribe(audit)

bus.publish("debate.started", {"id": "demo", "roles": ["analyst", "risk"]})
bus.publish("policy.check", {"policy": "min_return", "passed": True})
```

Middleware is invoked synchronously, keeping execution deterministic and easy to
test. If you need asynchronous fan-out, wrap the publish call with your own
queueing infrastructure while keeping the payload format the same.

## Design tips

- **Keep payloads explicit.** Avoid passing raw objects; favour serialisable
  dictionaries so logs remain human-readable.
- **Annotate contexts.** Include run identifiers, user IDs, or timestamps if
  your environment requires traceability.
- **Reuse the catalog.** When extending to a new domain, try to map events back
  to the same canonical names. This keeps dashboards and tests reusable across
  scenarios.
- **Leverage replays.** Persist the stream and replay it to reconstruct the state
  of a debate, policy gate, or trading pipeline for audits.

## Relationship to other guides

The debate protocol emits the first half of the catalog, the governor publishes
policy checks, and the routing layer contributes evaluation events. The trading
pack demonstrates how to consume all of them inside a single deterministic
workflow.
