"""HICRA credit assignment utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional

import torch


@dataclass
class HICRAConfig:
    """Configuration options for the :class:`HICRACreditAssigner`.

    Attributes
    ----------
    enabled:
        When ``False`` the assigner short-circuits and returns zeros.
    multiplier:
        Scalar factor applied to the computed credits.
    normalize:
        If ``True`` the assigner normalizes the masked rewards before applying
        the multiplier.
    normalization_eps:
        Small constant added during variance computation to avoid division by
        zero when all masked rewards are identical.
    """

    enabled: bool = True
    multiplier: float = 1.0
    normalize: bool = False
    normalization_eps: float = 1e-8

    @classmethod
    def from_dict(cls, data: Optional[Mapping[str, Any]] = None) -> "HICRAConfig":
        """Build a :class:`HICRAConfig` from a mapping.

        Parameters
        ----------
        data:
            Mapping containing configuration overrides. ``None`` yields the
            default configuration.
        """

        if data is None:
            return cls()

        def _maybe_get(mapping: Mapping[str, Any], *keys: str, default: Any = None) -> Any:
            for key in keys:
                if key in mapping:
                    return mapping[key]
            return default

        return cls(
            enabled=bool(_maybe_get(data, "enabled", default=True)),
            multiplier=float(_maybe_get(data, "multiplier", default=1.0)),
            normalize=bool(_maybe_get(data, "normalize", default=False)),
            normalization_eps=float(
                _maybe_get(data, "normalization_eps", "epsilon", default=1e-8)
            ),
        )


class HICRACreditAssigner:
    """Assign credits to rewards following the HICRA heuristics."""

    def __init__(self, config: Optional[HICRAConfig] = None) -> None:
        self.config = config or HICRAConfig()

    def __call__(
        self, rewards: torch.Tensor | Any, mask: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """Alias for :meth:`assign_credit`."""

        return self.assign_credit(rewards=rewards, mask=mask)

    def assign_credit(
        self, rewards: torch.Tensor | Any, mask: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """Assign credit scores for a batch of rewards.

        Parameters
        ----------
        rewards:
            Reward tensor of shape ``(..., T)`` where the last dimension
            represents the time steps in a trajectory.
        mask:
            Optional boolean tensor marking valid positions. ``True`` indicates
            a valid step. When ``None`` every position is treated as valid.
        """

        rewards_tensor = self._ensure_tensor(rewards)

        if not self.config.enabled:
            return torch.zeros_like(rewards_tensor)

        mask_tensor = self._build_mask(mask, rewards_tensor)
        mask_float = mask_tensor.to(dtype=rewards_tensor.dtype)

        masked_rewards = rewards_tensor * mask_float

        if self.config.normalize:
            credits = self._normalize(masked_rewards, mask_float)
        else:
            credits = masked_rewards

        return credits * self.config.multiplier

    def _normalize(self, rewards: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        """Normalize rewards using masked statistics."""

        if rewards.ndim == 0:
            return torch.zeros_like(rewards)

        dim = -1
        valid_counts = mask.sum(dim=dim, keepdim=True)
        safe_counts = torch.clamp(valid_counts, min=1.0)

        totals = (rewards).sum(dim=dim, keepdim=True)
        means = totals / safe_counts
        centered = (rewards - means) * mask

        variances = (centered ** 2).sum(dim=dim, keepdim=True) / safe_counts
        std = torch.sqrt(variances + self.config.normalization_eps)

        normalized = centered / std
        return normalized * mask

    @staticmethod
    def _ensure_tensor(values: torch.Tensor | Any) -> torch.Tensor:
        """Convert the input to a floating point tensor."""

        if isinstance(values, torch.Tensor):
            tensor = values
        else:
            tensor = torch.as_tensor(values)

        if not torch.is_floating_point(tensor):
            tensor = tensor.float()
        return tensor

    @staticmethod
    def _build_mask(mask: Optional[torch.Tensor], reference: torch.Tensor) -> torch.Tensor:
        """Validate and normalize the provided mask."""

        if mask is None:
            return torch.ones_like(reference, dtype=torch.bool)

        mask_tensor = mask
        if not isinstance(mask_tensor, torch.Tensor):
            mask_tensor = torch.as_tensor(mask)

        if mask_tensor.shape != reference.shape:
            raise ValueError("Mask must have the same shape as rewards.")

        if mask_tensor.dtype != torch.bool:
            mask_tensor = mask_tensor.to(dtype=torch.bool)

        return mask_tensor


def build_hicra_from_dict(config: Optional[Mapping[str, Any]]) -> HICRACreditAssigner:
    """Construct an assigner from a configuration mapping.

    Parameters
    ----------
    config:
        Either a mapping containing the trainer configuration or ``None`` to use
        defaults. The function accepts dictionaries with either the full
        ``{"hicra": {...}}`` nesting or the direct configuration mapping.
    """

    if config is None:
        return HICRACreditAssigner()

    if not isinstance(config, Mapping):
        raise TypeError("Configuration must be a mapping or None.")

    hicra_config = config.get("hicra") if "hicra" in config else config
    if hicra_config is None:
        return HICRACreditAssigner()
    if not isinstance(hicra_config, Mapping):
        raise TypeError("HICRA configuration must be a mapping.")

    return HICRACreditAssigner(HICRAConfig.from_dict(hicra_config))
