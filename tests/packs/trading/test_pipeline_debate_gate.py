from __future__ import annotations

from typing import Sequence

from naestro.agents import DebateOrchestrator, Message, Role, Roles
from packs.trading.pipelines import DebateGate


def test_debate_gate_approves_trade() -> None:
    def analyst(history: Sequence[Message]) -> str:
        return "approve"

    def risk(history: Sequence[Message]) -> str:
        return "approve"

    roles = Roles()
    roles.register(Role("analyst", "Analyst", analyst))
    roles.register(Role("risk", "Risk", risk))
    gate = DebateGate(DebateOrchestrator(roles), ["analyst", "risk"])

    class Trade:
        price = 100.0
        note = "enter"

    assert gate.approve(Trade()) is True


def test_debate_gate_handles_empty_participants() -> None:
    roles = Roles()
    gate = DebateGate(DebateOrchestrator(roles), [])

    class Trade:
        price = 100.0
        note = "enter"

    assert gate.approve(Trade()) is True
