import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

import io
import types
import wave

import pytest

import tts
import tts_azure
import tts_playht
import tts_piper
import tts_elevenlabs
import tts_riva
from tts.streaming import chunk_audio
from tts.cache import audio_seconds, PolicyEngine


def _run(gen):
    """Exhaust a generator and return its final value."""
    try:
        while True:
            next(gen)
    except StopIteration as e:  # pragma: no cover - control flow
        return e.value


def test_stub_adapters_not_implemented():
    for mod in (tts_azure, tts_playht, tts_piper):
        with pytest.raises(NotImplementedError):
            mod.synthesize("text", "voice", None)


def test_elevenlabs_disabled(monkeypatch):
    monkeypatch.delenv("ENABLE_ELEVENLABS", raising=False)
    gen = tts_elevenlabs.synthesize("hello", "v", None)
    with pytest.raises(RuntimeError):
        next(gen)


def test_elevenlabs_missing_key(monkeypatch):
    monkeypatch.setenv("ENABLE_ELEVENLABS", "1")
    monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
    gen = tts_elevenlabs.synthesize("hello", "v", None)
    with pytest.raises(RuntimeError):
        next(gen)


def test_elevenlabs_stream_and_non_stream(monkeypatch):
    monkeypatch.setenv("ENABLE_ELEVENLABS", "1")
    monkeypatch.setenv("ELEVENLABS_API_KEY", "key")

    class DummyResponse:
        def __init__(self, content=None, chunks=None):
            self.content = content
            self._chunks = chunks or []

        def raise_for_status(self):
            pass

        def iter_content(self, chunk_size=None):
            yield from self._chunks

    def fake_post(*args, **kwargs):
        return DummyResponse(chunks=[b"", b"a", b"b"])

    monkeypatch.setattr(tts_elevenlabs.requests, "post", fake_post)
    chunks = list(tts_elevenlabs.synthesize("hi", "v", "s", stream=True))
    assert chunks == [b"a", b"b"]

    def fake_post_nonstream(*args, **kwargs):
        return DummyResponse(content=b"data")

    monkeypatch.setattr(tts_elevenlabs.requests, "post", fake_post_nonstream)
    result = _run(tts_elevenlabs.synthesize("hi", "v", "s", stream=False))
    assert result == b"data"


def test_riva_requires_dependency():
    gen = tts_riva.synthesize("hi", "v", None)
    with pytest.raises(RuntimeError):
        next(gen)


def test_riva_stream_and_non_stream(monkeypatch):
    class DummyAuth:
        def __init__(self, server):
            self.server = server

    class DummyClient:
        def __init__(self, server, auth=None, use_ssl=False):
            self.server = server

        def synthesize_streaming(self, text, voice_name=None, speaking_style=None):
            yield types.SimpleNamespace(audio=b"a")
            yield types.SimpleNamespace(audio=b"b")

        def synthesize(self, text, voice_name=None, speaking_style=None):
            return types.SimpleNamespace(audio=b"c")

    monkeypatch.setattr(tts_riva, "Auth", DummyAuth)
    monkeypatch.setattr(tts_riva, "SpeechSynthesisClient", DummyClient)

    chunks = list(tts_riva.synthesize("hi", "v", None, stream=True))
    assert chunks == [b"a", b"b"]

    result = _run(tts_riva.synthesize("hi", "v", None, stream=False))
    assert result == b"c"


def test_tts_unknown_provider(monkeypatch):
    monkeypatch.setenv("TTS_PROVIDER", "unknown")
    with pytest.raises(ValueError):
        tts.synthesize("x", "v", None)


def test_audio_seconds(monkeypatch):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(10)
        wf.writeframes(b"\0\0" * 10)
    data = buf.getvalue()
    assert audio_seconds(data) == pytest.approx(1.0)

    monkeypatch.setenv("TTS_SAMPLE_RATE", "2")
    monkeypatch.setenv("TTS_SAMPLE_WIDTH", "1")
    assert audio_seconds(b"1234") == 2.0


def test_policy_engine_limit():
    engine = PolicyEngine(1.0)
    engine.consume(0.5)
    with pytest.raises(RuntimeError):
        engine.consume(0.6)


def test_chunk_audio():
    assert list(chunk_audio(b"abcdef", 2)) == [b"ab", b"cd", b"ef"]
    iterable_chunks = list(chunk_audio([b"abc", b"de"], 2))
    assert iterable_chunks == [b"ab", b"c", b"de"]
