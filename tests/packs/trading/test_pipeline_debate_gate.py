from __future__ import annotations

import sys  # isort: split

from pathlib import Path
from typing import Sequence

import pytest

try:
    from naestro.agents.debate import DebateOrchestrator
    from naestro.agents.roles import Role, Roles
    from naestro.agents.schemas import Message
    from naestro.core.bus import MessageBus
except ModuleNotFoundError:
    sys.path.append(str(Path(__file__).resolve().parents[3]))
    from naestro.agents.debate import DebateOrchestrator
    from naestro.agents.roles import Role, Roles
    from naestro.agents.schemas import Message
    from naestro.core.bus import MessageBus

from packs.trading.agents import TradeDecision
from packs.trading.pipelines import DebateGate

pytest.importorskip("jsonschema")


def test_debate_gate_approves_trade() -> None:
    def analyst(history: Sequence[Message]) -> str:
        return "approve"

    def risk(history: Sequence[Message]) -> str:
        return "approve"

    roles = Roles()
    roles.register(Role("analyst", "Analyst", analyst))
    roles.register(Role("risk", "Risk", risk))
    gate = DebateGate(DebateOrchestrator(roles), ["analyst", "risk"])

    trade = TradeDecision(index=0, position=1, price=100.0, note="enter")
    assert gate.approve(trade) is True


def test_debate_gate_rejects_when_final_message_is_negative() -> None:
    def analyst(history: Sequence[Message]) -> str:
        return "reject"

    def risk(history: Sequence[Message]) -> str:
        return "reject"

    roles = Roles()
    roles.register(Role("analyst", "Analyst", analyst))
    roles.register(Role("risk", "Risk", risk))
    gate = DebateGate(DebateOrchestrator(roles), ["analyst", "risk"])

    trade = TradeDecision(index=0, position=1, price=150.0, note="enter")
    assert gate.approve(trade) is False


def test_debate_gate_formats_prompt_using_trade_details() -> None:
    bus = MessageBus()
    prompts: list[str] = []
    bus.subscribe("debate.started", lambda payload: prompts.append(payload["prompt"]))

    roles = Roles()
    orchestrator = DebateOrchestrator(roles, bus=bus)
    gate = DebateGate(orchestrator, [])

    trade = TradeDecision(index=0, position=1, price=123.456, note="scout")
    assert gate.approve(trade) is True
    assert prompts
    assert "123.46" in prompts[0]
    assert "scout" in prompts[0]
