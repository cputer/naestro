"""Contains Agents runtime adapter stub.

This module provides a placeholder implementation that documents the future
work required to wire Contains Agents into the runtime integrations. The real
bindings will be added in a later iteration.
"""


class ContainsAgentsAdapter:
    """TODO: Shim adapter until Contains Agents bindings are implemented."""

    def __init__(self, config: dict | None = None) -> None:
        """Store configuration for the adapter without performing any setup."""
        self.config = config or {}

    def run_plan(self, plan: dict | None = None) -> dict:
        """Return a placeholder response indicating the adapter is not ready."""
        # TODO: Replace stub once Contains Agents wiring is implemented.
        return {
            "status": "not_wired",
            "message": "Contains Agents adapter is not wired yet",
            "plan": plan,
        }
