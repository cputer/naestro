"""Core public API surface for the lightweight Naestro runtime package.

This module exposes the most frequently used primitives so that example code and
third party extensions can import them directly from :mod:`naestro`.
"""

from __future__ import annotations

from .agents.registry import Role, RoleRegistry
from .core.bus import LoggingMiddleware, MessageBus
from .core.debate import DebateOrchestrator
from .core.schemas import DebateTranscript, Message
from .core.tracing import Tracer
from .governance.governor import Decision, Governor
from .governance.policies import Policy
from .routing.registry import ModelProfile, ModelRegistry
from .routing.router import Router, RoutingRequest

__all__ = [
    "Decision",
    "DebateOrchestrator",
    "DebateTranscript",
    "LoggingMiddleware",
    "Message",
    "MessageBus",
    "ModelProfile",
    "ModelRegistry",
    "Policy",
    "Role",
    "RoleRegistry",
    "Governor",
    "Router",
    "RoutingRequest",
    "Tracer",
]
