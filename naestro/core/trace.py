"""Helpers for exporting recorded envelopes to trace artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from json import dumps, loads
from pathlib import Path
from typing import Iterable, Mapping, Sequence, TYPE_CHECKING

from .bus import Envelope

if TYPE_CHECKING:  # pragma: no cover - imported for type checking only
    from naestro.agents.schemas import DebateTranscript
    from naestro.governance.schemas import Decision

    from .tracing import Tracer


@dataclass(frozen=True, slots=True)
class TraceEvent:
    """Serializable representation of an :class:`Envelope`."""

    sequence: int
    event: str
    timestamp: str
    payload: Mapping[str, object]
    redactions: Sequence[str]

    @classmethod
    def from_envelope(cls, envelope: Envelope) -> "TraceEvent":
        return cls(
            sequence=envelope.sequence,
            event=envelope.event,
            timestamp=envelope.timestamp.isoformat(),
            payload=dict(envelope.payload),
            redactions=list(envelope.redactions),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "sequence": self.sequence,
            "event": self.event,
            "timestamp": self.timestamp,
            "payload": loads(dumps(self.payload, default=str)),
            "redactions": list(self.redactions),
        }


def build_trace(envelopes: Sequence[Envelope] | Iterable[Envelope]) -> list[TraceEvent]:
    """Create :class:`TraceEvent` objects from recorded envelopes."""

    if not isinstance(envelopes, Sequence):
        envelopes = tuple(envelopes)
    return [TraceEvent.from_envelope(envelope) for envelope in envelopes]


def write_trace(
    envelopes: Sequence[Envelope] | Iterable[Envelope],
    target: Path,
) -> Path:
    """Write envelopes to *target* as JSON trace data."""

    events = [event.to_dict() for event in build_trace(envelopes)]
    target.write_text(dumps(events, indent=2), encoding="utf-8")
    return target
def start_trace(
    *, root: Path | str | None = None, run_name: str | None = None
) -> "Tracer":
    """Create a :class:`~naestro.core.tracing.Tracer` for manual management."""

    from .tracing import Tracer

    return Tracer(root=root, run_name=run_name)


def write_debate_transcript(transcript: "DebateTranscript", target: Path) -> Path:
    """Serialise a :class:`~naestro.agents.schemas.DebateTranscript` to JSON."""

    payload = transcript.to_dict()
    payload["summary"] = transcript.summary()
    target.write_text(dumps(payload, indent=2), encoding="utf-8")
    return target


def write_governor(decisions: Sequence["Decision"], target: Path) -> Path:
    """Write governor decisions to disk as JSON data."""

    payload = {
        "approved": all(decision.passed for decision in decisions),
        "decisions": [decision.model_dump() for decision in decisions],
    }
    target.write_text(dumps(payload, indent=2), encoding="utf-8")
    return target


__all__ = [
    "TraceEvent",
    "build_trace",
    "start_trace",
    "write_debate_transcript",
    "write_governor",
    "write_trace",
]
