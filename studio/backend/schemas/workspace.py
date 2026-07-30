"""Workspace API schemas."""

from __future__ import annotations

from pydantic import BaseModel


class WorkspaceProjectResponse(BaseModel):
    name: str
    path: str

    language: str

    git: bool
    docker: bool
    continue_config: bool

    readme: bool
    license: bool
    tests: bool

    score: int
    intelligence_score: int
    grade: str
    documentation_score: int

    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]


class WorkspaceReportResponse(BaseModel):

    root: str

    project_count: int

    projects: list[WorkspaceProjectResponse]
