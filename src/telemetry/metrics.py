"""Lightweight metrics primitives used for unit tests.

The real project is expected to use OpenTelemetry/Prometheus, but the test
environment keeps dependencies to a minimum.  These classes mimic a tiny subset
of the Prometheus client API so application code can instrument itself while the
unit tests can assert on metric values.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class LabeledCounter:
    """Counter supporting simple string labels."""

    name: str
    description: str
    _values: Dict[str, int] = field(default_factory=lambda: defaultdict(int))

    def inc(self, label: str, amount: int = 1) -> None:
        self._values[label] += amount

    def get(self, label: str) -> int:
        return self._values[label]

    def reset(self) -> None:
        self._values.clear()


@dataclass
class SimpleCounter:
    """Counter without labels."""

    name: str
    description: str
    value: int = 0

    def inc(self, amount: int = 1) -> None:
        self.value += amount

    def get(self) -> int:
        return self.value

    def reset(self) -> None:
        self.value = 0


@dataclass
class LabeledGauge:
    """Gauge storing the last value per label."""

    name: str
    description: str
    _values: Dict[str, float] = field(default_factory=dict)

    def set(self, label: str, value: float) -> None:
        self._values[label] = float(value)

    def get(self, label: str) -> float:
        return self._values.get(label, 0.0)

    def reset(self) -> None:
        self._values.clear()


# Collaboration metrics -------------------------------------------------------

# Number of routed requests per collaboration mode.
collab_routes = LabeledCounter(
    "collab_routes_total", "Number of routed requests per collaboration mode."
)

# Number of prompts composed per collaboration mode.
collab_prompts = LabeledCounter(
    "collab_prompts_total", "Number of prompts composed per collaboration mode."
)

# Last requested collaboration depth per mode.
collab_prompt_depth = LabeledGauge(
    "collab_prompt_depth", "Last requested collaboration depth per mode."
)

# Server level metrics --------------------------------------------------------

# Total orchestrate requests seen by the gateway server.
orchestrate_requests = SimpleCounter(
    "orchestrate_requests_total", "Total orchestrate requests processed."
)

# Number of telemetry events emitted by the gateway server.
telemetry_events = SimpleCounter(
    "telemetry_events_total", "Telemetry events emitted by the server."
)
