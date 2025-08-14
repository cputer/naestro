"""
Copyright (c) 2025 CPUTER Inc.
SPDX-License-Identifier: MIT
Project Codename: NAESTRO (Orchestrator)
"""

from fastapi import FastAPI
import httpx, os

app = FastAPI(title="NAESTRO Gateway (CPUTER Inc.)")
ORCH = os.getenv("ORCH_URL","http://orchestrator:8081")

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/orchestrate")
async def orchestrate(task: dict):
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(f"{ORCH}/run", json=task)
        r.raise_for_status()
        return r.json()
