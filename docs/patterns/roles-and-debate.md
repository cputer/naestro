The Naestro runtime models collaborative reasoning as a **deterministic debate**
between specialised roles. Each role contributes a perspective and the
orchestrator guarantees a predictable turn order, which makes the behaviour safe
for regression testing.

## Building a role catalog

Roles are registered in a :class:`~naestro.agents.roles.Roles` collection with a
small strategy callable. The callable receives the full debate history including
an initial system prompt.

```python
from typing import Sequence

from naestro.agents import DebateOrchestrator, DebateSettings, Message, Role, Roles


def analyst(history: Sequence[Message]) -> str:
    prompt = history[0].content if history else ""
    return "Approve" if "breakout" in prompt.lower() else "Watch levels"


def risk(history: Sequence[Message]) -> str:
    approvals = sum("approve" in message.content.lower() for message in history)
    return "Approve" if approvals else "Reject"


roles = Roles()
roles.register(Role("analyst", "Detects market structure", analyst))
roles.register(Role("risk", "Ensures guard rails", risk))

orchestrator = DebateOrchestrator(roles)
outcome = orchestrator.run(
    ["analyst", "risk"],
    "System prompt: evaluate the breakout setup",
    settings=DebateSettings(rounds=1),
)
for message in outcome.transcript.messages:
    print(message.role, "->", message.content)
```

The orchestrator stores a :class:`~naestro.agents.DebateTranscript` that
can be serialised or analysed after the debate completes.

## Message bus signals

Every debate publishes `debate.started`, `debate.prompt`, `debate.turn` and
`debate.finished` events on the shared
:class:`~naestro.core.bus.MessageBus`. Middleware can inspect or augment these
payloads without modifying the orchestrator implementation.
