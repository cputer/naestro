"""Adapter for ElevenLabs text-to-speech."""

from __future__ import annotations

import os
from typing import Iterable

import requests


def synthesize(
    text: str, voice: str, style: str | None, stream: bool = True
) -> Iterable[bytes] | bytes:
    """Synthesize ``text`` into speech using ElevenLabs.

    The adapter is guarded by the ``ENABLE_ELEVENLABS`` feature flag. Set
    ``ELEVENLABS_API_KEY`` to the API key.
    """
    if not os.getenv("ENABLE_ELEVENLABS"):
        raise RuntimeError("ElevenLabs TTS is disabled")

    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is not set")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"
    headers = {"xi-api-key": api_key}
    payload: dict[str, object] = {"text": text}
    if style:
        payload["voice_settings"] = {"style": style}

    response = requests.post(url, headers=headers, json=payload, stream=stream)
    response.raise_for_status()

    if stream:
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                yield chunk
    else:
        return response.content
