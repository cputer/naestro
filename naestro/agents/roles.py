"""Deterministic debate roles and builtin strategies."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, Iterable, Iterator, Mapping, Sequence

from .schemas import Message

Responder = Callable[[Sequence[Message]], str]


def _analyst_strategy(history: Sequence[Message]) -> str:
    """Baseline analyst strategy used in the TradingAgents prompt."""

    if not history:
        return "Monitoring market context."
    prompt = history[0].content.lower()
    if "breakout" in prompt or "momentum" in prompt:
        return "Bullish breakout detected; recommend long bias."
    if "breakdown" in prompt or "sell-off" in prompt:
        return "Bearish pressure noted; avoid aggressive longs."
    return "No clear signal; continue observing levels."


def _research_strategy(history: Sequence[Message]) -> str:
    """Research role that balances bullish and bearish evidence."""

    approvals = sum(
        1
        for message in history
        if message.role != "system" and "bull" in message.content.lower()
    )
    rejections = sum(
        1
        for message in history
        if message.role != "system" and "bear" in message.content.lower()
    )
    if approvals > rejections:
        return "Bull case stronger; advocate for participation."
    if rejections > approvals:
        return "Bear case dominant; recommend patience."
    return "Arguments balanced; request additional clarification."


def _risk_strategy(history: Sequence[Message]) -> str:
    """Risk strategy enforcing conservative execution guard rails."""

    caution_signals = sum(
        1
        for message in history
        if "reject" in message.content.lower()
        or "avoid" in message.content.lower()
        or "risk" in message.content.lower()
    )
    if caution_signals:
        return "Risk elevated; reject trade for now."
    approvals = sum(
        1
        for message in history
        if "approve" in message.content.lower() or "proceed" in message.content.lower()
    )
    if approvals >= 2:
        return "Risk acceptable; proceed with defined sizing."
    return "Maintain neutral stance until conviction improves."


@dataclass(slots=True)
class Role:
    """Represents a deterministic debate participant."""

    name: str
    description: str
    strategy: Responder
    fallback_response: str = "I have nothing further to add."
    metadata: Mapping[str, object] = field(default_factory=dict)

    def respond(self, history: Sequence[Message]) -> str:
        """Compute a response using the role's strategy."""

        try:
            return self.strategy(history)
        except Exception:
            return self.fallback_response


def _build_builtin_roles() -> Dict[str, Role]:
    """Create the builtin deterministic roles."""

    analyst = Role(
        name="analyst",
        description="Synthesises market data into a directional bias.",
        strategy=_analyst_strategy,
        metadata={"team": "research"},
    )
    researcher = Role(
        name="research",
        description="Balances bullish and bearish research perspectives.",
        strategy=_research_strategy,
        metadata={"team": "research"},
    )
    risk = Role(
        name="risk",
        description="Enforces guard rails before execution.",
        strategy=_risk_strategy,
        metadata={"team": "risk"},
    )
    return {role.name: role for role in (analyst, researcher, risk)}


_BUILTIN_ROLES = _build_builtin_roles()


class Roles(Mapping[str, Role]):
    """Mapping of available roles seeded with the TradingAgents defaults."""

    def __init__(self, roles: Iterable[Role] | None = None) -> None:
        self._roles: Dict[str, Role] = dict(_BUILTIN_ROLES)
        if roles is not None:
            for role in roles:
                self.register(role)

    def __getitem__(self, key: str) -> Role:
        return self._roles[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._roles)

    def __len__(self) -> int:
        return len(self._roles)

    def register(self, role: Role) -> None:
        """Register or replace a role."""

        self._roles[role.name] = role

    def unregister(self, name: str) -> None:
        """Remove a role by name if present."""

        self._roles.pop(name, None)

    def update_metadata(self, name: str, metadata: Mapping[str, object]) -> None:
        """Merge metadata into an existing role definition."""

        role = self.get(name)
        combined: Dict[str, object] = dict(role.metadata)
        combined.update(metadata)
        self._roles[name] = Role(
            name=role.name,
            description=role.description,
            strategy=role.strategy,
            fallback_response=role.fallback_response,
            metadata=combined,
        )

    def get(self, name: str) -> Role:
        """Lookup a role by name raising a helpful error when missing."""

        try:
            return self._roles[name]
        except KeyError as exc:  # pragma: no cover - helpful error message
            raise KeyError(f"Unknown role '{name}'") from exc

    def list(self) -> Sequence[Role]:
        """Return the available roles preserving registration order."""

        return list(self._roles.values())

    def clear(self) -> None:
        """Reset the role mapping to the builtin defaults."""

        self._roles = dict(_BUILTIN_ROLES)

    @property
    def builtin(self) -> Sequence[Role]:
        """Return the builtin deterministic roles."""

        return [self._roles[name] for name in _BUILTIN_ROLES]

    @property
    def names(self) -> Sequence[str]:
        """Return the names of registered roles."""

        return list(self._roles.keys())


__all__ = ["Responder", "Role", "Roles"]
