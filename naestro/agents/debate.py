"""Deterministic debate orchestrator using builtin roles."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Iterable, Mapping, MutableMapping, Sequence

from pydantic import BaseModel, ConfigDict, Field

from naestro.core.bus import MessageBus
from naestro.core.tracing import Tracer

from .roles import Role, Roles
from .schemas import DebateTranscript, Message


class DebateSettings(BaseModel):
    """Configuration parameters for a deterministic debate."""

    rounds: int = 1
    initial_offset: int = 0
    tags: MutableMapping[str, object] = Field(default_factory=dict)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class DebateOutcome(BaseModel):
    """Result returned after running a debate session."""

    transcript: DebateTranscript
    approved: bool = True
    rationale: str = ""

    model_config = ConfigDict(arbitrary_types_allowed=True)


class DebateOrchestrator:
    """Coordinates deterministic debates between registered roles."""

    def __init__(
        self,
        roles: Mapping[str, Role] | Iterable[Role] | None = None,
        *,
        bus: MessageBus | None = None,
        tracer: Tracer | None = None,
    ) -> None:
        if roles is None:
            catalog = Roles()
            self._roles: dict[str, Role] = {role.name: role for role in catalog.list()}
        elif isinstance(roles, Mapping):
            self._roles = dict(roles)
        else:
            self._roles = {role.name: role for role in roles}
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
        transcript = DebateTranscript(
            prompt=prompt,
            participants=list(participants),
            tags=dict(config.tags),
        )
        base_time = datetime(2024, 1, 1, tzinfo=timezone.utc)
        current_time = base_time + timedelta(seconds=config.initial_offset)

        start_payload = {"participants": list(participants), "prompt": prompt}
        self._publish("debate.started", start_payload)

        system_message = Message(
            role="system",
            content=prompt,
            timestamp=current_time,
            metadata={"round": -1, "order": -1},
        )
        transcript.append(system_message)
        prompt_payload = {"message": system_message.to_dict()}
        self._publish("debate.prompt", prompt_payload)
        current_time += timedelta(seconds=1)

        for round_index in range(config.rounds):
            for order, name in enumerate(participants):
                role = self._resolve_role(name)
                content = role.respond(tuple(transcript.messages))
                message = Message(
                    role=name,
                    content=content,
                    timestamp=current_time,
                    metadata={"round": round_index, "order": order},
                )
                transcript.append(message)
                payload = {"message": message.to_dict(), "round": round_index}
                self._publish("debate.turn", payload)
                current_time += timedelta(seconds=1)

        summary = transcript.summary()
        result_payload = {"summary": summary, "turns": len(transcript.messages)}
        self._publish("debate.finished", result_payload)
        return DebateOutcome(transcript=transcript, approved=True, rationale=summary)

    def _resolve_role(self, name: str) -> Role:
        try:
            return self._roles[name]
        except KeyError as exc:  # pragma: no cover - helpful error message
            raise KeyError(f"Unknown role '{name}'") from exc

    def _publish(self, topic: str, payload: Mapping[str, object]) -> None:
        self._bus.publish(topic, payload)
        if self._tracer is not None:
            self._tracer.log_event(topic, payload)


__all__ = ["DebateOrchestrator", "DebateOutcome", "DebateSettings"]
