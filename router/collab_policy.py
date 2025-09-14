"""Collaboration policy definitions and enforcement."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CollaborationMode(str, Enum):
    """Supported collaboration modes."""

    SOLO = "solo"
    CONSULT = "consult"
    COLLABORATE = "collaborate"
    CONSENSUS = "consensus"
    SWARM = "swarm"


@dataclass(frozen=True)
class PolicyRule:
    """Rule describing allowed agent counts for a mode."""

    min_agents: int
    max_agents: int | None = None


class CollaborationPolicy:
    """Collection of collaboration policy rules.

    The policy enforces simple numerical constraints on the number of agents
    involved in a request.  More sophisticated behaviour can be layered on top
    by callers as needed.
    """

    RULES: dict[CollaborationMode, PolicyRule] = {
        CollaborationMode.SOLO: PolicyRule(min_agents=1, max_agents=1),
        CollaborationMode.CONSULT: PolicyRule(min_agents=1, max_agents=2),
        CollaborationMode.COLLABORATE: PolicyRule(min_agents=2),
        CollaborationMode.CONSENSUS: PolicyRule(min_agents=2),
        CollaborationMode.SWARM: PolicyRule(min_agents=3),
    }

    @classmethod
    def enforce(cls, mode: CollaborationMode, num_agents: int) -> None:
        """Ensure ``num_agents`` satisfies the policy for ``mode``.

        Args:
            mode: The collaboration mode being used.
            num_agents: Number of participating agents.

        Raises:
            ValueError: If the policy for ``mode`` is violated.
        """

        rule = cls.RULES[mode]
        if num_agents < rule.min_agents:
            raise ValueError(
                f"{mode.value} mode requires at least {rule.min_agents} agent(s)"
            )
        if rule.max_agents is not None and num_agents > rule.max_agents:
            raise ValueError(
                f"{mode.value} mode allows at most {rule.max_agents} agent(s)"
            )
