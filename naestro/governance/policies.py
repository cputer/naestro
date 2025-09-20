"""Reusable policy definitions used by the :class:`Governor`."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol

from .schemas import Decision, PolicyInput

PolicyResult = Decision
"""Alias maintained for backwards compatibility with earlier releases."""


PolicyChecker = Callable[[PolicyInput], Decision]
"""Callable signature used by :class:`Policy` wrappers."""


class PolicyLike(Protocol):
    """Structural protocol implemented by policy objects."""

    name: str
    description: str

    def evaluate(  # pragma: no cover - protocol method
        self, policy_input: PolicyInput
    ) -> Decision:
        """Evaluate the provided input and return a policy decision."""


@dataclass(slots=True)
class Policy:
    """Wraps a simple callable into a policy instance."""

    name: str
    description: str
    checker: PolicyChecker

    def evaluate(self, policy_input: PolicyInput) -> Decision:
        return self.checker(policy_input)


@dataclass(slots=True)
class BudgetPolicy:
    """Ensure usage stays within a configured budget."""

    name: str = "budget"
    description: str = (
        "Validate that expected spend does not exceed the available budget."
    )

    def evaluate(self, policy_input: PolicyInput) -> Decision:
        budget = policy_input.budget
        if budget is None:
            return Decision(
                name=self.name,
                passed=True,
                reason="No budget configuration provided",
            )
        limit = budget.limit
        usage = budget.usage
        currency = budget.currency
        metadata = {
            "limit": limit,
            "usage": usage,
            "currency": currency,
        }
        if limit is None or usage is None:
            return Decision(
                name=self.name,
                passed=True,
                reason="Budget data incomplete",
                metadata=metadata,
            )
        usage_value = float(usage)
        limit_value = float(limit)
        metadata |= {"usage": usage_value, "limit": limit_value}
        if usage_value <= limit_value:
            reason = (
                f"{usage_value:.2f} {currency} within "
                f"{limit_value:.2f} {currency} budget"
            )
            return Decision(
                name=self.name,
                passed=True,
                reason=reason,
                metadata=metadata,
            )
        excess = usage_value - limit_value
        metadata["excess"] = excess
        reason = (
            f"{usage_value:.2f} {currency} exceeds budget {limit_value:.2f} {currency} "
            f"by {excess:.2f} {currency}"
        )
        return Decision(
            name=self.name,
            passed=False,
            reason=reason,
            severity="critical",
            metadata=metadata,
        )


@dataclass(slots=True)
class SafetyPolicy:
    """Check flagged categories against the configured block list."""

    name: str = "safety"
    description: str = (
        "Ensure content moderation checks do not report blocked categories."
    )

    def evaluate(self, policy_input: PolicyInput) -> Decision:
        safety = policy_input.safety
        if safety is None:
            return Decision(
                name=self.name,
                passed=True,
                reason="No safety signals provided",
            )
        blocked = set(safety.blocked_categories)
        flagged = set(safety.flagged_categories)
        violations = sorted(blocked & flagged)
        metadata = {
            "blocked_categories": sorted(blocked),
            "flagged_categories": sorted(flagged),
            "annotations": dict(safety.annotations),
        }
        if not violations:
            return Decision(
                name=self.name,
                passed=True,
                reason="No blocked categories flagged",
                metadata=metadata,
            )
        metadata["violations"] = violations
        reason = "Flagged blocked categories: " + ", ".join(violations)
        return Decision(
            name=self.name,
            passed=False,
            reason=reason,
            severity="critical",
            metadata=metadata,
        )


@dataclass(slots=True)
class RiskPolicy:
    """Validate that the risk score is below an acceptable threshold."""

    name: str = "risk"
    description: str = (
        "Require the risk score to remain under the configured threshold."
    )
    max_score: float | None = None

    def evaluate(self, policy_input: PolicyInput) -> Decision:
        risk = policy_input.risk
        score = float(risk.score) if risk and risk.score is not None else None
        threshold = (
            float(risk.threshold)
            if risk and risk.threshold is not None
            else (float(self.max_score) if self.max_score is not None else None)
        )
        metadata = {
            "score": score,
            "threshold": threshold,
            "label": risk.label if risk else None,
        }
        if score is None or threshold is None:
            return Decision(
                name=self.name,
                passed=True,
                reason="No risk constraints provided",
                metadata=metadata,
            )
        passed = score <= threshold
        if passed:
            reason = f"risk score {score:.2f} within threshold {threshold:.2f}"
        else:
            reason = f"risk score {score:.2f} exceeds threshold {threshold:.2f}"
        severity = "info" if passed else "warning"
        return Decision(
            name=self.name,
            passed=passed,
            reason=reason,
            severity=severity,
            metadata=metadata,
        )


@dataclass(slots=True)
class LatencySLOPolicy:
    """Ensure latency measurements remain within an SLO."""

    name: str = "latency_slo"
    description: str = (
        "Validate that observed latency does not exceed the SLO."
    )
    slo_ms: float | None = None

    def evaluate(self, policy_input: PolicyInput) -> Decision:
        latency = policy_input.latency
        observed = (
            float(latency.value_ms)
            if latency and latency.value_ms is not None
            else None
        )
        slo = (
            float(latency.slo_ms)
            if latency and latency.slo_ms is not None
            else (float(self.slo_ms) if self.slo_ms is not None else None)
        )
        metadata = {
            "observed_ms": observed,
            "slo_ms": slo,
            "window": latency.window if latency else None,
        }
        if observed is None or slo is None:
            return Decision(
                name=self.name,
                passed=True,
                reason="Latency data unavailable",
                metadata=metadata,
            )
        passed = observed <= slo
        if passed:
            reason = f"latency {observed:.2f}ms within SLO {slo:.2f}ms"
        else:
            reason = f"latency {observed:.2f}ms exceeds SLO {slo:.2f}ms"
        severity = "info" if passed else "warning"
        return Decision(
            name=self.name,
            passed=passed,
            reason=reason,
            severity=severity,
            metadata=metadata,
        )


__all__ = [
    "BudgetPolicy",
    "Decision",
    "LatencySLOPolicy",
    "Policy",
    "PolicyChecker",
    "PolicyLike",
    "PolicyResult",
    "RiskPolicy",
    "SafetyPolicy",
]
