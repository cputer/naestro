# Agent Companion Evaluators

## Overview

The Agent Companion program on Kaggle publishes a pair of reference
benchmarks that probe how well agentic systems reason over long-horizon tasks
and how reliably they execute tool calls. Naestro mirrors these competitions as
optional evaluator suites so teams can dry-run submissions locally before
pushing results to the Kaggle leaderboards. The evaluator registry is shipped
**disabled** until the infrastructure that automates submissions, auditing, and
reporting is in place.

## Benchmark suites

### `reasoning`
- **Kaggle anchor:** Agent Companion Reasoning Arena
- **Focus:** Scratchpad reasoning with self-reflection and tool planning
- **Datasets:**
  - `kaggle://agent-companion/reasoning-arena-dev-v1` (offline dev)
  - `kaggle://agent-companion/reasoning-arena-live-v1` (live leaderboard)
- **Metrics:** `final_answer_accuracy`, `scratchpad_consistency`,
  `self_reflection_coverage`, `tool_call_alignment`

### `tool_use`
- **Kaggle anchor:** Agent Companion Tool-Use Lab
- **Focus:** API/tool integrations, safety enforcement, execution robustness
- **Datasets:**
  - `kaggle://agent-companion/tool-use-lab-dev-v1` (offline dev)
  - `kaggle://agent-companion/tool-use-lab-live-v1` (live leaderboard)
- **Metrics:** `task_success_rate`, `api_call_accuracy`, `guardrail_compliance`,
  `latency_budget_adherence`

Each suite retains its own notes block in the configuration documenting the
operational caveats around credentials, notebook mirroring, and leaderboards.

## Configuration

The full configuration lives at
`configs/evaluators/agent_companion.yaml`. Both suites ship with
`enabled: false` and inherit the top-level guard. Toggle flags only after the
Kaggle submission automation and governance reviews are complete.

## Enablement steps

1. Review the Kaggle competition pages linked in the configuration to confirm
   data availability, submission windows, and any updated rules.
2. Run dry evaluations against the `*-dev-v1` datasets inside an isolated
   environment that mirrors the Kaggle execution environment.
3. Coordinate with compliance and governance teams to validate that leaderboards
   can be accessed from Naestro infrastructure and that credential handling is
   documented.
4. Flip `agent_companion.enabled` to `true` and selectively enable the suites
   (for example `suites.reasoning.enabled`) only after the automation and
   guardrails are in place.
5. When ready for production gating, monitor the live leaderboards and archive
   evaluator outputs alongside Kaggle submission artifacts for auditing.
