# Orchestrator Collaboration Modes & Depth

Naestro's orchestrator supports several collaboration strategies when coordinating with online
models. These preferences control how aggressively the system fans out work across models and how
much autonomy the router has to escalate.

## Modes

When collaboration mode allows external automation imports, Researcher and Runner agents can pull
FlowTemplate workflows as starting points. Imported flows respect consent policies and can be
reviewed in Copilot depth before escalation.

- **solo** – run locally without consulting other models.
- **consult** – issue a single query to an online model and return.
- **collaborate** – delegate roles (Researcher, Coder, Reviewer) to multiple models.
- **consensus** – collaborate and require models to vote before responding.
- **swarm** – run structured debates across many models.

## Depth

Depth tunes the intensity of collaboration. `0` is minimal while `3` is exhaustive.

## Additional Flags

- **auto** – allow the router to escalate mode/depth if confidence is low and budget and latency
  caps permit.
- **ask_online** – when `false`, all cloud calls are blocked.
- **budget_usd** – maximum spend for the run.
- **p95_latency_s** – target 95th percentile latency.
- **answer_strategy** – one of `self_if_confident`, `aggregate_always`,
  `ask_clarify_below_threshold` (requires `confidence_threshold`).

## Example

The preferences can be supplied when launching a run or in a job spec:

```json
{
  "mode": "collaborate",
  "depth": 2,
  "auto": true,
  "budget_usd": 0.5
}
```

## Telemetry

Runs emit OpenTelemetry/Prometheus metrics prefixed with `orch.` capturing the selected mode, depth,
auto flag, budgets, and whether an automatic escalation occurred.

## References

See [`ROADMAP.md`](../ROADMAP.md) for upcoming work integrating these preferences throughout the
planner, router, prompt composer, and UI. Related external links are listed in
[REFERENCES.md](../REFERENCES.md).
