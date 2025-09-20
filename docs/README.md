# Naestro: TradingAgents-inspired, Domain-Agnostic Patterns

This documentation set reframes the trading demo shipped with Naestro as a
collection of reusable building blocks. Each guide distils the playbook exposed
by the TradingAgents prompt into deterministic, domain-agnostic primitives that
can be remixed in other automation pipelines.

## Quick start map

- [Roles & Debate Protocol](patterns/roles-and-debate.md) — Stage deterministic
  conversations between specialised actors that mirror the TradingAgents
  prompt.
- [Message Bus Signals](core/message-bus.md) — Capture every state transition
  with structured events that power replay, analytics, and guard-rails.
- [Governor Policy Board](governance/governor.md) — Combine policies that veto
  unsafe outcomes before they leave the orchestrator.
- [Model Routing Matrix](routing/model-routing.md) — Score available model
  bundles against task profiles using transparent heuristics.
- [Trading Pack Walkthrough](packs/trading.md) — Assemble the full end-to-end
  pipeline, from signal detection to post-trade metrics, with deterministic
  defaults.
- [ADR-001 — TradingAgents-inspired Patterns](adr/ADR-001-trading-inspired-patterns.md)
  — Capture the architectural reasoning behind this pattern library.

## Implementation pillars

### Deterministic orchestration

The debate orchestrator, message bus, and governor are written to keep behaviour
replayable. You can run the trading pipeline offline, record every intermediate
state, and reliably assert on final outcomes. This determinism makes the
patterns safe to embed inside CI pipelines or regulatory workflows.

### Observability baked in

The message bus fan-outs for debate turns, policy checks, and routing decisions.
Each event carries structured payloads that allow downstream consumers to build
dashboards, trigger alerts, or replay the full transcript of a run.

### Extensible by design

Although the examples lean on trading metaphors, every component accepts
strategy callables or data sources that can be swapped for other domains.
Combine the guides in different arrangements to stand up procurement reviews,
incident response drills, or creative brainstorming assistants.

## Next steps

Read through the guides in the order above to understand how debates, policies,
and routing collaborate. When you are ready to experiment, copy the trading pack
and substitute your own signal generators, policies, and routing profiles.
