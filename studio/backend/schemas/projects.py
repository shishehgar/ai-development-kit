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
