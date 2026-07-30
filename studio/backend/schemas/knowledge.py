"""Knowledge API schemas."""

from __future__ import annotations

from pydantic import BaseModel


class KnowledgeSummaryResponse(
    BaseModel
):
    """Knowledge graph statistics."""

    entities: int

    relations: int

    projects: int

    modules: int

    symbols: int



class KnowledgeHealthResponse(
    BaseModel
):
    """Knowledge service health."""

    status: str

    service: str
