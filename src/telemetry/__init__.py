"""Telemetry metrics for Naestro.

Exposes lightweight counters and gauges used across the server, router and
prompt layers.  The metrics are intentionally simple so they can operate in the
unit test environment without any external dependencies."""

from .metrics import (
    collab_routes,
    collab_prompts,
    collab_prompt_depth,
    orchestrate_requests,
    telemetry_events,
)

__all__ = [
    "collab_routes",
    "collab_prompts",
    "collab_prompt_depth",
    "orchestrate_requests",
    "telemetry_events",
]
