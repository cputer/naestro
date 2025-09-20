"""Typed dictionaries describing routing task metadata."""

from __future__ import annotations

from typing import (
    Mapping,
    NotRequired,
    Sequence,
)

from typing_extensions import TypedDict

CapabilityList = Sequence[str] | set[str] | frozenset[str]


class BaseTaskSpec(TypedDict):
    """Base task specification used by the router."""

    task: str
    required_capabilities: CapabilityList


class TaskSpec(BaseTaskSpec, total=False):
    """Generic task spec with optional scoring and constraint hints."""

    weights: Mapping[str, float]
    exclude: CapabilityList
    min_quality: float
    max_latency: float
    max_cost: float
    metadata: Mapping[str, object]


class ChatTaskSpec(TaskSpec, total=False):
    """Specialisation for conversational tasks."""

    style: str
    expected_response_tokens: int


class ToolTaskSpec(TaskSpec, total=False):
    """Specialisation for tool or function calling tasks."""

    tools: Sequence[str]
    allow_partial_tools: NotRequired[bool]


__all__ = [
    "BaseTaskSpec",
    "TaskSpec",
    "ChatTaskSpec",
    "ToolTaskSpec",
    "CapabilityList",
]
