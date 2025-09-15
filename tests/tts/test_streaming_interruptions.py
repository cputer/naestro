from __future__ import annotations

import time

from src.voice import NullTTSAdapter, TTSRequest


def test_barge_in_interrupt():
    adapter = NullTTSAdapter()
    req = TTSRequest(text="hello world " * 100)
    start = time.monotonic()
    stream = adapter.synthesize_stream(req)
    data = bytearray()
    for i, chunk in enumerate(stream):
        data.extend(chunk.data)
        if i == 1:
            break
    elapsed = time.monotonic() - start
    assert elapsed < 0.25
    assert data


def test_full_stream_receives_final_chunk():
    adapter = NullTTSAdapter()
    req = TTSRequest(text="hello world " * 10)
    chunks = list(adapter.synthesize_stream(req))
    assert chunks[-1].final
