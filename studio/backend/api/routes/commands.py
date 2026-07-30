"""Command discovery and contextual help routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from studio.backend.schemas.commands import (
    CommandCollection,
    CommandSummary,
)
from studio.backend.services.command_catalog import CommandCatalogService

router = APIRouter(prefix="/commands", tags=["commands"])
service = CommandCatalogService()


@router.get("", response_model=CommandCollection)
def list_commands() -> CommandCollection:
    commands = service.list_commands()

    return CommandCollection(
        count=len(commands),
        commands=commands,
    )


@router.get("/{command_name}", response_model=CommandSummary)
def get_command(command_name: str) -> CommandSummary:
    command = service.get_command(command_name)

    if command is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="فرمان موردنظر در AIDK ثبت نشده است.",
        )

    return command
