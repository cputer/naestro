"""Helpers for exporting recorded envelopes to trace artifacts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from .bus import Envelope


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
            "payload": json.loads(json.dumps(self.payload, default=str)),
            "redactions": list(self.redactions),
        }


def build_trace(envelopes: Sequence[Envelope] | Iterable[Envelope]) -> list[TraceEvent]:
    """Create :class:`TraceEvent` objects from recorded envelopes."""

    if not isinstance(envelopes, Sequence):
        envelopes = tuple(envelopes)
    return [TraceEvent.from_envelope(envelope) for envelope in envelopes]


def write_trace(envelopes: Sequence[Envelope] | Iterable[Envelope], target: Path) -> Path:
    """Write envelopes to *target* as JSON trace data."""

    events = [event.to_dict() for event in build_trace(envelopes)]
    target.write_text(json.dumps(events, indent=2), encoding="utf-8")
    return target


__all__ = ["TraceEvent", "build_trace", "write_trace"]
