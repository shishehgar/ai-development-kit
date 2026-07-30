"""Knowledge API routes."""

from __future__ import annotations

from fastapi import APIRouter

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
def knowledge_summary():

    """
    Temporary dashboard data.

    Later connected to
    KnowledgeQueryService.
    """

    return {

        "entities": 0,

        "relations": 0,

        "projects": 0,

        "modules": 0,

        "symbols": 0,
    }
