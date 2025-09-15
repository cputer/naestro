"""Common text-to-speech interface with caching and streaming helpers."""

from __future__ import annotations

import os
import time
from typing import Callable, Iterable, Iterator

from tts_azure import synthesize as azure_synthesize
from tts_elevenlabs import synthesize as elevenlabs_synthesize
from tts_piper import synthesize as piper_synthesize
from tts_playht import synthesize as playht_synthesize
from tts_riva import synthesize as riva_synthesize

from .cache import audio_seconds, get as cache_get, policy, set as cache_set
from .streaming import chunk_audio
from .metrics import emit_metrics

_TTS_PROVIDERS: dict[
    str, Callable[[str, str, str | None, bool], Iterable[bytes] | bytes]
] = {
    "riva": riva_synthesize,
    "elevenlabs": elevenlabs_synthesize,
    "azure": azure_synthesize,
    "playht": playht_synthesize,
    "piper": piper_synthesize,
}


def synthesize(text: str, voice: str, style: str | None, stream: bool = True):
    """Synthesize speech using the provider defined by ``TTS_PROVIDER``.

    The provider name is read from the ``TTS_PROVIDER`` environment variable and
    defaults to ``"riva"``.  Results are cached based on ``text``, ``voice`` and
    ``style``.  The :mod:`tts.cache` policy engine is consulted to ensure the
    total seconds of synthesized audio do not exceed the allowed limit for the
    current run.
    """
    provider = os.getenv("TTS_PROVIDER", "riva").lower()
    synth = _TTS_PROVIDERS.get(provider)
    if synth is None:
        raise ValueError(f"Unsupported TTS provider: {provider}")

    start = time.perf_counter()
    cached = cache_get(text, voice, style)
    if cached is not None:
        seconds = audio_seconds(cached)
        policy.consume(seconds)
        latency_ms = (time.perf_counter() - start) * 1000
        emit_metrics(provider, text, latency_ms, 0)
        if stream:
            return chunk_audio(cached)
        return cached

    if stream:
        provider_stream = synth(text=text, voice=voice, style=style, stream=True)

        def _generator() -> Iterator[bytes]:
            buffer = bytearray()
            gaps = 0
            for chunk in chunk_audio(provider_stream):
                if not chunk:
                    gaps += 1
                    continue
                buffer.extend(chunk)
                yield chunk
            audio = bytes(buffer)
            seconds = audio_seconds(audio)
            policy.consume(seconds)
            cache_set(text, voice, style, audio)
            latency_ms = (time.perf_counter() - start) * 1000
            emit_metrics(provider, text, latency_ms, gaps)

        return _generator()
    else:
        audio = synth(text=text, voice=voice, style=style, stream=False)
        seconds = audio_seconds(audio)
        policy.consume(seconds)
        cache_set(text, voice, style, audio)
        latency_ms = (time.perf_counter() - start) * 1000
        emit_metrics(provider, text, latency_ms, 0)
        return audio


__all__ = ["synthesize"]
