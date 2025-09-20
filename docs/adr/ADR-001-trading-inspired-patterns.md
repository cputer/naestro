# ADR-001: Trading-Inspired Patterns

- Status: Accepted
- Date: 2024-04-12

## Context

We needed a deterministic showcase tying together the Naestro debate
orchestrator, governance policies and routing logic. Trading workflows provide a
rich metaphor with familiar concepts such as signals, risk checks and execution
pipelines.

## Decision

We introduced a `packs.trading` module that layers the debate orchestrator over a
signal/risk/execution pipeline. Governance policies guard the final output and
routing profiles demonstrate how different model configurations can serve the
pipeline. All behaviours are deterministic to keep tests and examples stable.

## Consequences

- Examples and tests now run without network connectivity or external APIs.
- The debate orchestrator emits trace files under `.naestro_runs` for inspection.
- Future packs can reuse the same primitives and governance hooks established in
  this ADR.
