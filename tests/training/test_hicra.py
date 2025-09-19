"""Unit tests for the HICRA credit assignment helpers."""

import torch

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
