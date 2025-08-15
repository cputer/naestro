"""FastAPI entrypoint for the LangGraph-based orchestrator."""

import os
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .orchestrator import app as workflow_app


app = FastAPI(title="NAESTRO Orchestrator")


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

    try:
        model_url = _route_model(task.model)
        state: Dict[str, Any] = {"input": task.input, "model_url": model_url}
        result = workflow_app.invoke(state)
        return RunResponse(result=result)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
