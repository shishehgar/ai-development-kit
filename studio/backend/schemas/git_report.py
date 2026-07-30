"""Workspace Git report API schemas."""

from __future__ import annotations

from pydantic import BaseModel


class GitRiskResponse(BaseModel):
    project: str
    level: str
    reasons: list[str]


class GitWorkspaceReportResponse(BaseModel):
    root: str
    total_projects: int
    clean_repositories: int
    dirty_repositories: int
    branches: dict[str, int]
    remote_count: int
    no_remote_count: int
    risks: list[GitRiskResponse]
