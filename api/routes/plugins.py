"""Plugin routes for interacting with optional integrations."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from integrations.plugins.deepcode_adapter import DeepCodeAdapter


CONFIG_PATH = Path(__file__).resolve().parents[2] / "configs" / "plugins.yaml"

router = APIRouter()


class DeepCodeBuildRequest(BaseModel):
    """Payload for DeepCode build requests."""

    source: Any | None = None


class DeepCodeBuildResponse(BaseModel):
    """Schema describing the DeepCode adapter response."""

    status: str
    message: str
    source: Any | None = None


def _load_plugins_config(path: Path | None = None) -> Mapping[str, Any]:
    """Load plugin configuration from YAML, returning an empty mapping on error."""

    if path is None:
        path = CONFIG_PATH

    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream) or {}

    if not isinstance(data, Mapping):
        raise ValueError("plugins.yaml must define a mapping at the top level")

    return data


def _resolve_deepcode_config(config: Mapping[str, Any]) -> dict[str, Any]:
    """Extract the DeepCode configuration mapping from the overall config."""

    plugins = config.get("plugins", {})
    if not isinstance(plugins, Mapping):
        return {}

    deepcode = plugins.get("deepcode", {})
    if not isinstance(deepcode, Mapping):
        return {}

    return dict(deepcode)


@router.post("/plugins/deepcode/build", response_model=DeepCodeBuildResponse)
def build_deepcode(request: DeepCodeBuildRequest) -> DeepCodeBuildResponse:
    """Build a DeepCode workspace from the provided source description."""

    config = _resolve_deepcode_config(_load_plugins_config())
    if not config.get("enabled"):
        raise HTTPException(status_code=503, detail="DeepCode plugin is disabled")

    adapter = DeepCodeAdapter(config)
    result = adapter.build_from_source(request.source)
    if not isinstance(result, Mapping):
        raise ValueError("DeepCode adapter must return a mapping")

    return DeepCodeBuildResponse(**result)


__all__ = ["router"]
