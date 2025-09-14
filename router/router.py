"""Simple router with collaboration policy enforcement."""

from __future__ import annotations

from typing import Iterable, Sequence

from .collab_policy import CollaborationMode, CollaborationPolicy


class Router:
    """Route requests to agents while enforcing collaboration policy."""

    def __init__(self, mode: CollaborationMode = CollaborationMode.SOLO) -> None:
        self.mode = mode

    def route(self, agents: Sequence[str] | Iterable[str]) -> Sequence[str]:
        """Validate agents according to the configured mode.

        The router itself does not perform any IO.  It simply checks the number
        of agents against the collaboration policy and returns the sequence.

        Args:
            agents: Sequence of agent identifiers.

        Returns:
            The provided sequence of agents.

        Raises:
            ValueError: If the agent count violates the collaboration policy.
        """

        agents = list(agents)
        CollaborationPolicy.enforce(self.mode, len(agents))
        return agents
