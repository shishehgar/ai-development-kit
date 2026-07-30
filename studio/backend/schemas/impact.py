"""Impact analysis schemas."""

from __future__ import annotations

from pydantic import BaseModel


class ImpactEntityResponse(BaseModel):

    id: str

    name: str

    kind: str



class ImpactResponse(BaseModel):

    target_id: str

    affected_entities: list[ImpactEntityResponse]

    affected_files: int

    affected_modules: int

    affected_tests: int

    risk: str
