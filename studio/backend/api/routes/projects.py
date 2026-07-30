"""Project management API routes."""

from __future__ import annotations

from fastapi import APIRouter

from studio.backend.schemas.projects import (
    ProjectPathRequest,
    ProjectPathResult,
)
from studio.backend.services.project_paths import ProjectPathService

router = APIRouter(prefix="/projects", tags=["projects"])
service = ProjectPathService()


@router.post("/validate-path", response_model=ProjectPathResult)
def validate_project_path(
    request: ProjectPathRequest,
) -> ProjectPathResult:
    return service.validate(request.path)
