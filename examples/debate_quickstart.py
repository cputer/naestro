"""Run a minimal deterministic debate."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from naestro.agents import Role, RoleRegistry
from naestro.core.debate import DebateOrchestrator, DebateSettings
from naestro.core.schemas import Message
from naestro.core.tracing import Tracer


def build_registry() -> RoleRegistry:
    def analyst_strategy(history: Sequence[Message]) -> str:
        turn = len(history) + 1
        return f"Turn {turn}: projected upside remains solid."

    def risk_strategy(history: Sequence[Message]) -> str:
        approvals = sum("approve" in message.content.lower() for message in history)
        return "Approve trade" if approvals > 0 else "Request more data"

    return RoleRegistry(
        [
            Role("analyst", "Builds the quantitative case", analyst_strategy),
            Role("risk", "Checks drawdown constraints", risk_strategy),
        ]
    )


def main() -> None:
    registry = build_registry()
    with Tracer(run_name="debate-quickstart") as tracer:
        orchestrator = DebateOrchestrator(registry, tracer=tracer)
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
