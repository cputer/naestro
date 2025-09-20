"""Typed schemas used by the governance subsystem."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Literal
from typing_extensions import TypedDict

from pydantic import BaseModel, ConfigDict, Field


class BudgetContext(BaseModel):
    """Budget information associated with a policy evaluation."""

    limit: float | None = Field(
        default=None,
        description="Maximum permitted spend expressed in the selected currency.",
    )
    usage: float | None = Field(
        default=None,
        description="Expected spend for the current request or workflow stage.",
    )
    currency: str = Field(
        default="usd",
        description="Currency code for the budget figures (ISO 4217 preferred).",
    )


class SafetyContext(BaseModel):
    """Signals emitted by safety classifiers or heuristic filters."""

    blocked_categories: set[str] = Field(
        default_factory=set,
        description="Categories that are disallowed for the current workflow.",
    )
    flagged_categories: set[str] = Field(
        default_factory=set,
        description="Categories flagged by upstream moderation systems.",
    )
    annotations: Mapping[str, Any] = Field(
        default_factory=dict,
        description="Raw annotations provided by the moderation system.",
    )


class RiskContext(BaseModel):
    """Structured risk metrics produced by a scoring component."""

    score: float | None = Field(
        default=None,
        description="Calculated risk score for the request.",
    )
    threshold: float | None = Field(
        default=None,
        description="Maximum acceptable risk score for the request.",
    )
    label: str | None = Field(
        default=None,
        description="Optional textual descriptor for the risk score.",
    )


class LatencyContext(BaseModel):
    """Latency measurements gathered from observability systems."""

    value_ms: float | None = Field(
        default=None,
        description="Observed or projected latency in milliseconds.",
    )
    slo_ms: float | None = Field(
        default=None,
        description="Latency service level objective in milliseconds.",
    )
    window: str | None = Field(
        default=None,
        description="Window or quantile associated with the latency measurement.",
    )


class PolicyPatch(TypedDict, total=False):
    """Declarative patch operation produced by a policy decision."""

    op: Literal["set", "remove", "merge"]
    path: Sequence[str | int]
    value: Any


class PolicyInput(BaseModel):
    """Input payload evaluated by governance policies."""

    model_config = ConfigDict(extra="allow")

    subject: str
    score: float | None = Field(default=None)
    metadata: dict[str, Any] = Field(default_factory=dict)
    plan: dict[str, Any] = Field(default_factory=dict)
    budget: BudgetContext | None = None
    safety: SafetyContext | None = None
    risk: RiskContext | None = None
    latency: LatencyContext | None = None


class Decision(BaseModel):
    """Outcome emitted by a policy evaluation."""

    model_config = ConfigDict(extra="allow")

    name: str
    passed: bool
    reason: str
    severity: Literal["info", "warning", "critical"] = "info"
    metadata: dict[str, Any] = Field(default_factory=dict)
    score: float | None = Field(default=None)
    patches: tuple[PolicyPatch, ...] = Field(default_factory=tuple)


__all__ = [
    "BudgetContext",
    "Decision",
    "LatencyContext",
    "PolicyInput",
    "PolicyPatch",
    "RiskContext",
    "SafetyContext",
]
