#!/usr/bin/env python3
"""CLI for running lightweight PPO training on the router environment."""

from __future__ import annotations

import argparse
import json
import logging
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict

import numpy as np
import yaml

from integrations.policy.rllm_ppo_adapter import (
    PPOParams,
    RewardWeights,
    RouterPPOAdapter,
)

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[1] / "configs" / "policy" / "rllm.yaml"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="Path to the RLLM configuration YAML file.",
    )
    parser.add_argument(
        "--updates",
        type=int,
        default=4,
        help="Number of PPO update iterations to run.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=0,
        help="Random seed passed to the adapter components.",
    )
    parser.add_argument(
        "--episode-length",
        dest="episode_length",
        type=int,
        default=64,
        help="Episode length for the synthetic router environment.",
    )
    return parser.parse_args()


def _ensure_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _load_config(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Configuration at {path} must be a mapping")
    return data


def _configure_logging(observability_cfg: Dict[str, Any]) -> None:
    logging_cfg = _ensure_dict(observability_cfg.get("logging"))
    if logging_cfg.get("enabled", False):
        level_name = str(logging_cfg.get("level", "info")).upper()
        level = getattr(logging, level_name, logging.INFO)
        handlers = []
        destination = logging_cfg.get("destination")
        if isinstance(destination, str) and destination:
            log_path = Path(destination)
            if not log_path.is_absolute():
                log_path = Path.cwd() / log_path
            log_path.parent.mkdir(parents=True, exist_ok=True)
            handlers.append(logging.FileHandler(log_path, encoding="utf-8"))
        if not handlers:
            handlers.append(logging.StreamHandler())
        logging.basicConfig(
            level=level,
            format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
            handlers=handlers,
        )
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        )


def _resolve_output_dir(path: Any) -> Path:
    if isinstance(path, (str, Path)) and path:
        output_path = Path(path)
        if not output_path.is_absolute():
            output_path = Path.cwd() / output_path
    else:
        output_path = Path.cwd() / "outputs" / "router_ppo"
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def _write_artifacts(
    output_dir: Path,
    history: list[Dict[str, Any]],
    policy_state: Dict[str, np.ndarray],
    params: PPOParams,
    reward_weights: RewardWeights,
    args: argparse.Namespace,
    raw_config: Dict[str, Any],
) -> None:
    history_path = output_dir / "training_history.json"
    with history_path.open("w", encoding="utf-8") as handle:
        json.dump(history, handle, indent=2)

    weights_path = output_dir / "policy_state.npz"
    np.savez(weights_path, **policy_state)

    metadata = {
        "updates": int(args.updates),
        "seed": int(args.seed),
        "episode_length": int(args.episode_length),
        "ppo_params": asdict(params),
        "reward_weights": asdict(reward_weights),
        "config_path": str(Path(args.config).resolve()),
    }
    metadata_path = output_dir / "metadata.json"
    with metadata_path.open("w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2)

    snapshot_path = output_dir / "config_snapshot.yaml"
    with snapshot_path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(raw_config, handle, sort_keys=False)

    logger.info("Artifacts written to %s", output_dir)


def main() -> int:
    args = _parse_args()
    config = _load_config(Path(args.config))
    rllm_cfg = _ensure_dict(config.get("rllm"))

    if not rllm_cfg.get("enabled", False):
        logger.info("RLLM integration disabled; nothing to do.")
        return 0

    trainer_cfg = _ensure_dict(rllm_cfg.get("trainer"))
    if not trainer_cfg.get("enabled", False):
        logger.info("Trainer disabled in configuration; skipping PPO run.")
        return 0

    backend = str(trainer_cfg.get("backend", "")).lower()
    if backend and backend not in {"ppo", "trlx"}:
        logger.warning("Unsupported trainer backend '%s'; continuing with PPO adapter.", backend)

    _configure_logging(_ensure_dict(rllm_cfg.get("observability", {})))

    params = PPOParams.from_dict(_ensure_dict(rllm_cfg.get("ppo")))
    reward_weights = RewardWeights.from_dict(rllm_cfg.get("reward_weights"))

    adapter = RouterPPOAdapter(
        params,
        reward_weights=reward_weights,
        seed=args.seed,
        episode_length=args.episode_length,
    )
    logger.info(
        "Starting PPO training with rollout_length=%s, updates=%s", params.rollout_length, args.updates
    )
    results = adapter.train(num_updates=args.updates)
    history = results.get("history", [])
    policy_state = results.get("policy_state", {})

    experiment_cfg = _ensure_dict(rllm_cfg.get("experiment"))
    if experiment_cfg.get("enabled", False):
        output_dir = _resolve_output_dir(experiment_cfg.get("output_dir"))
        _write_artifacts(output_dir, history, policy_state, params, reward_weights, args, config)
    else:
        logger.info("Experiment output disabled; skipping artifact persistence.")

    logger.info("Training finished after %s updates", args.updates)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    raise SystemExit(main())
