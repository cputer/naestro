from fastapi import FastAPI
from typing import Dict

app = FastAPI(title="NAESTRO Orchestrator")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run")
def run(task: Dict):
    # TODO: integrate LangGraph workflow (Plan -> Implement -> Verify -> Refine -> Review)
    # TODO: route to SLM/NIM/vLLM based on policy
    return {"ok": True, "echo": task}
