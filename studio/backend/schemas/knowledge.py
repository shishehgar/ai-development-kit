"""Knowledge API schemas."""

from pydantic import BaseModel


class KnowledgeSummaryResponse(
    BaseModel
):

    entities: int

    relations: int

    projects: int

    modules: int

    symbols: int



class KnowledgeHealthResponse(
    BaseModel
):

    status: str

    service: str
