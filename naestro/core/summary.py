"""Utilities for summarising recorded bus envelopes."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from .bus import Envelope


@dataclass(frozen=True, slots=True)
class BusSummary:
    """Aggregated view over a sequence of :class:`Envelope` objects."""

    total_events: int
    event_counts: Mapping[str, int]
    redaction_counts: Mapping[str, int]

    def to_dict(self) -> dict[str, object]:
        return {
            "total_events": self.total_events,
            "event_counts": dict(self.event_counts),
            "redaction_counts": dict(self.redaction_counts),
        }

    def format(self) -> str:
        parts: list[str] = [f"total={self.total_events}"]
        if self.event_counts:
            event_parts = ", ".join(
                f"{name}:{count}"
                for name, count in sorted(self.event_counts.items())
            )
            parts.append(f"events=({event_parts})")
        if self.redaction_counts:
            redaction_parts = ", ".join(
                f"{path}:{count}"
                for path, count in sorted(self.redaction_counts.items())
            )
            parts.append(f"redactions=({redaction_parts})")
        return " | ".join(parts)


def summarize(envelopes: Sequence[Envelope] | Iterable[Envelope]) -> BusSummary:
    """Produce a :class:`BusSummary` from previously recorded envelopes."""

    if not isinstance(envelopes, Sequence):
        envelopes = tuple(envelopes)
    event_counts: Counter[str] = Counter()
    redaction_counts: Counter[str] = Counter()
    for envelope in envelopes:
        event_counts[envelope.event] += 1
        redaction_counts.update(envelope.redactions)
    return BusSummary(
        total_events=len(envelopes),
        event_counts=dict(event_counts),
        redaction_counts=dict(redaction_counts),
    )


__all__ = ["BusSummary", "summarize"]
