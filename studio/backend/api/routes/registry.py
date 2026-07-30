"""Application registry API routes."""

from __future__ import annotations

from fastapi import APIRouter

from aidk.app import app
from studio.backend.schemas.registry import (
    RegistryResponse,
)


router = APIRouter(
    prefix="/registry",
    tags=["platform"],
)


@router.get(
    "",
    response_model=RegistryResponse,
)
def get_registry() -> RegistryResponse:
    services = [
        item.to_dict()
        for item
        in app.registry.describe()
    ]

    return RegistryResponse.model_validate(
        {
            "total": len(services),
            "services": services,
        }
    )
