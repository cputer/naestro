"""Lightweight PPO components for router policy prototyping."""

from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass, fields
from typing import Any, Dict, Iterable, Mapping, Sequence

import numpy as np

from router.collab_policy import CollaborationMode

logger = logging.getLogger(__name__)

_EPS = 1e-8


@dataclass(slots=True)
class PPOParams:
    """Hyper-parameters controlling the PPO update."""

    rollout_length: int = 256
    mini_batch_size: int = 64
    update_epochs: int = 4
    gamma: float = 0.99
    gae_lambda: float = 0.95
    clip_coef: float = 0.2
    value_loss_coef: float = 0.5
    entropy_coef: float = 0.01
    learning_rate: float = 3e-4
    max_grad_norm: float = 1.0

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> "PPOParams":
        data = data or {}
        kwargs: Dict[str, Any] = {}
        for field in fields(cls):
            kwargs[field.name] = data.get(field.name, getattr(cls, field.name))
        params = cls(**kwargs)
        params.validate()
        return params

    def validate(self) -> None:
        if self.rollout_length <= 0:
            raise ValueError("rollout_length must be positive")
        if self.mini_batch_size <= 0:
            raise ValueError("mini_batch_size must be positive")
        if self.mini_batch_size > self.rollout_length:
            raise ValueError("mini_batch_size cannot exceed rollout_length")
        if self.update_epochs <= 0:
            raise ValueError("update_epochs must be positive")
        if not 0.0 < self.gamma <= 1.0:
            raise ValueError("gamma must be in (0, 1]")
        if not 0.0 <= self.gae_lambda <= 1.0:
            raise ValueError("gae_lambda must be in [0, 1]")
        if self.clip_coef <= 0:
            raise ValueError("clip_coef must be positive")
        if self.learning_rate <= 0:
            raise ValueError("learning_rate must be positive")
        if self.max_grad_norm <= 0:
            raise ValueError("max_grad_norm must be positive")


@dataclass(slots=True)
class RewardWeights:
    """Linear weights applied to router environment metrics."""

    throughput: float = 1.0
    reliability: float = 0.5
    latency: float = 0.75
    collaboration_cost: float = 0.1
    violation: float = 1.0

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> "RewardWeights":
        data = data or {}
        kwargs: Dict[str, Any] = {}
        for field in fields(cls):
            kwargs[field.name] = float(data.get(field.name, getattr(cls, field.name)))
        return cls(**kwargs)


class RouterEnv:
    """Synthetic router environment suitable for toy PPO experiments."""

    def __init__(
        self,
        reward_weights: RewardWeights | None = None,
        *,
        episode_length: int = 64,
        seed: int | None = None,
    ) -> None:
        self.reward_weights = reward_weights or RewardWeights()
        self.episode_length = int(episode_length)
        if self.episode_length <= 0:
            raise ValueError("episode_length must be positive")
        self._rng = np.random.default_rng(seed)
        self._modes: Sequence[CollaborationMode] = list(CollaborationMode)
        self.action_dim = len(self._modes)
        self.observation_dim = 4
        self._state = np.zeros(self.observation_dim, dtype=np.float32)
        self._steps = 0

    def reset(self) -> np.ndarray:
        """Reset the environment to a random initial state."""

        self._steps = 0
        # Observation vector: [traffic_load, latency, collaboration_pressure, backlog]
        self._state = self._rng.uniform(low=[0.3, 0.2, 0.1, 0.1], high=[0.9, 0.6, 0.9, 0.7]).astype(
            np.float32
        )
        return self._state.copy()

    def step(self, action: int) -> tuple[np.ndarray, float, bool, Dict[str, Any]]:
        """Advance the environment by one step."""

        if not 0 <= action < self.action_dim:
            raise ValueError(f"action must be in [0, {self.action_dim})")

        traffic_load, latency, collaboration_pressure, backlog = self._state.astype(float)
        collaboration_level = 0.0 if self.action_dim <= 1 else action / (self.action_dim - 1)

        # Heuristic metrics influenced by the selected collaboration strategy.
        throughput = (1.15 - 0.25 * collaboration_level) * (1.0 - 0.4 * backlog)
        throughput *= 1.0 - 0.35 * latency
        throughput = max(0.0, throughput + self._rng.normal(0.0, 0.02))

        reliability = 0.55 + 0.3 * collaboration_level - 0.45 * latency
        reliability += self._rng.normal(0.0, 0.05)
        reliability = float(np.clip(reliability, 0.0, 1.0))

        latency_penalty = latency + 0.25 * collaboration_level + 0.05 * backlog
        latency_penalty += abs(self._rng.normal(0.0, 0.03))

        collaboration_cost = collaboration_level * (0.35 + 0.4 * collaboration_pressure)

        violation_penalty = max(0.0, 0.3 - reliability)

        metrics = {
            "throughput": float(throughput),
            "reliability": reliability,
            "latency": float(latency_penalty),
            "collaboration_cost": float(collaboration_cost),
            "violation_penalty": float(violation_penalty),
        }

        reward = compute_reward(metrics, self.reward_weights)

        # Transition dynamics encourage exploration of different collaboration levels.
        traffic_load = float(np.clip(0.55 * traffic_load + 0.35 * collaboration_pressure + 0.1 * self._rng.random(), 0.0, 1.0))
        latency = float(
            np.clip(
                0.6 * latency + 0.25 * backlog + 0.2 * collaboration_level + self._rng.normal(0.0, 0.02),
                0.0,
                1.2,
            )
        )
        collaboration_pressure = float(
            np.clip(
                0.4 * collaboration_pressure + 0.4 * self._rng.random() + 0.2 * collaboration_level,
                0.0,
                1.0,
            )
        )
        backlog = float(
            np.clip(
                0.5 * backlog + 0.3 * traffic_load + 0.2 * (1.0 - throughput) + 0.1 * self._rng.random(),
                0.0,
                1.0,
            )
        )

        self._state = np.array([traffic_load, latency, collaboration_pressure, backlog], dtype=np.float32)
        self._steps += 1
        done = self._steps >= self.episode_length

        info = {
            "metrics": metrics,
            "mode": self._modes[action].value,
            "step": self._steps,
        }
        if done:
            # Reset step counter for the next rollout; the caller handles fetching the next observation.
            self._steps = 0
        return self._state.copy(), float(reward), bool(done), info


def compute_reward(metrics: Mapping[str, float], weights: RewardWeights) -> float:
    """Combine environment metrics into a scalar reward."""

    throughput = float(metrics.get("throughput", 0.0))
    reliability = float(metrics.get("reliability", 0.0))
    latency = float(metrics.get("latency", 0.0))
    collaboration_cost = float(metrics.get("collaboration_cost", 0.0))
    violation = float(metrics.get("violation_penalty", metrics.get("violation", 0.0)))

    reward = 0.0
    reward += weights.throughput * throughput
    reward += weights.reliability * reliability
    reward -= weights.latency * latency
    reward -= weights.collaboration_cost * collaboration_cost
    reward -= weights.violation * violation
    return float(reward)


class SimpleCategoricalPolicy:
    """Linear policy/value heads with categorical action sampling."""

    def __init__(
        self,
        observation_dim: int,
        action_dim: int,
        *,
        rng: np.random.Generator | None = None,
    ) -> None:
        self.observation_dim = observation_dim
        self.action_dim = action_dim
        self._rng = rng or np.random.default_rng()
        scale = 1.0 / np.sqrt(max(observation_dim, 1))
        self.policy_w = self._rng.normal(0.0, scale, size=(observation_dim, action_dim)).astype(np.float32)
        self.policy_b = np.zeros(action_dim, dtype=np.float32)
        self.value_w = self._rng.normal(0.0, scale, size=(observation_dim,)).astype(np.float32)
        self.value_b = 0.0

    def _softmax(self, logits: np.ndarray) -> np.ndarray:
        logits = logits - logits.max(axis=-1, keepdims=True)
        exp_logits = np.exp(logits)
        return exp_logits / np.clip(exp_logits.sum(axis=-1, keepdims=True), _EPS, None)

    def policy_logits(self, obs: np.ndarray) -> np.ndarray:
        return obs @ self.policy_w + self.policy_b

    def value(self, obs: np.ndarray) -> float:
        return float(obs @ self.value_w + self.value_b)

    def act(self, obs: np.ndarray) -> tuple[int, float, float]:
        logits = self.policy_logits(obs[np.newaxis, :])[0]
        probs = self._softmax(logits[np.newaxis, :])[0]
        action = int(self._rng.choice(self.action_dim, p=probs))
        log_prob = float(np.log(np.clip(probs[action], _EPS, None)))
        value = self.value(obs)
        return action, log_prob, value

    def evaluate(self, obs: np.ndarray, actions: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        logits = self.policy_logits(obs)
        probs = self._softmax(logits)
        log_probs = np.log(np.clip(probs, _EPS, None))
        selected_log_probs = log_probs[np.arange(obs.shape[0]), actions]
        values = obs @ self.value_w + self.value_b
        entropy = -np.sum(probs * log_probs, axis=1)
        return selected_log_probs, values, entropy, probs

    def state_dict(self) -> Dict[str, np.ndarray]:
        return {
            "policy_w": self.policy_w.copy(),
            "policy_b": self.policy_b.copy(),
            "value_w": self.value_w.copy(),
            "value_b": np.array([self.value_b], dtype=np.float32),
        }

    def load_state_dict(self, state: Mapping[str, np.ndarray]) -> None:
        self.policy_w = np.array(state["policy_w"], dtype=np.float32)
        self.policy_b = np.array(state["policy_b"], dtype=np.float32)
        self.value_w = np.array(state["value_w"], dtype=np.float32)
        self.value_b = float(np.array(state["value_b"], dtype=np.float32).item())

    def update(
        self,
        obs: np.ndarray,
        actions: np.ndarray,
        old_log_probs: np.ndarray,
        returns: np.ndarray,
        advantages: np.ndarray,
        params: PPOParams,
        *,
        rng: np.random.Generator | None = None,
    ) -> Dict[str, float]:
        rng = rng or np.random.default_rng()
        batch_size = obs.shape[0]
        if batch_size == 0:
            raise ValueError("Empty batch provided to policy update")

        metrics: list[Dict[str, float]] = []
        for _ in range(params.update_epochs):
            indices = rng.permutation(batch_size)
            for start in range(0, batch_size, params.mini_batch_size):
                end = start + params.mini_batch_size
                mb_idx = indices[start:end]
                metrics.append(
                    self._update_minibatch(
                        obs[mb_idx],
                        actions[mb_idx],
                        old_log_probs[mb_idx],
                        returns[mb_idx],
                        advantages[mb_idx],
                        params,
                    )
                )
        agg: Dict[str, float] = {}
        if metrics:
            for key in metrics[0].keys():
                agg[key] = float(np.mean([m[key] for m in metrics]))
        return agg

    def _update_minibatch(
        self,
        obs: np.ndarray,
        actions: np.ndarray,
        old_log_probs: np.ndarray,
        returns: np.ndarray,
        advantages: np.ndarray,
        params: PPOParams,
    ) -> Dict[str, float]:
        logits = self.policy_logits(obs)
        probs = self._softmax(logits)
        log_probs = np.log(np.clip(probs, _EPS, None))
        batch_indices = np.arange(obs.shape[0])
        selected_log_probs = log_probs[batch_indices, actions]
        values = obs @ self.value_w + self.value_b
        entropy = -np.mean(np.sum(probs * log_probs, axis=1))

        ratios = np.exp(selected_log_probs - old_log_probs)
        clipped_ratios = np.clip(ratios, 1.0 - params.clip_coef, 1.0 + params.clip_coef)
        surrogate1 = ratios * advantages
        surrogate2 = clipped_ratios * advantages
        objective = np.minimum(surrogate1, surrogate2)
        policy_loss = -np.mean(objective)

        value_loss = 0.5 * np.mean((returns - values) ** 2)

        approx_kl = float(np.mean(old_log_probs - selected_log_probs))
        clip_frac = float(np.mean(np.greater(np.abs(ratios - 1.0), params.clip_coef)))

        # Gradients ------------------------------------------------------------------
        one_hot = np.zeros_like(probs)
        one_hot[batch_indices, actions] = 1.0

        grad_ratio = advantages[:, None] * ratios[:, None] * (one_hot - probs)
        grad_ratio_clipped = grad_ratio.copy()
        active_clip = (ratios >= 1.0 - params.clip_coef) & (ratios <= 1.0 + params.clip_coef)
        grad_ratio_clipped[~active_clip, :] = 0.0
        use_surrogate1 = surrogate1 <= surrogate2
        grad_objective = np.where(use_surrogate1[:, None], grad_ratio, grad_ratio_clipped)
        grad_policy_logits = -grad_objective / obs.shape[0]

        # Entropy gradient contribution
        grad_entropy = np.zeros_like(probs)
        for i in range(obs.shape[0]):
            p = probs[i]
            log_p = log_probs[i]
            jacobian = np.diag(p) - np.outer(p, p)
            grad_entropy[i] = -jacobian @ (log_p + 1.0)
        grad_entropy = -params.entropy_coef * grad_entropy / obs.shape[0]

        grad_logits_total = grad_policy_logits + grad_entropy
        grad_policy_w = obs.T @ grad_logits_total
        grad_policy_b = grad_logits_total.sum(axis=0)

        grad_values = params.value_loss_coef * (values - returns) / obs.shape[0]
        grad_value_w = obs.T @ grad_values[:, None]
        grad_value_b = grad_values.sum()

        total_norm = float(
            np.sqrt(
                np.sum(grad_policy_w**2)
                + np.sum(grad_policy_b**2)
                + np.sum(grad_value_w**2)
                + grad_value_b**2
            )
        )
        if total_norm > params.max_grad_norm:
            scale = params.max_grad_norm / (total_norm + _EPS)
            grad_policy_w *= scale
            grad_policy_b *= scale
            grad_value_w *= scale
            grad_value_b *= scale

        self.policy_w -= params.learning_rate * grad_policy_w
        self.policy_b -= params.learning_rate * grad_policy_b
        self.value_w -= params.learning_rate * grad_value_w.flatten()
        self.value_b -= params.learning_rate * grad_value_b

        return {
            "policy_loss": float(policy_loss),
            "value_loss": float(value_loss),
            "entropy": float(entropy),
            "approx_kl": approx_kl,
            "clip_frac": clip_frac,
        }


def _compute_gae(
    rewards: np.ndarray,
    values: np.ndarray,
    dones: np.ndarray,
    last_value: float,
    gamma: float,
    gae_lambda: float,
) -> tuple[np.ndarray, np.ndarray]:
    advantages = np.zeros_like(rewards)
    lastgaelam = 0.0
    for t in reversed(range(rewards.shape[0])):
        if t == rewards.shape[0] - 1:
            next_values = last_value
            next_non_terminal = 1.0 - dones[t]
        else:
            next_values = values[t + 1]
            next_non_terminal = 1.0 - dones[t + 1]
        delta = rewards[t] + gamma * next_values * next_non_terminal - values[t]
        lastgaelam = delta + gamma * gae_lambda * next_non_terminal * lastgaelam
        advantages[t] = lastgaelam
    returns = advantages + values
    return advantages, returns


def _aggregate_metrics(metrics: Iterable[Mapping[str, float]]) -> Dict[str, float]:
    totals: dict[str, float] = defaultdict(float)
    count = 0
    for metric in metrics:
        if not metric:
            continue
        count += 1
        for key, value in metric.items():
            totals[key] += float(value)
    if count == 0:
        return {}
    return {f"avg_{key}": totals[key] / count for key in totals}


def ppo_train(
    env: RouterEnv,
    policy: SimpleCategoricalPolicy,
    params: PPOParams,
    *,
    num_updates: int,
    rng: np.random.Generator | None = None,
) -> list[Dict[str, float]]:
    """Execute PPO training and return per-update metrics."""

    rng = rng or np.random.default_rng()
    history: list[Dict[str, float]] = []
    obs = env.reset()

    for update in range(num_updates):
        observations: list[np.ndarray] = []
        actions: list[int] = []
        log_probs: list[float] = []
        rewards: list[float] = []
        dones: list[float] = []
        values: list[float] = []
        step_metrics: list[Mapping[str, float]] = []
        episode_returns: list[float] = []
        episode_lengths: list[int] = []
        running_return = 0.0
        running_length = 0

        for _ in range(params.rollout_length):
            action, log_prob, value = policy.act(obs)
            next_obs, reward, done, info = env.step(action)

            observations.append(obs)
            actions.append(action)
            log_probs.append(log_prob)
            rewards.append(reward)
            dones.append(1.0 if done else 0.0)
            values.append(value)
            if isinstance(info, Mapping):
                step_metrics.append(info.get("metrics", {}))

            running_return += reward
            running_length += 1
            obs = next_obs

            if done:
                episode_returns.append(running_return)
                episode_lengths.append(running_length)
                obs = env.reset()
                running_return = 0.0
                running_length = 0

        last_value = policy.value(obs)
        advantages, returns = _compute_gae(
            np.array(rewards, dtype=np.float32),
            np.array(values, dtype=np.float32),
            np.array(dones, dtype=np.float32),
            last_value,
            params.gamma,
            params.gae_lambda,
        )
        advantages = (advantages - advantages.mean()) / (advantages.std() + _EPS)

        update_metrics = policy.update(
            np.array(observations, dtype=np.float32),
            np.array(actions, dtype=np.int32),
            np.array(log_probs, dtype=np.float32),
            np.array(returns, dtype=np.float32),
            advantages.astype(np.float32),
            params,
            rng=rng,
        )

        aggregated_metrics = _aggregate_metrics(step_metrics)
        mean_reward = float(np.mean(rewards)) if rewards else 0.0
        if episode_returns:
            avg_episode_return = float(np.mean(episode_returns))
            avg_episode_length = float(np.mean(episode_lengths))
        else:
            avg_episode_return = float(sum(rewards))
            avg_episode_length = float(len(rewards))

        history_entry: Dict[str, float] = {
            "update": float(update + 1),
            "mean_reward": mean_reward,
            "avg_episode_return": avg_episode_return,
            "avg_episode_length": avg_episode_length,
        }
        history_entry.update({key: float(value) for key, value in aggregated_metrics.items()})
        history_entry.update(update_metrics)
        history.append(history_entry)

        logger.info(
            "Update %s | reward=%.3f policy_loss=%.3f value_loss=%.3f entropy=%.3f",
            update + 1,
            mean_reward,
            update_metrics.get("policy_loss", float("nan")),
            update_metrics.get("value_loss", float("nan")),
            update_metrics.get("entropy", float("nan")),
        )

    return history


class RouterPPOAdapter:
    """Convenience wrapper wiring the environment, policy, and PPO loop."""

    def __init__(
        self,
        params: PPOParams,
        reward_weights: RewardWeights | None = None,
        *,
        seed: int | None = None,
        episode_length: int = 64,
    ) -> None:
        base_rng = np.random.default_rng(seed)
        self.env = RouterEnv(
            reward_weights=reward_weights,
            episode_length=episode_length,
            seed=int(base_rng.integers(0, 1_000_000)),
        )
        self.policy = SimpleCategoricalPolicy(
            self.env.observation_dim,
            self.env.action_dim,
            rng=np.random.default_rng(int(base_rng.integers(0, 1_000_000))),
        )
        self.params = params
        self._rng = np.random.default_rng(int(base_rng.integers(0, 1_000_000)))

    def train(self, num_updates: int) -> Dict[str, Any]:
        history = ppo_train(
            self.env,
            self.policy,
            self.params,
            num_updates=num_updates,
            rng=self._rng,
        )
        return {
            "history": history,
            "policy_state": self.policy.state_dict(),
        }


__all__ = [
    "PPOParams",
    "RewardWeights",
    "RouterEnv",
    "SimpleCategoricalPolicy",
    "RouterPPOAdapter",
    "compute_reward",
    "ppo_train",
]
