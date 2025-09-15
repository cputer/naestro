"""Helpers for chunked audio streaming."""

from __future__ import annotations

from typing import Iterable, Iterator, Union


def chunk_audio(data: Union[bytes, bytearray, Iterable[bytes]], chunk_size: int = 4096) -> Iterator[bytes]:
    """Yield ``data`` in fixed-size chunks.

    Args:
        data: Raw audio bytes or an iterable producing byte chunks.
        chunk_size: Maximum size of yielded chunks.
    """
    if isinstance(data, (bytes, bytearray)):
        for i in range(0, len(data), chunk_size):
            yield data[i : i + chunk_size]
    else:
        for part in data:
            for i in range(0, len(part), chunk_size):
                yield part[i : i + chunk_size]
