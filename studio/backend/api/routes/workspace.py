"""Workspace routes."""

from __future__ import annotations

from fastapi import APIRouter

from aidk.app import app

from studio.backend.schemas.workspace import (
    WorkspaceReportResponse,
)

router = APIRouter(
    prefix="/workspace",
    tags=["workspace"],
)


@router.get(
    "",
    response_model=WorkspaceReportResponse,
)
def workspace():

    report = app.services.workspace.run()

    return WorkspaceReportResponse.model_validate(
        report.to_dict()
    )
