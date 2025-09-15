"""Common text-to-speech interface."""

from __future__ import annotations

import os
from typing import Callable, Iterable

from .tts_azure import synthesize as azure_synthesize
from .tts_elevenlabs import synthesize as elevenlabs_synthesize
from .tts_piper import synthesize as piper_synthesize
from .tts_playht import synthesize as playht_synthesize
from .tts_riva import synthesize as riva_synthesize

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
    defaults to ``"riva"``.
    """
    provider = os.getenv("TTS_PROVIDER", "riva").lower()
    synth = _TTS_PROVIDERS.get(provider)
    if synth is None:
        raise ValueError(f"Unsupported TTS provider: {provider}")
    return synth(text=text, voice=voice, style=style, stream=stream)
