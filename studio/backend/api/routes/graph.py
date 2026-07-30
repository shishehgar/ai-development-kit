"""Graph API routes."""

from fastapi import APIRouter

from studio.backend.services.graph_service import (
    build_graph_response,
)


router = APIRouter(
    prefix="/graph",
    tags=["graph"],
)


@router.get("")
def graph():

    return build_graph_response()
