"""Adapter for NVIDIA Riva text-to-speech."""

from __future__ import annotations

import os
from typing import Iterable

try:
    from riva.client import Auth, SpeechSynthesisClient
except Exception:  # pragma: no cover - optional dependency
    Auth = None
    SpeechSynthesisClient = None


def synthesize(
    text: str, voice: str, style: str | None, stream: bool = True
) -> Iterable[bytes] | bytes:
    """Synthesize ``text`` into speech using Riva.

    Args:
        text: The text to convert.
        voice: Voice name to use.
        style: Optional speaking style.
        stream: When ``True`` yield audio chunks, otherwise return full audio bytes.
    """
    if SpeechSynthesisClient is None or Auth is None:
        raise RuntimeError("riva.client is required for Riva TTS")

    server = os.getenv("RIVA_TTS_URL", "localhost:50051")
    auth = Auth(server)
    client = SpeechSynthesisClient(server, auth=auth, use_ssl=False)

    if stream:
        for response in client.synthesize_streaming(
            text, voice_name=voice, speaking_style=style
        ):
            yield response.audio
    else:
        resp = client.synthesize(text, voice_name=voice, speaking_style=style)
        return resp.audio
