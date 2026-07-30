"""Plugin API routes."""

from __future__ import annotations

from fastapi import APIRouter

from aidk.app import app
from studio.backend.schemas.plugins import (
    PluginsResponse,
)


router = APIRouter(
    prefix="/plugins",
    tags=["platform"],
)


@router.get(
    "",
    response_model=PluginsResponse,
)
def get_plugins() -> PluginsResponse:
    loaded_plugins = (
        app.plugins.describe()
    )

    discovered_plugins = (
        app.plugins.discover()
    )

    return PluginsResponse.model_validate(
        {
            "loaded": len(
                loaded_plugins
            ),
            "discovered": len(
                discovered_plugins
            ),
            "plugins": loaded_plugins,
        }
    )
