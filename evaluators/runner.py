"""Evaluation suite runner and determinism guard."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping

import yaml

from infra import determinism


CONFIG_PATH = Path(__file__).resolve().parents[1] / "configs" / "evals.yaml"


def _as_mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return list(value)
    return []


@dataclass(frozen=True)
class SuiteDefinition:
    """Resolved evaluation suite configuration."""

    name: str
    config: dict[str, Any]
    deterministic: bool

    @property
    def datasets(self) -> list[Any]:
        """Return the dataset references configured for the suite."""

        return _as_list(self.config.get("datasets", []))


class EvalSuiteRunner:
    """Helper responsible for loading suites and enabling determinism."""

    def __init__(self, config_path: Path | None = None) -> None:
        self.config_path = config_path or CONFIG_PATH
        self._config = self._load_config(self.config_path)

    @staticmethod
    def _load_config(path: Path) -> dict[str, Any]:
        if not path.exists():
            return {}
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        if not isinstance(data, Mapping):
            raise ValueError("evals.yaml must define a mapping at the top level")
        return dict(data)

    @property
    def defaults(self) -> dict[str, Any]:
        return _as_mapping(self._config.get("defaults", {}))

    @property
    def datasets(self) -> dict[str, dict[str, Any]]:
        registry: dict[str, dict[str, Any]] = {}
        for item in _as_list(self._config.get("datasets", [])):
            if not isinstance(item, Mapping):
                continue
            name = item.get("name")
            if isinstance(name, str) and name:
                registry[name] = dict(item)
        return registry

    def list_suites(self) -> list[str]:
        suites = self._config.get("suites", {})
        if not isinstance(suites, Mapping):
            return []
        return [str(name) for name in suites.keys()]

    def _resolve_suite_config(self, name: str) -> dict[str, Any]:
        suites = self._config.get("suites", {})
        if not isinstance(suites, Mapping) or name not in suites:
            raise KeyError(f"Unknown evaluation suite '{name}'")
        return _as_mapping(suites[name])

    def _resolve_deterministic(self, suite_cfg: Mapping[str, Any]) -> bool:
        if "deterministic" in suite_cfg:
            return bool(suite_cfg.get("deterministic"))
        defaults = self.defaults
        return bool(defaults.get("deterministic", False))

    def get_suite(self, name: str) -> SuiteDefinition:
        suite_cfg = self._resolve_suite_config(name)
        return SuiteDefinition(
            name=name,
            config=suite_cfg,
            deterministic=self._resolve_deterministic(suite_cfg),
        )

    def iter_suites(self, selection: Iterable[str] | None = None) -> Iterator[SuiteDefinition]:
        names = list(selection) if selection is not None else self.list_suites()
        for name in names:
            yield self.get_suite(name)

    def enable_for_suite(self, suite: SuiteDefinition) -> None:
        if suite.deterministic:
            seed = int(os.getenv("NAESTRO_EVAL_SEED", "0"))
            determinism.enable(seed)

    def iter_prepared_suites(self, selection: Iterable[str] | None = None) -> Iterator[SuiteDefinition]:
        for suite in self.iter_suites(selection):
            self.enable_for_suite(suite)
            yield suite

    def resolve_suite_datasets(self, suite: SuiteDefinition) -> list[dict[str, Any]]:
        resolved: list[dict[str, Any]] = []
        registry = self.datasets
        for entry in suite.datasets:
            if isinstance(entry, str):
                if entry not in registry:
                    raise KeyError(
                        f"Suite '{suite.name}' references unknown dataset '{entry}'"
                    )
                resolved.append(dict(registry[entry]))
                continue

            if isinstance(entry, Mapping):
                name = entry.get("name")
                base = registry.get(name) if isinstance(name, str) else None
                merged = dict(base) if base else {}
                merged.update({k: v for k, v in entry.items() if k != "name"})
                if name and isinstance(name, str):
                    merged["name"] = name
                resolved.append(merged)
        return resolved


__all__ = ["EvalSuiteRunner", "SuiteDefinition"]
