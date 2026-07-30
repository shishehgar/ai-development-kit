"""Knowledge API routes."""

from fastapi import APIRouter


router = APIRouter(
    prefix="/knowledge",
    tags=[
        "knowledge"
    ],
)


@router.get(
    "/health"
)
def knowledge_health():

    return {
        "status": "ok",
        "service": "knowledge",
    }
