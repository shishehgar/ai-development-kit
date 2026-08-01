"""AI status API routes."""

from fastapi import APIRouter

from studio.backend.services.ai_status import (
    ai_status_service,
)


router = APIRouter(
    prefix="/assistant",
    tags=["assistant"],
)



@router.get("/status")
def assistant_status():

    return (
        ai_status_service.status()
    )
