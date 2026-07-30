"""Git API routes."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Query

from aidk.application.container import services
from studio.backend.schemas.git import GitReportResponse


router = APIRouter(
    prefix="/git",
    tags=["git"],
)


@router.get(
    "",
    response_model=GitReportResponse,
)
def inspect_git(
    path: str | None = Query(
        default=None,
    ),
) -> GitReportResponse:
    target = Path(path) if path else None

    report = services.git.run(
        target
    )

    return GitReportResponse.model_validate(
        report.to_dict()
    )
