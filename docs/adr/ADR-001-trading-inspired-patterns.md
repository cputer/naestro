# ADR-001 — TradingAgents-inspired Patterns

- **Status:** Accepted
- **Date:** 2024-04-12

## Context

We needed a compact, deterministic showcase for Naestro that explains how debates,
policy boards, and routing combine into production-ready workflows. The
TradingAgents prompt already illustrated these behaviours in a well-understood
domain (trading), making it an ideal source of inspiration.

## Decision

We extracted the underlying patterns—roles and debate loops, message bus
telemetry, policy governance, model routing, and an end-to-end pack—and codified
them as domain-agnostic components. Documentation within `docs/` now mirrors the
TradingAgents vocabulary so practitioners can map between the prompt and Naestro
implementations.

## Consequences

- The trading pack acts as a canonical example that teams can fork and repurpose.
- Deterministic behaviour allows CI pipelines to replay transcripts and policy
  decisions without external dependencies.
- Observability hooks (`debate.*`, `policy.check`, `routing.evaluated`,
  `trade.executed`) provide end-to-end telemetry out of the box.

## Alternatives considered

- **Ad-hoc tutorials.** Rejected because they lacked the architectural cohesion
  offered by a single prompt-inspired narrative.
- **Domain rewrite.** Rejected because keeping the trading metaphor improves
  discoverability for the existing TradingAgents community.

## Follow-up work

- Capture more domain templates (procurement, incident response) using the same
  primitives.
- Expand testing fixtures so each component ships with golden transcripts and
  payloads.
- Document migration notes for teams upgrading from earlier Naestro builds.
