"""Core public API surface for the lightweight Naestro runtime package.

This module exposes the most frequently used primitives so that example code and
third party extensions can import them directly from :mod:`naestro`.
"""

from __future__ import annotations

from .agents import (
    DebateOrchestrator,
    DebateOutcome,
    DebateSettings,
    DebateTranscript,
    Message,
    Role,
    Roles,
)
from .core.bus import LoggingMiddleware, MessageBus
from .core.tracing import Tracer
from .governance import (
    BudgetPolicy,
    Decision,
    Governor,
    LatencySLOPolicy,
    Policy,
    PolicyChecker,
    PolicyInput,
    PolicyLike,
    PolicyPatch,
    PolicyResult,
    RiskPolicy,
    SafetyPolicy,
    apply_patches,
)
from .routing import (
    BaseTaskSpec,
    ChatTaskSpec,
    ModelInfo,
    ModelRegistry,
    ModelRouter,
    REGISTRY,
    TaskSpec,
    ToolTaskSpec,
)

__all__ = [
    "BudgetPolicy",
    "Decision",
    "DebateOrchestrator",
    "DebateOutcome",
    "DebateSettings",
    "DebateTranscript",
    "Governor",
    "LatencySLOPolicy",
    "LoggingMiddleware",
    "Message",
    "MessageBus",
    "BaseTaskSpec",
    "ChatTaskSpec",
    "ModelInfo",
    "ModelRegistry",
    "ModelRouter",
    "Policy",
    "PolicyChecker",
    "PolicyInput",
    "PolicyLike",
    "PolicyPatch",
    "PolicyResult",
    "RiskPolicy",
    "Role",
    "Roles",
    "REGISTRY",
    "TaskSpec",
    "ToolTaskSpec",
    "SafetyPolicy",
    "Tracer",
    "apply_patches",
]
