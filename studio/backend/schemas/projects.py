"""Project API schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ProjectPathRequest(BaseModel):
    path: str = Field(min_length=1)


class ProjectPathResult(BaseModel):
    path: str
    exists: bool
    is_directory: bool
    is_git_repository: bool
    allowed: bool
    message: str


class ProjectIndexResponse(BaseModel):
    """Project indexing result."""

    project: str

    entities: int

    relations: int

    status: str


class ProjectRegistryItem(BaseModel):
    """Registered project information."""

    id: str

    name: str

    path: str

    status: str

