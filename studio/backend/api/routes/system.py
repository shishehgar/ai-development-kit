"""System API routes."""

from __future__ import annotations

from fastapi import APIRouter

from studio.backend.core.config import settings
from studio.backend.schemas.system import SystemStatus
from studio.backend.services.command_catalog import CommandCatalogService

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/status", response_model=SystemStatus)
def system_status() -> SystemStatus:
    commands = CommandCatalogService().list_commands()

    return SystemStatus(
        name=settings.app_name,
        version=settings.version,
        status="ready",
        api_prefix=settings.api_prefix,
        workspace_root=str(settings.workspace_root),
        command_count=len(commands),
    )
