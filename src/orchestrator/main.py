"""FastAPI entrypoint for the LangGraph-based orchestrator."""

import logging
import os
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .math_agent import app as math_app
from .orchestrator import app as workflow_app

app = FastAPI(title="NAESTRO Orchestrator")


# Guardrail stubs -----------------------------------------------------------


def thermal_guard() -> None:
    """Reduce concurrency and emit incidents when temperature exceeds 78°C."""

    temp_c = 70  # TODO: replace with real temperature telemetry
    if temp_c >= 78:
        # TODO: integrate concurrency throttling and incident emission
        logging.warning("Thermal guard triggered at %s°C", temp_c)


def oom_guard() -> None:
    """Reroute workload to cloud on OOM with incident logging."""

    # TODO: detect OOM conditions and reroute traffic to the cloud
    logging.error("OOM guard activated; rerouting to cloud")


def backpressure_guard(p95_paint_ms: float) -> None:
    """Coalesce updates when UI paint P95 exceeds 500 ms."""

    # TODO: integrate with real paint metrics and coalescing logic
    if p95_paint_ms > 500:
        logging.info("Backpressure guard engaged at %sms", p95_paint_ms)


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
        backpressure_guard(p95_paint_ms=0)  # TODO: supply real paint metric
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
