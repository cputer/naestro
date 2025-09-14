"""Utilities for composing prompts with collaboration headers.

This module exposes two helpers:

``add_collab_headers`` injects simple mode/depth tokens at the start of a
prompt.  The tokens use a ``<<cop.*>>`` scheme so downstream agents can parse
out collaboration preferences.

``choose_answer`` applies an answer aggregation strategy given a list of
responses.  Each response is expected to be a mapping with ``content`` and
``confidence`` keys.  The function supports three strategies:

* ``self_if_confident`` – use the first response if its confidence meets the
  threshold, otherwise aggregate all responses.
* ``aggregate_always`` – always aggregate all responses.
* ``ask_clarify_below_threshold`` – when the top confidence is below the
  threshold return the string ``"clarify"`` signalling that a clarifying
  question should be asked.  Otherwise aggregate the responses.

These behaviours are intentionally lightweight so they can be used in unit
tests without requiring any model calls.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping

from orchestrator.planner import clamp_prefs


def _aggregate(responses: Iterable[Mapping[str, Any]]) -> str:
    """Aggregate multiple model responses into a single string.

    Aggregation here is intentionally simple: join the ``content`` fields with
    newlines.  The helper lives outside of ``choose_answer`` purely to make the
    behaviour easy to test and to keep ``choose_answer`` small.
    """

    return "\n".join(str(r.get("content", "")) for r in responses)


def add_collab_headers(prompt: str, prefs: Mapping[str, Any]) -> str:
    """Inject collaboration mode/depth tokens into ``prompt``.

    Parameters
    ----------
    prompt:
        The base prompt text.
    prefs:
        Collaboration preferences.  Only ``mode`` and ``depth`` are used but
        the input is run through :func:`orchestrator.planner.clamp_prefs` so
        callers can supply partial or noisy data.
    """

    cfg = clamp_prefs(dict(prefs))
    mode = cfg["mode"]
    depth = cfg["depth"]
    header = f"<<cop.mode:{mode}>> <<cop.depth:{depth}>>"
    return f"{header}\n{prompt}"


def choose_answer(responses: List[Mapping[str, Any]], prefs: Mapping[str, Any]) -> str:
    """Return a final answer according to ``prefs``.

    The caller supplies a list of response mappings.  Each mapping should
    contain ``content`` and ``confidence`` keys.  ``prefs`` may contain an
    ``answer_strategy`` and ``confidence_threshold`` which control how the final
    answer is selected.
    """

    cfg = clamp_prefs(dict(prefs))
    strat = cfg["answer_strategy"]
    threshold = float(cfg["confidence_threshold"])

    if not responses:
        return ""

    top = responses[0]
    top_conf = float(top.get("confidence", 0.0))

    if strat == "aggregate_always":
        return _aggregate(responses)

    if strat == "self_if_confident":
        if top_conf >= threshold:
            return str(top.get("content", ""))
        return _aggregate(responses)

    if strat == "ask_clarify_below_threshold":
        if top_conf < threshold:
            return "clarify"
        return _aggregate(responses)

    # Fallback – aggregate everything.
    return _aggregate(responses)
