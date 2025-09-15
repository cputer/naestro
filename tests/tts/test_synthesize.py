import sys
from pathlib import Path

# Ensure src/ directory is on sys.path for imports like `tts_riva`
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

import pytest

import tts
from tts import metrics as tts_metrics
from tts import cache as tts_cache


@pytest.fixture(autouse=True)
def reset_state():
    # Clear cache and reset metrics/policy before each test
    tts_cache._CACHE.clear()
    tts_cache.policy.used_seconds = 0
    tts_metrics.tts_latency_ms.reset()
    tts_metrics.tts_chars.reset()
    tts_metrics.provider.reset()
    tts_metrics.stream_gaps.reset()


def test_synthesize_streaming_cache_and_metrics(monkeypatch):
    monkeypatch.setenv("TTS_PROVIDER", "riva")
    calls = []

    def fake_provider(*, text, voice, style, stream):
        assert stream is True
        calls.append(text)
        return [b"foo", b"bar"]

    monkeypatch.setitem(tts._TTS_PROVIDERS, "riva", fake_provider)

    def fake_chunk_audio(data, chunk_size=4096):
        if isinstance(data, (bytes, bytearray)):
            yield data
        else:
            first = True
            for part in data:
                yield part
                if first:
                    # Insert an empty chunk to simulate a gap
                    yield b""
                    first = False

    monkeypatch.setattr(tts, "chunk_audio", fake_chunk_audio)

    times = iter([0.0, 0.1, 0.2, 0.3])
    monkeypatch.setattr(tts.time, "perf_counter", lambda: next(times))

    # Cache miss with streaming and gap
    result1 = tts.synthesize("hello", "v", None, stream=True)
    chunks1 = list(result1)
    assert b"".join(chunks1) == b"foobar"
    assert calls == ["hello"]
    assert tts_metrics.provider.get("riva") == 1
    assert tts_metrics.tts_chars.get("riva") == len("hello")
    assert tts_metrics.stream_gaps.get("riva") == 1
    assert tts_metrics.tts_latency_ms.get("riva") == pytest.approx(100.0)

    # Cache hit should not invoke provider
    result2 = tts.synthesize("hello", "v", None, stream=True)
    chunks2 = list(result2)
    assert b"".join(chunks2) == b"foobar"
    assert calls == ["hello"]
    assert tts_metrics.provider.get("riva") == 2
    assert tts_metrics.tts_chars.get("riva") == 2 * len("hello")
    # stream_gaps only counted for the miss
    assert tts_metrics.stream_gaps.get("riva") == 1
    # Latency updated on cache hit
    assert tts_metrics.tts_latency_ms.get("riva") == pytest.approx(100.0)


def test_synthesize_non_streaming_cache_and_metrics(monkeypatch):
    monkeypatch.setenv("TTS_PROVIDER", "riva")
    calls = []

    def fake_provider(*, text, voice, style, stream):
        assert stream is False
        calls.append(text)
        return b"baz"

    monkeypatch.setitem(tts._TTS_PROVIDERS, "riva", fake_provider)

    times = iter([0.0, 0.2, 0.3, 0.4])
    monkeypatch.setattr(tts.time, "perf_counter", lambda: next(times))

    # Cache miss
    audio1 = tts.synthesize("hello", "v", None, stream=False)
    assert audio1 == b"baz"
    assert calls == ["hello"]
    assert tts_metrics.provider.get("riva") == 1
    assert tts_metrics.tts_chars.get("riva") == len("hello")
    assert tts_metrics.stream_gaps.get("riva") == 0
    assert tts_metrics.tts_latency_ms.get("riva") == pytest.approx(200.0)

    # Cache hit
    audio2 = tts.synthesize("hello", "v", None, stream=False)
    assert audio2 == b"baz"
    assert calls == ["hello"]
    assert tts_metrics.provider.get("riva") == 2
    assert tts_metrics.tts_chars.get("riva") == 2 * len("hello")
    assert tts_metrics.stream_gaps.get("riva") == 0
    assert tts_metrics.tts_latency_ms.get("riva") == pytest.approx(100.0)
