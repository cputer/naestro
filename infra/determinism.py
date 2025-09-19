"""Deterministic runtime helpers."""

from __future__ import annotations

import os
import random
from typing import Any

try:
    import numpy as _np  # type: ignore
except Exception:  # pragma: no cover - numpy optional
    _np = None  # type: ignore[assignment]


def _set_env_defaults(seed: int) -> None:
    os.environ["PYTHONHASHSEED"] = str(seed)
    os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":16:8")


def _seed_numpy(seed: int) -> None:
    if _np is None:
        return
    try:
        _np.random.seed(seed)
    except Exception:  # pragma: no cover - downstream library issues
        pass


def _seed_torch(seed: int, torch_det: bool) -> None:
    try:
        import torch  # type: ignore
    except Exception:  # pragma: no cover - torch optional
        return

    try:
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except Exception:  # pragma: no cover - defensive
        pass

    if not torch_det:
        return

    try:
        torch.use_deterministic_algorithms(True)  # type: ignore[attr-defined]
    except Exception:  # pragma: no cover - older torch versions
        pass

    backends: Any = getattr(torch, "backends", None)
    if backends is None:
        return

    cudnn = getattr(backends, "cudnn", None)
    if cudnn is not None:
        try:
            cudnn.deterministic = True  # type: ignore[attr-defined]
            cudnn.benchmark = False  # type: ignore[attr-defined]
        except Exception:  # pragma: no cover - defensive
            pass
        if hasattr(cudnn, "allow_tf32"):
            try:
                cudnn.allow_tf32 = False  # type: ignore[attr-defined]
            except Exception:  # pragma: no cover - defensive
                pass

    cuda_backend = getattr(backends, "cuda", None)
    if cuda_backend is not None:
        matmul = getattr(cuda_backend, "matmul", None)
        if matmul is not None and hasattr(matmul, "allow_tf32"):
            try:
                matmul.allow_tf32 = False  # type: ignore[attr-defined]
            except Exception:  # pragma: no cover - defensive
                pass


def enable(seed: int = 0, torch_det: bool = True) -> None:
    """Enable deterministic execution for Python, NumPy, and PyTorch."""

    _set_env_defaults(seed)
    random.seed(seed)
    _seed_numpy(seed)
    _seed_torch(seed, torch_det)


__all__ = ["enable"]
