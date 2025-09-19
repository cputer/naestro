"""Disabled-by-default registry helper for the mlabonne/llm-datasets catalog."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
import json
from pathlib import Path
from typing import Any

import yaml


_CONFIG_PATH = Path(__file__).resolve().parents[2] / "configs" / "datasets" / "llm_datasets.yaml"


class LLMDatasetsRegistry:
    """Helper around the curated mlabonne/llm-datasets configuration."""

    def __init__(
        self,
        document: Mapping[str, Any] | None = None,
        *,
        config_path: Path | None = None,
    ) -> None:
        self._config_path = config_path or _CONFIG_PATH
        raw_document = self._load_document(document)
        self._config = self._extract_config(raw_document)
        self._categories = self._normalise_categories(self._config.get("categories"))

    def _load_document(self, document: Mapping[str, Any] | None) -> dict[str, Any]:
        if document is not None:
            return dict(document)

        if not self._config_path.exists():
            raise FileNotFoundError(f"Dataset registry config missing: {self._config_path}")
        loaded = yaml.safe_load(self._config_path.read_text()) or {}
        if not isinstance(loaded, dict):
            raise TypeError("Dataset registry config must deserialize to a mapping")
        return loaded

    @staticmethod
    def _extract_config(document: Mapping[str, Any]) -> dict[str, Any]:
        if "llm_datasets" in document and isinstance(document["llm_datasets"], Mapping):
            source = document["llm_datasets"]
        else:
            source = document
        return dict(source)

    @staticmethod
    def _normalise_categories(categories: Any) -> list[dict[str, Any]]:
        normalised: list[dict[str, Any]] = []
        if isinstance(categories, Mapping):
            for identifier, entry in categories.items():
                if isinstance(entry, Mapping):
                    data = dict(entry)
                else:
                    data = {"value": entry}
                data.setdefault("id", identifier)
                normalised.append(data)
            return normalised

        if isinstance(categories, Iterable):
            for entry in categories:
                if isinstance(entry, Mapping):
                    normalised.append(dict(entry))
        return normalised

    @property
    def enabled(self) -> bool:
        """Return whether the registry is enabled for automated consumption."""

        return bool(self._config.get("enabled"))

    @property
    def notes(self) -> str | None:
        """Return the operator notes attached to the registry configuration."""

        raw_notes = self._config.get("notes")
        return str(raw_notes) if raw_notes is not None else None

    def list_categories(self) -> list[str]:
        """Return the category identifiers tracked in the registry."""

        categories: list[str] = []
        for entry in self._categories:
            identifier = entry.get("id") or entry.get("title") or entry.get("name")
            if identifier is None:
                continue
            categories.append(str(identifier))
        return categories

    def get_category(self, identifier: str) -> dict[str, Any]:
        """Return metadata for a given category identifier."""

        normalised = identifier.lower()
        for entry in self._categories:
            candidate = str(entry.get("id") or entry.get("title") or "").lower()
            if candidate == normalised:
                return dict(entry)
        raise KeyError(f"Unknown dataset category: {identifier}")

    def create_plan(self, identifier: str) -> dict[str, Any]:
        """Create a disabled-by-default Naestro plan stub for the requested category."""

        category = self.get_category(identifier)
        plan_template = self._config.get("usage", {}).get("plan_template", {})
        steps: list[Any] = []
        template_steps = plan_template.get("steps")
        if isinstance(template_steps, Iterable) and not isinstance(template_steps, (str, bytes)):
            for step in template_steps:
                steps.append(step)

        sources: list[dict[str, Any]] = []
        for source in category.get("sources", []) or []:
            if isinstance(source, Mapping):
                sources.append(
                    {
                        "name": source.get("name"),
                        "url": source.get("url"),
                        "license": source.get("license"),
                        "size": source.get("size"),
                        "reference": source.get("reference"),
                    }
                )

        return {
            "status": "disabled" if not self.enabled else "draft",
            "category": category.get("id"),
            "title": category.get("title"),
            "summary": category.get("summary"),
            "notes": self.notes,
            "sources": sources,
            "plan_template": {
                "summary": plan_template.get("summary"),
                "steps": steps,
            },
        }

    def export_plan(self, identifier: str, destination: Path) -> Path:
        """Write a category plan stub to disk as formatted JSON."""

        plan = self.create_plan(identifier)
        destination = destination.expanduser().resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(plan, indent=2, sort_keys=True))
        return destination


def load_registry(config_path: Path | None = None) -> LLMDatasetsRegistry:
    """Convenience loader that returns a registry instance from disk."""

    if config_path is not None:
        document = yaml.safe_load(config_path.read_text()) or {}
        return LLMDatasetsRegistry(document=document, config_path=config_path)
    return LLMDatasetsRegistry()
