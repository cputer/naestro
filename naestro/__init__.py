"""Convenience re-exports for the primary Naestro building blocks."""

from __future__ import annotations

from .agents import DebateSettings, Message
from .agents.debate import DebateConfig, DebateOrchestrator
from .agents.roles import Role, Roles
from .agents.schemas import AgentMessage, Critique, Verdict
from .core.bus import MessageBus, logging_mw, redaction_mw
from .core.trace import start_trace, write_debate_transcript, write_governor
from .core.tracing import Tracer
from .governance import Decision, Policy, PolicyInput
from .governance.governor import Governor, apply_patches
from .governance.policies import (
    BudgetPolicy,
    LatencySLOPolicy,
    RiskPolicy,
    SafetyPolicy,
)
from .routing.model_registry import ModelInfo
from .routing.router import ModelRouter, RoutePolicy
from .routing.task_specs import (
    BaseTaskSpec,
    CapabilityList,
    ChatTaskSpec,
    TaskSpec,
    ToolTaskSpec,
)

__all__ = (
    "DebateOrchestrator",
    "DebateConfig",
    "DebateSettings",
    "Role",
    "Roles",
    "Message",
    "AgentMessage",
    "Critique",
    "Verdict",
    "MessageBus",
    "logging_mw",
    "redaction_mw",
    "start_trace",
    "write_debate_transcript",
    "write_governor",
    "Tracer",
    "BudgetPolicy",
    "SafetyPolicy",
    "RiskPolicy",
    "LatencySLOPolicy",
    "Governor",
    "apply_patches",
    "Decision",
    "Policy",
    "PolicyInput",
    "ModelInfo",
    "ModelRouter",
    "RoutePolicy",
    "BaseTaskSpec",
    "TaskSpec",
    "ChatTaskSpec",
    "ToolTaskSpec",
    "CapabilityList",
)
