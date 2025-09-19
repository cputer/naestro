"""Unit tests for the HICRA credit assignment helpers."""
import pytest
import torch

from src.telemetry.metrics import (
    hicra_depth,
    hicra_planner_reward_ratio,
    hicra_success,
)
from src.training.hicra import HICRAConfig, HICRACreditAssigner, build_hicra_from_dict


def test_hicra_multiplier_scaling() -> None:
    assigner = HICRACreditAssigner(HICRAConfig(multiplier=2.5))
    rewards = torch.tensor([[1.0, -2.0], [0.5, 0.0]])

    credits = assigner.assign_credit(rewards)

    expected = rewards * 2.5
    assert torch.allclose(credits, expected)


def test_hicra_disabled_returns_zeros() -> None:
    assigner = HICRACreditAssigner(HICRAConfig(enabled=False, multiplier=10.0))
    rewards = torch.tensor([[1.0, 2.0, 3.0]])
    mask = torch.tensor([[True, False, True]])

    credits = assigner.assign_credit(rewards, mask=mask)

    assert torch.equal(credits, torch.zeros_like(rewards))


def test_hicra_normalization_with_mask() -> None:
    config = HICRAConfig(normalize=True, multiplier=1.0, normalization_eps=1e-6)
    assigner = HICRACreditAssigner(config)
    rewards = torch.tensor([[1.0, 2.0, 3.0], [4.0, 4.0, 4.0]])
    mask = torch.tensor([[True, True, False], [True, False, False]])

    credits = assigner.assign_credit(rewards, mask=mask)

    expected = torch.tensor([[-1.0, 1.0, 0.0], [0.0, 0.0, 0.0]])
    assert torch.allclose(credits, expected, atol=1e-5)


def test_build_hicra_from_dict_handles_nested_config() -> None:
    assigner = build_hicra_from_dict({"hicra": {"multiplier": 3.0}})
    rewards = torch.tensor([1.0, 2.0])

    credits = assigner(rewards)

    assert torch.allclose(credits, rewards * 3.0)


def test_build_hicra_from_dict_supports_alias_keys() -> None:
    assigner = build_hicra_from_dict(
        {"hicra": {"planner_weight": 2.0, "normalize": True, "eps": 1e-6}}
    )

    assert assigner.config.multiplier == 2.0
    assert assigner.config.normalize is True
    assert assigner.config.normalization_eps == 1e-6


def test_hicra_metrics_emitted_when_enabled() -> None:
    hicra_planner_reward_ratio.reset()
    hicra_depth.reset()
    hicra_success.reset()

    assigner = HICRACreditAssigner(HICRAConfig(enabled=True))
    rewards = torch.tensor([[2.0, 1.0, -1.0], [0.0, 0.0, 0.0]])

    _ = assigner.assign_credit(rewards)

    ratio = hicra_planner_reward_ratio.get("overall")
    depth = hicra_depth.get("overall")
    success = hicra_success.get()

    assert ratio == pytest.approx(0.5)
    assert depth == pytest.approx(3.0)
    assert success == 1


def test_hicra_metrics_not_emitted_when_disabled() -> None:
    hicra_planner_reward_ratio.reset()
    hicra_depth.reset()
    hicra_success.reset()

    assigner = HICRACreditAssigner(HICRAConfig(enabled=False))
    rewards = torch.tensor([[1.0, 2.0, 3.0]])

    _ = assigner.assign_credit(rewards)

    assert hicra_planner_reward_ratio.get("overall") == 0.0
    assert hicra_depth.get("overall") == 0.0
    assert hicra_success.get() == 0
