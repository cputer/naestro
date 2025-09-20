"""Simple role registry used by the orchestrator and trading packs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Iterable, List, Mapping, MutableMapping, Sequence

from naestro.core.schemas import Message

Responder = Callable[[Sequence[Message]], str]


@dataclass(slots=True)
class Role:
    """Represents a participant in a debate."""

    name: str
    description: str
    strategy: Responder
    fallback_response: str = "I have nothing further to add."
    metadata: Mapping[str, object] = field(default_factory=dict)

    def respond(self, history: Sequence[Message]) -> str:
        """Compute a response from the role given the conversation history."""

        try:
            response = self.strategy(history)
        except Exception:  # pragma: no cover - defensive fallback
            response = self.fallback_response
        return response


class RoleRegistry:
    """In-memory registry for role definitions."""

    def __init__(self, roles: Iterable[Role] | None = None) -> None:
        self._roles: Dict[str, Role] = {}
        if roles is not None:
            for role in roles:
                self.register(role)

    def register(self, role: Role) -> None:
        self._roles[role.name] = role

    def unregister(self, name: str) -> None:
        self._roles.pop(name, None)

    def get(self, name: str) -> Role:
        try:
            return self._roles[name]
        except KeyError as exc:  # pragma: no cover - ensures helpful error message
            raise KeyError(f"Unknown role '{name}'") from exc

    def update_metadata(self, name: str, metadata: Mapping[str, object]) -> None:
        role = self.get(name)
        combined: MutableMapping[str, object] = dict(role.metadata)
        combined.update(metadata)
        self._roles[name] = Role(
            name=role.name,
            description=role.description,
            strategy=role.strategy,
            fallback_response=role.fallback_response,
            metadata=dict(combined),
        )

    def list(self) -> List[Role]:
        return list(self._roles.values())

    def clear(self) -> None:
        self._roles.clear()


__all__ = ["Role", "RoleRegistry", "Responder"]
