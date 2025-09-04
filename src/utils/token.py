"""Token-related helper functions."""

from __future__ import annotations


def round_tokens(tokens: float) -> int:
    """Round a floating point token count to the nearest integer.

    This follows the common "round half up" strategy, where values ending in
    ``.5`` are rounded up rather than to the nearest even number.
    """
    return int(tokens + 0.5)
