"""Project impact-analysis API routes."""

from __future__ import annotations

from fastapi import (
    APIRouter,
    HTTPException,
)

from studio.backend.services.project_impact import (
    AmbiguousImpactEntityError,
    ImpactEntityNotFoundError,
    ProjectNotFoundError,
    project_impact_service,
)


router = APIRouter(
    prefix="/projects",
    tags=["impact"],
)


@router.get(
    "/{project_id}/impact/{entity_reference}",
)
def analyze_project_impact(
    project_id: str,
    entity_reference: str,
) -> dict[str, object]:
    """Return dependency impact for a project entity."""

    try:
        return project_impact_service.analyze(
            project_id,
            entity_reference,
        )

    except ProjectNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except ImpactEntityNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except AmbiguousImpactEntityError as exc:
        raise HTTPException(
            status_code=409,
            detail={
                "message": str(exc),
                "candidates": exc.candidates,
            },
        ) from exc
