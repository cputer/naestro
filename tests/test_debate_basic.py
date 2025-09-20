from __future__ import annotations

from typing import List, Sequence

from naestro.agents import DebateOrchestrator, DebateSettings, Message, Role, Roles
from naestro.core.bus import MessageBus


def test_orchestrator_runs_rounds() -> None:
    def analyst(history: Sequence[Message]) -> str:
        return f"analysis {len(history)}"

    def critic(history: Sequence[Message]) -> str:
        return "approve" if len(history) > 0 else "needs more"

    roles = Roles()
    roles.register(Role("analyst", "Provides initial view", analyst))
    roles.register(Role("critic", "Challenges proposals", critic))
    bus = MessageBus()
    rounds: List[int] = []

    def record(payload: object) -> None:
        mapping = payload if isinstance(payload, dict) else {}
        rounds.append(int(mapping["round"]))

    bus.subscribe("debate.turn", record)
    orchestrator = DebateOrchestrator(roles, bus=bus)
    outcome = orchestrator.run(
        ["analyst", "critic"],
        "Is the trade compelling?",
        settings=DebateSettings(rounds=2),
    )
    assert len(outcome.transcript.messages) == 5
    assert outcome.transcript.messages[0].role == "system"
    assert rounds == [0, 0, 1, 1]
    assert outcome.transcript.messages[-1].content == "approve"
