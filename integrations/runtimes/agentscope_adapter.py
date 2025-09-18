"""AgentScope runtime adapter stub.

This module provides a placeholder implementation that documents the future
work required to wire AgentScope into the runtime integrations. The real
bindings will be added in a later iteration.
"""


class AgentScopeAdapter:
    """TODO: Shim adapter until AgentScope bindings are implemented."""

    def __init__(self, config: dict | None = None) -> None:
        """Store configuration for the adapter without performing any setup."""
        self.config = config or {}

    def run_plan(self, plan: dict | None = None) -> dict:
        """Return a placeholder response indicating the adapter is not ready."""
        return {
            "status": "not_wired",
            "message": "AgentScope adapter is not wired yet",
            "plan": plan,
        }
