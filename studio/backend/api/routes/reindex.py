"""Incremental project reindex API."""

from __future__ import annotations

from fastapi import (
    APIRouter,
    HTTPException,
)

from studio.backend.schemas.reindex import (
    ReindexResponse,
)
from studio.backend.services.project_incremental import (
    IncrementalProjectNotFoundError,
    ProjectIncrementalError,
    project_incremental_service,
)


router = APIRouter(
    prefix="/projects",
    tags=["project-reindex"],
)


@router.post(
    "/{project_id}/reindex",
    response_model=ReindexResponse,
)
def reindex_project(
    project_id: str,
) -> ReindexResponse:
    """Safely reindex a registered project."""

    try:
        result = (
            project_incremental_service
            .reindex(project_id)
        )

        return ReindexResponse(
            **result
        )

    except IncrementalProjectNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except ProjectIncrementalError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc
