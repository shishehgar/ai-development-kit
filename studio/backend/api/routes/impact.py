"""Impact API routes."""

from fastapi import APIRouter


from studio.backend.services.impact_service import (
    analyze_impact,
)


router = APIRouter(
    prefix="/impact",
    tags=[
        "impact"
    ],
)



@router.get("/{entity_id}")
def impact(
    entity_id: str,
):

    return analyze_impact(
        entity_id
    )
