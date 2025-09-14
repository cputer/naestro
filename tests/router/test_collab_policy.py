import pytest

from router.collab_policy import CollaborationMode
from router.router import Router


def test_solo_only_allows_one_agent():
    router = Router(CollaborationMode.SOLO)
    assert router.route(["alice"]) == ["alice"]
    with pytest.raises(ValueError):
        router.route(["alice", "bob"])


def test_consult_allows_two_agents_but_not_three():
    router = Router(CollaborationMode.CONSULT)
    assert router.route(["alice", "bob"]) == ["alice", "bob"]
    with pytest.raises(ValueError):
        router.route(["alice", "bob", "carol"])


def test_collaborate_requires_at_least_two_agents():
    router = Router(CollaborationMode.COLLABORATE)
    with pytest.raises(ValueError):
        router.route(["alice"])
    assert router.route(["alice", "bob"]) == ["alice", "bob"]


def test_consensus_requires_at_least_two_agents():
    router = Router(CollaborationMode.CONSENSUS)
    with pytest.raises(ValueError):
        router.route(["alice"])
    assert router.route(["alice", "bob"]) == ["alice", "bob"]


def test_swarm_requires_three_agents():
    router = Router(CollaborationMode.SWARM)
    with pytest.raises(ValueError):
        router.route(["alice", "bob"])
    assert router.route(["alice", "bob", "carol"]) == ["alice", "bob", "carol"]
