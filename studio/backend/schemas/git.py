"""Git API schemas."""

from __future__ import annotations

from pydantic import BaseModel


class GitReportResponse(BaseModel):
    path: str
    exists: bool
    repository_root: str
    branch: str
    default_branch: str
    clean: bool
    modified_files: int
    staged_files: int
    untracked_files: int
    remote: bool
    remote_name: str
    remote_url: str
    last_commit_hash: str
    last_commit_author: str
    last_commit_date: str
    ahead: int
    behind: int
