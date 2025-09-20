from __future__ import annotations

import pathlib
import sys
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

import pytest
from naestro.agents.roles import Role, Roles
from naestro.agents.schemas import Message


def test_roles_registry_handles_registration_and_builtin_roles() -> None:
    roles = Roles()
    builtin_names = {role.name for role in roles.builtin}
    assert {"analyst", "research", "risk"} <= builtin_names

    def reviewer(history: Sequence[Message]) -> str:
        return f"reviewed-{len(history)}"

    review_role = Role(
        name="review",
        description="Evaluates proposed trades",
        strategy=reviewer,
        metadata={"team": "ops"},
    )
    roles.register(review_role)

    retrieved = roles.get("review")
    assert retrieved.respond(()) == "reviewed-0"

    roles.update_metadata("review", {"priority": "high"})
    updated = roles.get("review")
    assert updated.metadata["team"] == "ops"
    assert updated.metadata["priority"] == "high"

    def unstable(history: Sequence[Message]) -> str:
        raise RuntimeError("boom")

    fallback = Role(
        name="fallback",
        description="Uses fallback when strategy errors",
        strategy=unstable,
        fallback_response="fallback-response",
    )
    roles.register(fallback)
    assert roles.get("fallback").respond(()) == "fallback-response"

    roles.unregister("fallback")
    with pytest.raises(KeyError):
        roles.get("fallback")

    roles.clear()
    assert {role.name for role in roles.list()} == {role.name for role in roles.builtin}
