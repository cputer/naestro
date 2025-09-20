"""Agent role definitions and deterministic debate utilities."""

from __future__ import annotations

from .debate import DebateOrchestrator, DebateOutcome, DebateSettings
from .roles import Responder, Role, Roles
from .schemas import DebateTranscript, Message, new_message

__all__ = [
    "DebateOrchestrator",
    "DebateOutcome",
    "DebateSettings",
    "DebateTranscript",
    "Message",
    "Responder",
    "Role",
    "Roles",
    "new_message",
]
