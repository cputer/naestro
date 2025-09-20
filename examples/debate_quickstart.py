"""Quickstart example running a deterministic debate between two roles."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from naestro import DebateOrchestrator, DebateSettings, Message, Role, Roles, Tracer


def build_roles() -> Roles:
    """Register a pair of roles representing the analyst and risk leads."""

    def analyst(history: Sequence[Message]) -> str:
        prompt = history[0].content if history else ""
        if "breakout" in prompt.lower():
            return "Momentum strong; approve breakout trade."
        return "No breakout yet; continue monitoring."

    def risk(history: Sequence[Message]) -> str:
        approvals = sum("approve" in message.content.lower() for message in history)
        return "Approve trade" if approvals else "Reject trade"

    roles = Roles()
    roles.register(Role("analyst", "Builds the quantitative case", analyst))
    roles.register(Role("risk", "Checks drawdown constraints", risk))
    return roles


def main() -> None:
    roles = build_roles()
    with Tracer(run_name="debate-quickstart") as tracer:
        orchestrator = DebateOrchestrator(roles, tracer=tracer)
        outcome = orchestrator.run(
            ["analyst", "risk"],
            "Should we open a new position in AAPL given the breakout?",
            settings=DebateSettings(rounds=2),
        )
    print("Debate transcript:")
    for message in outcome.transcript.messages:
        print(f"- {message.role}: {message.content}")
    print("Summary:", outcome.rationale)
    print("Trace stored in", tracer.run_path)


if __name__ == "__main__":
    main()
