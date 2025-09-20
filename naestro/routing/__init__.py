"""Public routing APIs exposed by :mod:`naestro.routing`."""

from __future__ import annotations

from .model_registry import DEFAULT_WEIGHTS, ModelInfo, ModelRegistry, REGISTRY
from .router import ModelRouter, RoutePolicy
from .task_specs import BaseTaskSpec, ChatTaskSpec, TaskSpec, ToolTaskSpec

__all__ = [
    "BaseTaskSpec",
    "ChatTaskSpec",
    "DEFAULT_WEIGHTS",
    "ModelInfo",
    "ModelRegistry",
    "ModelRouter",
    "RoutePolicy",
    "REGISTRY",
    "TaskSpec",
    "ToolTaskSpec",
]
