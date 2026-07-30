"""Workspace Git report API routes."""

from __future__ import annotations

from fastapi import APIRouter

from aidk.app import app
from studio.backend.schemas.git_report import (
    GitWorkspaceReportResponse,
)


router = APIRouter(
    prefix="/git-report",
    tags=["git"],
)


@router.get(
    "",
    response_model=GitWorkspaceReportResponse,
)
def generate_git_report() -> GitWorkspaceReportResponse:
    report = app.services.git_report.run()

    return GitWorkspaceReportResponse.model_validate(
        report.to_dict()
    )
