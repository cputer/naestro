"""Simple CLI wrapper for running evaluation suites."""

from __future__ import annotations

import argparse
from typing import Iterable

from evaluators import EvalSuiteRunner


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run NAESTRO evaluation suites")
    parser.add_argument(
        "suites",
        nargs="*",
        help="Names of suites to execute (defaults to all configured suites)",
    )
    return parser.parse_args()


def _selected_suites(names: list[str]) -> Iterable[str] | None:
    return names if names else None


def main() -> int:
    args = _parse_args()
    runner = EvalSuiteRunner()

    for suite in runner.iter_prepared_suites(_selected_suites(args.suites)):
        # Placeholder for the actual execution logic; determinism is configured
        # via EvalSuiteRunner.enable_for_suite before models load.
        print(
            f"Suite '{suite.name}' ready (deterministic={suite.deterministic}) with "
            f"datasets={runner.resolve_suite_datasets(suite)}"
        )

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
