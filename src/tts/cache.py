"""Caching and policy enforcement for text-to-speech outputs."""

from __future__ import annotations

import hashlib
import io
import os
import wave
from dataclasses import dataclass
from typing import Dict, Optional

_CACHE: Dict[str, bytes] = {}


def fingerprint(text: str, voice: str, style: str | None) -> str:
    """Return a stable fingerprint for a synthesis request."""
    h = hashlib.sha256()
    h.update(text.encode("utf-8"))
    h.update(b"\0")
    h.update(voice.encode("utf-8"))
    h.update(b"\0")
    h.update((style or "").encode("utf-8"))
    return h.hexdigest()


def get(text: str, voice: str, style: str | None) -> Optional[bytes]:
    """Retrieve cached audio if present."""
    return _CACHE.get(fingerprint(text, voice, style))


def set(text: str, voice: str, style: str | None, audio: bytes) -> None:
    """Store audio in the cache."""
    _CACHE[fingerprint(text, voice, style)] = audio


def audio_seconds(audio: bytes) -> float:
    """Best-effort estimation of audio duration in seconds."""
    try:
        with wave.open(io.BytesIO(audio)) as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            return frames / float(rate)
    except Exception:
        sample_rate = int(os.getenv("TTS_SAMPLE_RATE", "22050"))
        sample_width = int(os.getenv("TTS_SAMPLE_WIDTH", "2"))
        return len(audio) / (sample_rate * sample_width)


@dataclass
class PolicyEngine:
    """Simple policy engine tracking synthesized audio duration."""

    max_seconds: float
    used_seconds: float = 0.0

    def consume(self, seconds: float) -> None:
        """Consume ``seconds`` from the remaining allowance."""
        if self.used_seconds + seconds > self.max_seconds:
            raise RuntimeError(
                f"TTS limit exceeded: {self.used_seconds + seconds:.2f}s > {self.max_seconds:.2f}s"
            )
        self.used_seconds += seconds


policy = PolicyEngine(float(os.getenv("TTS_MAX_SECONDS", "60")))

__all__ = [
    "get",
    "set",
    "audio_seconds",
    "policy",
    "fingerprint",
]
