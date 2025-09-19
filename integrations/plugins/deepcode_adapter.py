"""DeepCode plugin adapter stub.

This module provides a placeholder implementation that documents the future
work required to connect DeepCode with Naestro's plugin system. The real
integration will be added in a later iteration.
"""

from __future__ import annotations

from collections.abc import Mapping


class DeepCodeAdapter:
    """Placeholder adapter for the DeepCode multi-agent coding framework."""

    def __init__(self, config: Mapping[str, object] | None = None) -> None:
        """Store configuration for the adapter without performing any setup."""
        self.config = dict(config or {})

    def build_from_source(self, source: str | Mapping[str, object] | None = None) -> dict[str, object]:
        """Return a placeholder response indicating the adapter is not yet implemented."""
        return {
            "status": "not_wired",
            "message": "DeepCode adapter is not wired yet",
            "source": source,
        }
