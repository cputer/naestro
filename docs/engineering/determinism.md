# Deterministic Inference Guard

The deterministic inference guard pins runtime behavior so that model outputs are reproducible across runs, GPU hosts, and CI jobs. It is designed to make golden and canary evaluation suites reliable by removing the non-determinism introduced by random number generation and GPU kernels.

## Seeding Strategy

- Seeds Python `random`, NumPy, and PyTorch generators from a stable scenario hash (request id + model revision).
- Calls `torch.manual_seed()`/`torch.cuda.manual_seed_all()` on guard entry and replays the seed before every batch to stop drift over long-running jobs.
- Resets generator state after guard exit so that non-deterministic runs remain unaffected.

## cuDNN/cuBLAS Controls

- Forces deterministic algorithm selection with `torch.use_deterministic_algorithms(True)` and `torch.backends.cudnn.deterministic = True`.
- Disables cuDNN benchmarking (`torch.backends.cudnn.benchmark = False`) and TF32 fast paths (`torch.backends.cuda.matmul.allow_tf32 = False`).
- Sets `CUBLAS_WORKSPACE_CONFIG` to `:4096:8` when initializing CUDA contexts to stabilize GEMM ordering.

## Runtime Configuration Toggle

- Exposed via `runtime.determinism.guard_enabled` in service configuration and the `NAESTRO_DETERMINISTIC_GUARD=1` environment variable.
- The guard defaults to **on** for production inference. Operators can disable it for exploratory runs by setting the toggle to `false` or exporting `NAESTRO_DETERMINISTIC_GUARD=0`.
- When disabled the guard logs a structured warning so that CI pipelines and dashboards can flag non-deterministic jobs.

## Evaluation Suite Integration

- Golden and canary suites force-enable the guard and emit a failing check if it is bypassed.
- Canary runs pin all evaluation seeds by calling the guard prior to dataset preparation, guaranteeing reproducible prompt sampling.
- CI hints remind contributors to run the suites with `NAESTRO_DETERMINISTIC_GUARD=1` so local results mirror the pipeline.
- Regression tests exercise deterministic toggling by asserting identical logits/hash digests across repeat runs when the guard is active.
