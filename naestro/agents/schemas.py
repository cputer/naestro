"""Pydantic models used by the deterministic debate orchestrator."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Sequence

from pydantic import BaseModel, ConfigDict, Field


def _default_timestamp() -> datetime:
    """Return the canonical timestamp used for deterministic debates."""

    return datetime(2024, 1, 1, tzinfo=timezone.utc)


class Message(BaseModel):
    """Represents a single utterance in a debate transcript."""

    role: str
    content: str
    timestamp: datetime = Field(default_factory=_default_timestamp)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True)

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the message into a JSON-friendly mapping."""

        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": dict(self.metadata),
        }


class DebateTranscript(BaseModel):
    """Full transcript of a deterministic debate session."""

    prompt: str
    participants: List[str]
    messages: List[Message] = Field(default_factory=list)
    tags: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def append(self, message: Message) -> None:
        """Append a message to the transcript."""

        self.messages.append(message)

    def extend(self, messages: Sequence[Message]) -> None:
        """Append multiple messages to the transcript."""

        self.messages.extend(messages)

    def last_speaker(self) -> str | None:
        """Return the role that produced the most recent message."""

        if not self.messages:
            return None
        return self.messages[-1].role

    def summary(self) -> str:
        """Build a concise textual summary of the debate."""

        if not self.messages:
            return f"Debate[{', '.join(self.participants)}]: <empty>"
        tail = self.messages[-3:]
        fragments = ", ".join(f"{message.role}:{message.content}" for message in tail)
        return f"Debate[{', '.join(self.participants)}]: {fragments}"

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the transcript for storage or analytics."""

        return {
            "prompt": self.prompt,
            "participants": list(self.participants),
            "messages": [message.to_dict() for message in self.messages],
            "tags": dict(self.tags),
        }


def new_message(
    role: str,
    content: str,
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Message:
    """Create a message with deterministic metadata and timestamp."""

    meta = dict(metadata) if metadata is not None else {}
    return Message(role=role, content=content, metadata=meta)


__all__ = ["DebateTranscript", "Message", "new_message"]
