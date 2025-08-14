from fastapi import FastAPI
from typing import Dict

# Placeholder: wire actual LangGraph app here
app = FastAPI(title="NAESTRO Orchestrator")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run")
def run(task: Dict):
    # TODO: call planner -> implement -> verify -> refine workflow
    return {"ok": True, "echo": task}
