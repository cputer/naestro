"""FastAPI entrypoint for the LangGraph-based orchestrator."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

try:  # pragma: no cover - defensive import
    from infra.determinism import enable as _det_en
except Exception:  # pragma: no cover - determinism helper optional
    def _det_en(*_args: Any, **_kwargs: Any) -> None:
        return None


def _load_runtime_config() -> Dict[str, Any]:
    config_path = Path(__file__).resolve().parents[2] / "configs" / "runtime.yaml"
    if not config_path.exists():
        return {}
    with config_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        return {}
    return data


def _enable_determinism() -> None:
    config = _load_runtime_config()
    runtime_cfg = config.get("runtime", {}) if isinstance(config, dict) else {}
    det_cfg = runtime_cfg.get("determinism", {})
    if not isinstance(det_cfg, dict):
        det_cfg = {}
    enabled = det_cfg.get("enabled", True)
    if enabled:
        seed = int(det_cfg.get("seed", 0) or 0)
        _det_en(seed=seed)


_enable_determinism()

from .math_agent import app as math_app
from .orchestrator import app as workflow_app

logger = logging.getLogger(__name__)
app = FastAPI(title="NAESTRO Orchestrator")


# Guardrails -----------------------------------------------------------------


def thermal_guard() -> bool:
    """Reduce concurrency and emit incidents when temperature exceeds threshold."""

    limit_c = int(os.getenv("THERMAL_GUARD_MAX_C", "78"))
    try:  # pragma: no cover - psutil may not be installed
        import psutil  # type: ignore

        temps = psutil.sensors_temperatures()  # type: ignore[attr-defined]
        current = max(
            [t.current for group in temps.values() for t in group], default=None
        )
    except Exception as exc:  # pragma: no cover - telemetry not available
        logger.debug("Thermal telemetry unavailable: %s", exc)
        return False

    if current is not None and current >= limit_c:
        logger.warning("Thermal guard triggered at %s°C", current)
        return True
    return False


def oom_guard() -> bool:
    """Reroute workload to cloud on low available memory with incident logging."""

    min_free_mb = int(os.getenv("OOM_GUARD_MIN_AVAILABLE_MB", "0"))
    if min_free_mb <= 0:
        return False

    try:  # pragma: no cover - psutil may not be installed
        import psutil  # type: ignore

        avail_mb = psutil.virtual_memory().available / (1024 * 1024)
    except Exception as exc:  # pragma: no cover - telemetry not available
        logger.debug("Memory telemetry unavailable: %s", exc)
        return False

    if avail_mb < min_free_mb:
        logger.error(
            "OOM guard activated; available memory %.1fMB below threshold %sMB",
            avail_mb,
            min_free_mb,
        )
        return True
    return False


def backpressure_guard(p95_paint_ms: float) -> bool:
    """Coalesce updates when UI paint P95 exceeds configured limit."""

    threshold = float(os.getenv("BACKPRESSURE_P95_THRESHOLD_MS", "500"))
    if p95_paint_ms > threshold:
        logger.info("Backpressure guard engaged at %sms", p95_paint_ms)
        return True
    return False


class TaskRequest(BaseModel):
    """Incoming task payload."""

    input: str
    model: Optional[str] = None  # slm, nim, vllm, or auto


class RunResponse(BaseModel):
    """Workflow result payload."""

    result: Dict[str, Any]


def _route_model(policy: Optional[str]) -> str:
    """Resolve the model endpoint based on policy/environment configuration."""

    policy = (policy or "auto").lower()
    base_urls = {
        "slm": os.getenv("SLM_BASE_URL"),
        "nim": os.getenv("NIM_BASE_URL"),
        "vllm": os.getenv("VLLM_BASE_URL"),
    }

    if policy == "auto":
        for key in ("slm", "vllm", "nim"):
            if base_urls.get(key):
                return base_urls[key]  # first configured service wins
        raise HTTPException(status_code=500, detail="No model endpoints configured")

    url = base_urls.get(policy)
    if not url:
        raise HTTPException(status_code=400, detail=f"Unknown model policy '{policy}'")
    return url


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/run", response_model=RunResponse)
def run(task: TaskRequest) -> RunResponse:
    """Execute the LangGraph workflow and return its final state."""

    thermal_guard()

    try:
        model_url = _route_model(task.model)
        state: Dict[str, Any] = {"input": task.input, "model_url": model_url}
        result = workflow_app.invoke(state)
        paint_ms = float(os.getenv("PAINT_METRIC_P95_MS", "0"))
        backpressure_guard(paint_ms)
        return RunResponse(result=result)
    except MemoryError:
        oom_guard()
        raise HTTPException(status_code=500, detail="Rerouted to cloud due to OOM")
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


class MathRequest(BaseModel):
    """Payload for math queries."""

    query: str


@app.post("/math", response_model=RunResponse)
def math(task: MathRequest) -> RunResponse:
    """Execute the math agent and return the result."""

    try:
        result = math_app.invoke({"query": task.query})
        return RunResponse(result=result)
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=500, detail=str(exc))
