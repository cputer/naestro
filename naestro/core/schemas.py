"""Common data structures shared across the runtime."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Mapping, Sequence


@dataclass(slots=True)
class Message:
    """Represents an utterance in a debate."""

    role: str
    content: str
    timestamp: datetime
    metadata: Mapping[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class DebateTranscript:
    """Full conversation transcript."""

    prompt: str
    participants: Sequence[str]
    messages: List[Message] = field(default_factory=list)
    tags: Mapping[str, object] = field(default_factory=dict)

    def append(self, message: Message) -> None:
        self.messages.append(message)

    def last_speaker(self) -> str | None:
        if not self.messages:
            return None
        return self.messages[-1].role

    def summary(self) -> str:
        fragments = ", ".join(f"{m.role}:{m.content}" for m in self.messages[-3:])
        return f"Debate[{', '.join(self.participants)}]: {fragments}"

    def to_dict(self) -> dict[str, object]:
        return {
            "prompt": self.prompt,
            "participants": list(self.participants),
            "messages": [message.to_dict() for message in self.messages],
            "tags": dict(self.tags),
        }


def new_message(
    role: str, content: str, *, metadata: Mapping[str, object] | None = None
) -> Message:
    """Create a message with a deterministic timestamp."""

    meta: Mapping[str, object] = metadata if metadata is not None else {}
    timestamp = datetime(2024, 1, 1, tzinfo=timezone.utc)
    return Message(role=role, content=content, timestamp=timestamp, metadata=meta)
