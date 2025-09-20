"""Implementation of a deterministic debate orchestrator."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Sequence, TYPE_CHECKING

from naestro.core.bus import MessageBus
from naestro.core.schemas import DebateTranscript, Message
from naestro.core.tracing import Tracer

if TYPE_CHECKING:  # pragma: no cover - typing only
    from naestro.agents.registry import RoleRegistry


@dataclass(slots=True)
class DebateSettings:
    rounds: int = 1
    initial_offset: int = 0


@dataclass(slots=True)
class DebateOutcome:
    transcript: DebateTranscript
    approved: bool
    rationale: str


class DebateOrchestrator:
    """Coordinates a debate between registered roles."""

    def __init__(
        self,
        registry: "RoleRegistry",
        *,
        bus: MessageBus | None = None,
        tracer: Tracer | None = None,
    ) -> None:
        self._registry = registry
        self._bus = bus or MessageBus()
        self._tracer = tracer

    def run(
        self,
        participants: Sequence[str],
        prompt: str,
        *,
        settings: DebateSettings | None = None,
    ) -> DebateOutcome:
        config = settings or DebateSettings()
        transcript = DebateTranscript(prompt=prompt, participants=list(participants))
        base_time = datetime(2024, 1, 1, tzinfo=timezone.utc)
        current_time = base_time + timedelta(seconds=config.initial_offset)
        self._bus.publish(
            "debate.started", {"participants": list(participants), "prompt": prompt}
        )
        if self._tracer is not None:
            self._tracer.log_event(
                "debate.started",
                {"participants": list(participants), "prompt": prompt},
            )

        system_message = Message(
            role="system",
            content=prompt,
            timestamp=current_time,
            metadata={"round": -1, "order": -1},
        )
        transcript.append(system_message)
        prompt_payload = {"message": system_message.to_dict()}
        self._bus.publish("debate.prompt", prompt_payload)
        if self._tracer is not None:
            self._tracer.log_event("debate.prompt", prompt_payload)
        current_time += timedelta(seconds=1)

        for round_index in range(config.rounds):
            for position, name in enumerate(participants):
                role = self._registry.get(name)
                message = Message(
                    role=name,
                    content=role.respond(transcript.messages),
                    timestamp=current_time,
                    metadata={"round": round_index, "order": position},
                )
                transcript.append(message)
                payload = {"message": message.to_dict(), "round": round_index}
                self._bus.publish("debate.turn", payload)
                if self._tracer is not None:
                    self._tracer.log_event("debate.turn", payload)
                current_time += timedelta(seconds=1)

        summary = transcript.summary()
        result_payload = {"summary": summary, "turns": len(transcript.messages)}
        self._bus.publish("debate.finished", result_payload)
        if self._tracer is not None:
            self._tracer.log_event("debate.finished", result_payload)
        return DebateOutcome(transcript=transcript, approved=True, rationale=summary)


__all__ = ["DebateOrchestrator", "DebateOutcome", "DebateSettings"]
