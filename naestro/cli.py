"""Command line entry point for Naestro."""

from __future__ import annotations

import argparse
from typing import Sequence, cast

from naestro.agents import Role, RoleRegistry
from naestro.core.debate import DebateOrchestrator, DebateSettings
from naestro.core.schemas import Message
from naestro.core.tracing import Tracer
from naestro.governance import Decision, Governor, Policy, PolicyResult
from packs.trading import (
    DebateGate,
    ExecutionAgent,
    RiskAgent,
    SignalAgent,
    TradingPipeline,
)


def build_roles() -> RoleRegistry:
    def analyst(history: Sequence[Message]) -> str:
        return "Approve trade" if len(history) % 2 == 0 else "Highlight momentum"

    def risk(history: Sequence[Message]) -> str:
        approvals = sum("approve" in message.content.lower() for message in history)
        return "Approve trade" if approvals >= 1 else "Reject trade"

    return RoleRegistry(
        [
            Role("analyst", "Analyst reviewing opportunities", analyst),
            Role("risk", "Risk reviewer", risk),
        ]
    )


def build_governor() -> Governor:
    governor = Governor()

    def guard_drawdown(decision: Decision) -> PolicyResult:
        raw_drawdown = decision.metadata.get("max_drawdown", 0.0)
        drawdown = float(cast(float, raw_drawdown))
        passed = drawdown <= 3.0
        reason = "Drawdown ok" if passed else f"Drawdown {drawdown:.2f} too high"
        return PolicyResult(name="drawdown", passed=passed, reason=reason)

    def guard_return(decision: Decision) -> PolicyResult:
        passed = decision.score >= 0.2
        reason = "Return adequate" if passed else "Return too low"
        return PolicyResult(name="return", passed=passed, reason=reason)

    governor.register(Policy("drawdown", "Protect against drawdown", guard_drawdown))
    governor.register(Policy("return", "Minimum return threshold", guard_return))
    return governor


def list_roles(registry: RoleRegistry) -> None:
    print("Registered roles:")
    for role in registry.list():
        print(f"- {role.name}: {role.description}")


def run_debate(registry: RoleRegistry, prompt: str, rounds: int) -> None:
    with Tracer(run_name="cli-debate") as tracer:
        orchestrator = DebateOrchestrator(registry, tracer=tracer)
        outcome = orchestrator.run(
            [role.name for role in registry.list()],
            prompt,
            settings=DebateSettings(rounds=rounds),
        )
    print("Transcript:")
    for message in outcome.transcript.messages:
        print(f"  {message.role}: {message.content}")
    print("Trace stored in", tracer.run_path)


def run_pipeline(registry: RoleRegistry) -> None:
    gate = DebateGate(DebateOrchestrator(registry), ["analyst", "risk"])
    pipeline = TradingPipeline(
        SignalAgent(window=2),
        RiskAgent(max_exposure=1, min_confidence=0.15),
        ExecutionAgent(),
        debate_gate=gate,
        governor=build_governor(),
    )
    prices = [100.0, 101.0, 102.0, 101.5, 103.0]
    result = pipeline.run(prices)
    print("Pipeline trades:")
    for trade in result.trades:
        print(f"  idx={trade.index} price={trade.price:.2f} note={trade.note}")
    print("Governance:")
    for policy_result in result.governance_results:
        status = "PASS" if policy_result.passed else "FAIL"
        print(f"  {policy_result.name}: {status} - {policy_result.reason}")
    print("Pipeline approved:", result.approved)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Naestro CLI utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list-roles", help="List registered roles")

    debate_parser = subparsers.add_parser("run-debate", help="Run a sample debate")
    debate_parser.add_argument("--prompt", required=True)
    debate_parser.add_argument("--rounds", type=int, default=1)

    subparsers.add_parser("run-pipeline", help="Execute the trading pipeline demo")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    registry = build_roles()
    if args.command == "list-roles":
        list_roles(registry)
    elif args.command == "run-debate":
        run_debate(registry, args.prompt, args.rounds)
    elif args.command == "run-pipeline":
        run_pipeline(registry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
