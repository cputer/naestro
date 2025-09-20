from __future__ import annotations

import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from naestro.agents import DebateOrchestrator, DebateSettings, Message, Role, Roles
from naestro.core.tracing import Tracer


def build_roles() -> Roles:
    def analyst_strategy(history: Sequence[Message]) -> str:
        turn = len(history) + 1
        return f"Turn {turn}: projected upside remains solid."

    def risk_strategy(history: Sequence[Message]) -> str:
        approvals = sum("approve" in message.content.lower() for message in history)
        return "Approve trade" if approvals > 0 else "Request more data"

    roles = Roles()
    roles.register(Role("analyst", "Builds the quantitative case", analyst_strategy))
    roles.register(Role("risk", "Checks drawdown constraints", risk_strategy))
    return roles


def main() -> None:
    roles = build_roles()
    with Tracer(run_name="debate-quickstart") as tracer:
        orchestrator = DebateOrchestrator(roles, tracer=tracer)
        outcome = orchestrator.run(
            ["analyst", "risk"],
            "Should we open a new position in AAPL?",
            settings=DebateSettings(rounds=2),
        )
    print("Debate transcript:")
    for message in outcome.transcript.messages:
        print(f"- {message.role}: {message.content}")
    print("Summary:", outcome.rationale)
    print("Trace stored in", tracer.run_path)


if __name__ == "__main__":
    main()
