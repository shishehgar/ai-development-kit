"""Incremental reindex API schemas."""

from __future__ import annotations

from pydantic import BaseModel


class ReindexResponse(BaseModel):
    """Result of safe project reindexing."""

    project: str
    strategy: str
    reason: str
    changed_files: int
    added_files: int
    modified_files: int
    deleted_files: int
    renamed_files: int
    entities: int
    relations: int
