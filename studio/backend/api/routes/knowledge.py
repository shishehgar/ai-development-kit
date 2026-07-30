"""Knowledge API routes."""

from __future__ import annotations

from fastapi import APIRouter

from studio.backend.services.knowledge_runtime import (
    knowledge_runtime,
)

from studio.backend.schemas.knowledge import (
    KnowledgeHealthResponse,
    KnowledgeSummaryResponse,
)


router = APIRouter(
    prefix="/knowledge",
    tags=[
        "knowledge"
    ],
)



@router.get(
    "/health",
    response_model=KnowledgeHealthResponse,
)
def knowledge_health():

    return {
        "status": "ok",
        "service": "knowledge",
    }



@router.get(
    "/summary",
    response_model=KnowledgeSummaryResponse,
)
@router.post(
    "/scan"
)
def scan_project(
    path: str,
):

    return (
        knowledge_runtime.scan_project(
            path
        )
    )
def knowledge_summary():

    return (
        knowledge_runtime.summary()
    )
