# Codex Prompt: HICRA Credit Assignment Package

## Objective
Stand up the HICRA credit assignment training package inside the repository so
Codex can implement and test the module end-to-end.

## Project Structure
Create the training package under `src/training/` with the following skeleton:

```
src/
  training/
    __init__.py
    hicra.py
```

The tests for the assigner should live alongside the other unit suites, e.g.
`tests/training/test_hicra.py`.

## Implementation Notes
- Expose the main entry point as `HICRACreditAssigner` inside
  `src/training/hicra.py`.
- Update any existing references so Codex always imports the class with:

  ```python
  from src.training.hicra import HICRACreditAssigner
  ```

- Build lightweight fixtures so tests can instantiate the assigner without
  orchestrator dependencies.
- Place the trainer defaults in `configs/training/hicra.yaml` inside the
  existing `configs/` tree. Use this real configuration file (create it in the
  `configs/training/` directory) rather than referencing a placeholder
  `config.yaml`.
- Instrument HICRA metrics through the shared telemetry helpers in
  `src.telemetry.metrics`. Reuse the provided `LabeledCounter`/`LabeledGauge`
  types and follow their naming conventions (`*_total` for counters, direct
  unit suffixes such as `_ms` for gauges) instead of wiring into a placeholder
  like `naestro/metrics/logger.py`.

## TODO / Integration Follow-Ups
- When orchestrator support is ready, thread the trained assigner into
  `src/orchestrator/orchestrator.py` and `src/orchestrator/main.py`.
- The live orchestrator entry points already exist under
  `src/orchestrator/main.py` (FastAPI) and `src/orchestrator/orchestrator.py`
  (LangGraph workflow). Target these modules when wiring policies or runtime
  hooks instead of referencing a placeholder like
  `naestro/training/orchestrator_rl.py`.
- Router policy training is controlled through the real CLI at
  `scripts/run_router_ppo.py`. When adjusting PPO behavior, update that script
  and reference its actual flags: `--config`, `--updates`, `--seed`, and
  `--episode-length`.
- Document how the training outputs plug into the routers and agents under
  `src/orchestrator/` for future automation.
- Add integration smoke tests once the orchestrator glue code in
  `src/orchestrator/math_agent.py` consumes the training artifacts.

## Validation Checklist
- Unit tests import `HICRACreditAssigner` from `src.training.hicra`.
- Ensure linting passes for the new package.
- Capture README updates if configuration steps change.
