from fastapi import FastAPI, HTTPException
import os, httpx

app = FastAPI(title="NAESTRO Gateway")

NIM = os.getenv("NIM_BASE_URL", "http://nim:8000/v1")
VLLM = os.getenv("VLLM_BASE_URL", "http://vllm:8000/v1")
SLM = os.getenv("SLM_BASE_URL", "http://slm:8000/v1")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/orchestrate")
async def orchestrate(task: dict):
    # naive pass-through to orchestrator (internal)
    async with httpx.AsyncClient() as client:
        r = await client.post("http://orchestrator:8081/run", json=task, timeout=120)
        r.raise_for_status()
        return r.json()
