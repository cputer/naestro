import argparse
from typing import Sequence, cast

from naestro.agents import DebateOrchestrator, DebateSettings, Message, Role, Roles
from naestro.core.tracing import Tracer
from naestro.governance import Decision, Governor, Policy, PolicyInput
from packs.trading import (
    DebateGate,
    ExecutionAgent,
    RiskAgent,
    SignalAgent,
    TradingPipeline,
)


def build_roles() -> Roles:
    def analyst(history: Sequence[Message]) -> str:
        return "Approve trade" if len(history) % 2 == 0 else "Highlight momentum"

    def risk(history: Sequence[Message]) -> str:
        approvals = sum("approve" in message.content.lower() for message in history)
        return "Approve trade" if approvals >= 1 else "Reject trade"

    roles = Roles()
    roles.register(Role("analyst", "Analyst reviewing opportunities", analyst))
    roles.register(Role("risk", "Risk reviewer", risk))
    return roles


def build_governor() -> Governor:
    governor = Governor()

    def guard_drawdown(payload: PolicyInput) -> Decision:
        raw_drawdown = payload.metadata.get("max_drawdown", 0.0)
        drawdown = float(cast(float, raw_drawdown))
        passed = drawdown <= 3.0
        reason = "Drawdown ok" if passed else f"Drawdown {drawdown:.2f} too high"
        return Decision(name="drawdown", passed=passed, reason=reason)

    def guard_return(payload: PolicyInput) -> Decision:
        score = payload.score or 0.0
        passed = score >= 0.2
        reason = "Return adequate" if passed else "Return too low"
        return Decision(name="return", passed=passed, reason=reason)

    governor.register(Policy("drawdown", "Protect against drawdown", guard_drawdown))
    governor.register(Policy("return", "Minimum return threshold", guard_return))
    return governor


def list_roles(roles: Roles) -> None:
    print("Registered roles:")
    for role in roles.list():
        print(f"- {role.name}: {role.description}")


def run_debate(roles: Roles, prompt: str, rounds: int) -> None:
    with Tracer(run_name="cli-debate") as tracer:
        orchestrator = DebateOrchestrator(roles, tracer=tracer)
        outcome = orchestrator.run(
            [role.name for role in roles.list()],
            prompt,
            settings=DebateSettings(rounds=rounds),
        )
    print("Transcript:")
    for message in outcome.transcript.messages:
        print(f"  {message.role}: {message.content}")
    print("Trace stored in", tracer.run_path)


def run_pipeline(roles: Roles) -> None:
    gate = DebateGate(DebateOrchestrator(roles), ["analyst", "risk"])
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
    roles = build_roles()
    if args.command == "list-roles":
        list_roles(roles)
    elif args.command == "run-debate":
        run_debate(roles, args.prompt, args.rounds)
    elif args.command == "run-pipeline":
        run_pipeline(roles)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
