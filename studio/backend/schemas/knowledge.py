"""Knowledge API schemas."""

from __future__ import annotations

from pydantic import BaseModel


class KnowledgeSummaryResponse(
    BaseModel
):

    entities: int

    relations: int

    projects: int

    modules: int

    symbols: int
