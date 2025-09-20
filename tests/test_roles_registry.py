from __future__ import annotations

from typing import Sequence

from naestro.agents import Role, RoleRegistry
from naestro.core.schemas import Message


def test_register_and_lookup_role() -> None:
    def strategy(history: Sequence[Message]) -> str:
        return f"seen {len(history)} messages"

    registry = RoleRegistry([Role("analyst", "Performs analysis", strategy)])
    role = registry.get("analyst")
    response = role.respond([])
    assert response == "seen 0 messages"


def test_update_metadata() -> None:
    def risk_strategy(history: Sequence[Message]) -> str:
        return "ok"

    registry = RoleRegistry([Role("risk", "Risk reviewer", risk_strategy)])
    registry.update_metadata("risk", {"level": "low"})
    updated = registry.get("risk")
    assert updated.metadata["level"] == "low"
