from __future__ import annotations

from typing import Sequence

from naestro.agents import Message, Role, Roles


def test_register_and_lookup_role() -> None:
    def strategy(history: Sequence[Message]) -> str:
        return f"seen {len(history)} messages"

    roles = Roles()
    roles.register(Role("quant", "Performs analysis", strategy))
    role = roles.get("quant")
    response = role.respond([])
    assert response == "seen 0 messages"


def test_update_metadata() -> None:
    def risk_strategy(history: Sequence[Message]) -> str:
        return "ok"

    roles = Roles()
    roles.register(Role("risk", "Risk reviewer", risk_strategy))
    roles.update_metadata("risk", {"level": "low"})
    updated = roles.get("risk")
    assert updated.metadata["level"] == "low"
