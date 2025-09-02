"""Gateway service exposing orchestration and telemetry APIs."""

import asyncio
import logging
import os
import statistics
import time
from typing import List

import httpx
from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.websockets import WebSocketDisconnect
from pydantic import BaseModel

app = FastAPI(title="NAESTRO Gateway")
ORCH = os.getenv("ORCH_URL", "http://orchestrator:8081")

logger = logging.getLogger(__name__)


class SystemMetrics(BaseModel):
    """CPU and memory usage sampled from the host system."""

    cpu_percent: float
    memory_mb: float


class KPIMetrics(BaseModel):
    """Application KPIs collected during runtime."""

    latency_p95_ms: float
    throughput_rps: float


class Telemetry(BaseModel):
    """Telemetry event emitted to streaming clients.

    Schema::
        {
            "timestamp": <float>,
            "system": {"cpu_percent": <float>, "memory_mb": <float>},
            "kpis": {"latency_p95_ms": <float>, "throughput_rps": <float>}
        }
    """

    timestamp: float
    system: SystemMetrics
    kpis: KPIMetrics


REQUEST_LATENCIES: List[float] = []
REQUEST_COUNT = 0
START_TIME = time.time()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/orchestrate")
async def orchestrate(task: dict):
    """Proxy task execution to the orchestrator."""

    global REQUEST_COUNT, REQUEST_LATENCIES
    start = time.perf_counter()
    async with httpx.AsyncClient(timeout=120) as client:
        try:
            r = await client.post(f"{ORCH}/run", json=task)
            r.raise_for_status()
            return r.json()
        except httpx.RequestError:
            return JSONResponse(
                {"error": "orchestrator unreachable"}, status_code=502
            )
        finally:
            duration_ms = (time.perf_counter() - start) * 1000
            REQUEST_LATENCIES.append(duration_ms)
            REQUEST_COUNT += 1


def _system_metrics() -> SystemMetrics:
    try:  # pragma: no cover - psutil may not be installed
        import psutil  # type: ignore

        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().used / (1024 * 1024)
        return SystemMetrics(cpu_percent=cpu, memory_mb=mem)
    except Exception as exc:  # pragma: no cover - telemetry not available
        logger.debug("System metrics unavailable: %s", exc)
        return SystemMetrics(cpu_percent=0.0, memory_mb=0.0)


def _kpi_metrics() -> KPIMetrics:
    p95 = 0.0
    if len(REQUEST_LATENCIES) >= 2:
        p95 = statistics.quantiles(
            REQUEST_LATENCIES, n=100, method="inclusive"
        )[94]
    elif REQUEST_LATENCIES:
        p95 = REQUEST_LATENCIES[0]
    elapsed = time.time() - START_TIME
    throughput = REQUEST_COUNT / elapsed if elapsed > 0 else 0.0
    return KPIMetrics(latency_p95_ms=p95, throughput_rps=throughput)


def _telemetry_event() -> Telemetry:
    return Telemetry(
        timestamp=time.time(),
        system=_system_metrics(),
        kpis=_kpi_metrics(),
    )


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket stream emitting system and KPI telemetry every 20 seconds."""

    await websocket.accept()
    try:
        while True:
            event = _telemetry_event()
            await websocket.send_json(event.model_dump())
            await asyncio.sleep(20)
    except WebSocketDisconnect:  # pragma: no cover - connection dropped
        pass
    except Exception:  # pragma: no cover - unexpected error
        logger.exception("WebSocket error")
    finally:
        await websocket.close()


@app.get("/events")
async def sse_endpoint():
    """Server‑Sent Events fallback emitting telemetry every 20 seconds."""

    async def event_generator():
        try:
            while True:
                event = _telemetry_event()
                yield f"data: {event.model_dump_json()}\n\n"
                await asyncio.sleep(20)
        except asyncio.CancelledError:  # pragma: no cover - client disconnected
            logger.debug("SSE client disconnected")

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.get("/api/metrics/system", response_model=SystemMetrics)
def system_metrics() -> SystemMetrics:
    """Return current CPU and memory usage."""

    return _system_metrics()


@app.get("/api/metrics/kpis", response_model=KPIMetrics)
def kpi_metrics() -> KPIMetrics:
    """Return runtime KPI statistics."""

    return _kpi_metrics()
