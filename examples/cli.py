"""Demonstrate the Naestro CLI commands programmatically."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from naestro import cli


def main() -> None:
    print("== Run debate demo ==")
    cli.main(["run-debate", "--prompt", "Is the setup favorable?", "--rounds", "2"])
    print("\n== Run trading demo ==")
    cli.main(["run-trading"])
    print("\n== Run governed trading demo ==")
    cli.main(["run-governed"])


if __name__ == "__main__":
    main()
