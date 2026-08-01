"""Knowledge API routes."""

from __future__ import annotations

from fastapi import APIRouter

from studio.backend.schemas.knowledge import (
    KnowledgeHealthResponse,
    KnowledgeSummaryResponse,
)
from studio.backend.services.knowledge_runtime import (
    knowledge_runtime,
)


router = APIRouter(
    prefix="/knowledge",
    tags=["knowledge"],
)


@router.get(
    "/health",
    response_model=KnowledgeHealthResponse,
)
def knowledge_health() -> dict[str, str]:
    """Return knowledge-service health."""

    return {
        "status": "ok",
        "service": "knowledge",
    }


@router.get(
    "/summary",
    response_model=KnowledgeSummaryResponse,
)
def knowledge_summary():
    """Return current knowledge-graph statistics."""

    return knowledge_runtime.summary()


@router.post(
    "/scan",
)
def scan_project(
    path: str,
):
    """Scan a project path into the runtime graph."""

    return knowledge_runtime.scan_project(
        path
    )
