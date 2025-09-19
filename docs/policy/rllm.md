# RLLM Policy Training

[← Back to README](../../README.md)

## Summary

- Reinforcement Learning for Language Models (RLLM) support provides a light-weight PPO loop for tuning Naestro's router collaboration policy using synthetic rollouts.
- The integration is implemented by [`RouterPPOAdapter`](../../integrations/policy/rllm_ppo_adapter.py), which wires a toy router environment, linear policy/value heads, and generalized advantage estimation updates.
- Operational toggles live in [`configs/policy/rllm.yaml`](../../configs/policy/rllm.yaml); the block is disabled by default and surfaces knobs for rollout services, trainers, evaluation, autopilot, experiment logging, and observability.

## Safety Scope

- Training is opt-in: `rllm.enabled`, `trainer.enabled`, and related flags stay `false` until a maintainer explicitly enables them, preventing accidental PPO runs in production deployments.
- The synthetic router environment exercises collaboration modes without touching live traffic or connected providers, ensuring experimentation stays sandboxed.
- Observability sinks (file logging, OTLP tracing, Weights & Biases) remain off unless configured, avoiding unsolicited telemetry streams.
- Tests such as [`tests/policy/test_rllm_config.py`](../../tests/policy/test_rllm_config.py) assert the feature ships disabled so CI will flag configuration drift.

## Enablement Steps

1. Copy or edit [`configs/policy/rllm.yaml`](../../configs/policy/rllm.yaml) and flip `rllm.enabled: true` alongside `trainer.enabled: true`; optionally turn on `experiment`, `evaluation`, or `observability` blocks as needed.
2. Adjust PPO hyperparameters (`rollout_length`, `mini_batch_size`, etc.) and `reward_weights` inside the same file to reflect the router behaviors you want to reward or penalize.
3. (Optional) Configure logging/metrics destinations by setting `observability.logging.destination` and the `observability.metrics` backend before launching a run.
4. Execute the trainer via [`scripts/run_router_ppo.py`](../../scripts/run_router_ppo.py):

   ```bash
   python scripts/run_router_ppo.py --config configs/policy/rllm.yaml --updates 8 --seed 42
   ```

   The CLI respects the enablement flags, seeds, and episode length specified via arguments or configuration.
5. Review console output or the configured log destination to confirm PPO progress and inspect mean reward, policy/value losses, and entropy per update.

## Artifact Locations

- When `experiment.enabled` is true, PPO snapshots land under `experiment.output_dir` (default `outputs/rllm/`):
  - `training_history.json` – per-update reward and loss metrics.
  - `policy_state.npz` – serialized linear policy/value weights.
  - `metadata.json` – run metadata (seed, update count, PPO params, reward weights).
  - `config_snapshot.yaml` – copy of the resolved configuration used for the run.
- If observability logging is enabled, structured logs stream to `observability.logging.destination` (defaults to `logs/rllm.log` when configured).
- Metrics exporters such as Weights & Biases read from `observability.metrics.*`; populate `project`, `entity`, and `tags` to publish training curves externally.
- Traces emit to the configured OTLP endpoint when `observability.tracing.enabled` is true.
