import asyncio
import os
import time

import httpx
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
from fastapi.responses import JSONResponse, StreamingResponse

app = FastAPI(title="NAESTRO Gateway")
ORCH = os.getenv("ORCH_URL", "http://orchestrator:8081")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/orchestrate")
async def orchestrate(task: dict):
    async with httpx.AsyncClient(timeout=120) as client:
        try:
            r = await client.post(f"{ORCH}/run", json=task)
            r.raise_for_status()
            return r.json()
        except httpx.RequestError:
            return JSONResponse(
                {"error": "orchestrator unreachable"}, status_code=502
            )


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket stream emitting heartbeats every 20 seconds."""

    await websocket.accept()
    try:
        while True:
            # TODO: replace heartbeat with real telemetry events
            await websocket.send_json({"heartbeat": time.time()})
            await asyncio.sleep(20)
    except WebSocketDisconnect:  # pragma: no cover - client disconnected
        pass
    finally:
        await websocket.close()


@app.get("/events")
async def sse_endpoint():
    """Server‑Sent Events fallback emitting heartbeats every 20 seconds."""

    async def event_generator():
        try:
            while True:
                # TODO: replace heartbeat with real telemetry events
                yield f'data: {{"heartbeat": {time.time()}}}\n\n'
                await asyncio.sleep(20)
        except asyncio.CancelledError:  # pragma: no cover - client disconnected
            return

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.get("/api/metrics/system")
def system_metrics():
    """Return mock system metrics."""

    # TODO: replace mock data with real system metrics
    return {"cpu": 0.42, "memory": 1234}


@app.get("/api/metrics/kpis")
def kpi_metrics():
    """Return mock KPI metrics."""

    # TODO: replace mock data with real KPI metrics
    return {"latency_p95_ms": 250, "throughput_rps": 99}
