from __future__ import annotations

import pytest

from src.voice import NullTTSAdapter, PiperTTSStub, TTSRequest, parse_ssml


@pytest.mark.parametrize("adapter_cls", [NullTTSAdapter, PiperTTSStub])
def test_streaming(adapter_cls):
    adapter = adapter_cls()
    text = "hello world " * 50
    req = TTSRequest(text=text)
    chunks = list(adapter.synthesize_stream(req))
    assert len(chunks) >= 2
    assert sum(len(c.data) for c in chunks) >= len(text)
    assert sum(1 for c in chunks if c.final) == 1
    seqs = [c.seq for c in chunks]
    assert seqs == sorted(seqs)


def test_ssml_parsing_with_null_adapter():
    ssml = (
        '<prosody rate="fast"><emphasis level="strong">hello'
        '</emphasis><break time="500ms"/></prosody>'
    )
    text, controls = parse_ssml(ssml)
    assert text == "hello"
    assert controls == {
        "prosody.rate": "fast",
        "emphasis.level": "strong",
        "break.ms": 500,
    }
    adapter = NullTTSAdapter()
    req = TTSRequest(text=ssml, ssml=True)
    data = b"".join(chunk.data for chunk in adapter.synthesize_stream(req))
    assert data.decode() == text


def test_piper_stub_requires_plain_text():
    ssml = '<emphasis level="moderate">hi there</emphasis>'
    text, _ = parse_ssml(ssml)
    adapter = PiperTTSStub()
    assert adapter.supports_ssml() is False
    req = TTSRequest(text=text)
    data = b"".join(chunk.data for chunk in adapter.synthesize_stream(req))
    assert data.decode() == text
