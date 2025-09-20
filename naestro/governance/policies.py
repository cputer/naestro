"""Reusable policy definitions used by the :class:`Governor`."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:  # pragma: no cover - import for typing only
    from naestro.governance.governor import Decision


@dataclass(slots=True)
class PolicyResult:
    name: str
    passed: bool
    reason: str


PolicyChecker = Callable[["Decision"], PolicyResult]


@dataclass(slots=True)
class Policy:
    name: str
    description: str
    checker: PolicyChecker

    def evaluate(self, decision: "Decision") -> PolicyResult:
        return self.checker(decision)


__all__ = ["Policy", "PolicyChecker", "PolicyResult"]
