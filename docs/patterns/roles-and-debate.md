# Roles & Debate Protocol

The TradingAgents prompt pairs specialised roles inside a deterministic debate so
that every turn is auditable. Naestro mirrors that design with
:class:`~naestro.agents.DebateOrchestrator`, :class:`~naestro.agents.Roles`, and
serialisable transcripts. This guide explains how to configure a reusable debate
loop that fits outside of trading while keeping the same guard-rails.

## Debate timeline

1. **Prime** the transcript with a system message that anchors the scenario.
2. **Schedule** a deterministic sequence of roles. The orchestrator enforces the
   order and number of rounds.
3. **Emit** bus events for every turn so middleware can log, enrich, or veto the
   conversation (see [Message Bus Signals](../core/message-bus.md)).
4. **Resolve** the outcome and hand it to a downstream component, such as the
   [Governor Policy Board](../governance/governor.md) or a routing decision.

## Role catalogue

The TradingAgents setup ships with three reference roles:

| Role      | Purpose                                                 | Default strategy snippet |
|-----------|----------------------------------------------------------|---------------------------|
| `analyst` | Provides structured market commentary or hypotheses.     | Reviews the system prompt and surfaces opportunities. |
| `risk`    | Challenges proposals, applying deterministic rules.      | Counts approvals and vetoes unsafe leverage. |
| `operator`| Executes the decision or summarises next actions.        | Mirrors the final consensus back to the caller. |

You can register additional roles—such as `compliance` or `advisor`—as long as
their callables accept the transcript history and return a string.

## Minimal orchestration example

```python
from typing import Sequence

from naestro.agents import DebateOrchestrator, DebateSettings, Message, Role, Roles


def analyst(history: Sequence[Message]) -> str:
    prompt = history[0].content if history else ""
    return "Opportunity: momentum breakout" if "breakout" in prompt.lower() else "Hold"


def risk(history: Sequence[Message]) -> str:
    approvals = sum("opportunity" in message.content.lower() for message in history)
    return "Approve" if approvals else "Reject"


def operator(history: Sequence[Message]) -> str:
    return "Execute" if any("approve" in message.content.lower() for message in history) else "Wait"


roles = Roles()
roles.register(Role("analyst", "Evaluates signals", analyst))
roles.register(Role("risk", "Applies guard-rails", risk))
roles.register(Role("operator", "Commits to action", operator))

settings = DebateSettings(rounds=1)
orchestrator = DebateOrchestrator(roles)
transcript = orchestrator.run([
    "analyst",
    "risk",
    "operator",
], "System prompt: review the breakout setup", settings=settings)

for message in transcript.transcript.messages:
    print(message.role, "->", message.content)
```

## Observability hooks

Every debate publishes `debate.started`, `debate.prompt`, `debate.turn`, and
`debate.finished` events on the shared bus. Middleware can append diagnostics,
toggle feature flags, or emit structured logs. See
[Message Bus Signals](../core/message-bus.md) for the full catalog.

## Beyond trading

Swap the role strategies to fit procurement reviews, incident response drills,
or creative brainstorming. Because the orchestrator enforces order and rounds,
the resulting transcripts remain stable enough for snapshot-based testing.
