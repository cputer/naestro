"""Telemetry metrics for text-to-speech synthesis."""

from __future__ import annotations

from src.telemetry import metrics as base_metrics

# Last latency per provider in milliseconds.
tts_latency_ms = base_metrics.LabeledGauge(
    "tts_latency_ms", "Last TTS synthesis latency in milliseconds per provider."
)

# Total characters synthesized per provider.
tts_chars = base_metrics.LabeledCounter(
    "tts_chars_total", "Total characters synthesized per provider."
)

# Number of requests made per provider.
provider = base_metrics.LabeledCounter(
    "tts_provider_total", "Number of TTS requests per provider."
)

# Detected gaps or anomalies during streaming per provider.
stream_gaps = base_metrics.LabeledCounter(
    "tts_stream_gaps_total", "Number of streaming gaps detected per provider."
)


def emit_metrics(provider_name: str, text: str, latency_ms: float, gaps: int) -> None:
    """Record basic TTS telemetry metrics."""
    provider.inc(provider_name)
    tts_latency_ms.set(provider_name, latency_ms)
    tts_chars.inc(provider_name, len(text))
    if gaps:
        stream_gaps.inc(provider_name, gaps)


__all__ = [
    "tts_latency_ms",
    "tts_chars",
    "provider",
    "stream_gaps",
    "emit_metrics",
]
