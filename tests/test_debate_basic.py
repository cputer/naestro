from __future__ import annotations

import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

import pytest

pytest.importorskip("jsonschema")

from naestro.agents.debate import DebateOrchestrator, DebateOutcome, DebateSettings
from naestro.agents.roles import Role, Roles
from naestro.agents.schemas import Message
from naestro.core.bus import MessageBus


def test_orchestrator_runs_rounds_and_emits_events() -> None:
    def analyst(history: Sequence[Message]) -> str:
        return f"analysis-{len(history)}"

    def critic(history: Sequence[Message]) -> str:
        if history and history[-1].role == "analyst":
            return "approve"
        return "continue"

    roles = Roles()
    roles.register(Role("analyst", "Provides initial view", analyst))
    roles.register(Role("critic", "Challenges proposals", critic))

    bus = MessageBus()
    rounds: list[int] = []
    bus.subscribe("debate.turn", lambda payload: rounds.append(int(payload["round"])))

    orchestrator = DebateOrchestrator(roles, bus=bus)
    settings = DebateSettings(rounds=2, initial_offset=5, tags={"scenario": "trade"})
    outcome = orchestrator.run(
        ["analyst", "critic"],
        "Evaluate the setup",
        settings=settings,
    )

    assert isinstance(outcome, DebateOutcome)
    transcript = outcome.transcript
    assert transcript.tags == {"scenario": "trade"}

    message_rounds = [
        message.metadata["round"] for message in transcript.messages[1:]
    ]
    assert message_rounds == [0, 0, 1, 1]

    first_message = transcript.messages[0]
    assert first_message.metadata == {"round": -1, "order": -1}
    assert first_message.timestamp.isoformat() == "2024-01-01T00:00:05+00:00"

    assert transcript.messages[-1].content == "approve"
    assert outcome.approved is True

    expected_rationale = (
        "Debate[analyst, critic]: critic:approve, analyst:analysis-3, critic:approve"
    )
    assert outcome.rationale == expected_rationale

    events = [envelope.event for envelope in bus.envelopes]
    assert events == [
        "debate.started",
        "debate.prompt",
        "debate.turn",
        "debate.turn",
        "debate.turn",
        "debate.turn",
        "debate.finished",
    ]

    started_payload = bus.envelopes[0].payload
    assert started_payload["participants"] == ["analyst", "critic"]
    assert started_payload["prompt"] == "Evaluate the setup"
    finished_payload = bus.envelopes[-1].payload
    assert finished_payload["turns"] == len(transcript.messages)
    assert rounds == [0, 0, 1, 1]

    known_events = set(bus.known_events)
    expected_events = {
        "debate.started",
        "debate.turn",
        "debate.prompt",
        "debate.finished",
    }
    assert expected_events <= known_events
