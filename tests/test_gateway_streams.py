import asyncio

from starlette.websockets import WebSocketDisconnect

from src.gateway import main as gw


def test_kpi_metrics_single_latency():
    gw.REQUEST_LATENCIES[:] = [100.0]
    gw.REQUEST_COUNT = 1
    kpis = gw._kpi_metrics()
    assert kpis.latency_p95_ms == 100.0


def test_telemetry_event():
    gw.REQUEST_LATENCIES[:] = []
    gw.REQUEST_COUNT = 0
    event = gw._telemetry_event()
    assert event.system.cpu_percent >= 0


def test_websocket_endpoint_iteration(monkeypatch):
    gw.REQUEST_LATENCIES[:] = []
    gw.REQUEST_COUNT = 0

    events = []

    class DummyWebSocket:
        async def accept(self):
            pass

        async def send_json(self, data):
            events.append(data)
            if len(events) >= 2:
                raise WebSocketDisconnect()

        async def close(self):
            pass

    async def fast_sleep(_):
        return None

    monkeypatch.setattr(asyncio, "sleep", fast_sleep)

    async def run():
        await asyncio.wait_for(gw.websocket_endpoint(DummyWebSocket()), timeout=0.1)

    asyncio.run(run())
    assert len(events) == 2


def test_sse_event_generator(monkeypatch):
    async def fast_sleep(_):
        return None

    monkeypatch.setattr(asyncio, "sleep", fast_sleep)

    async def run():
        resp = await asyncio.wait_for(gw.sse_endpoint(), timeout=0.1)
        gen = resp.body_iterator
        first = await asyncio.wait_for(gen.__anext__(), timeout=0.1)
        assert first.startswith("data: ")
        second = await asyncio.wait_for(gen.__anext__(), timeout=0.1)
        assert second.startswith("data: ")
        await gen.aclose()

    asyncio.run(run())
