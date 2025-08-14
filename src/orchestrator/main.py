from fastapi import FastAPI
from typing import Dict

app = FastAPI(title="NAESTRO Orchestrator")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run")
def run(task: Dict):
    # TODO: plug in LangGraph workflow (planner -> implement -> verify -> refine -> review)
    return {"ok": True, "echo": task}
