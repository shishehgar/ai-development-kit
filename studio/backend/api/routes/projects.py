"""Project routes."""

from __future__ import annotations

from fastapi import APIRouter

from studio.backend.schemas.projects import (
    ProjectPathRequest,
    ProjectPathResult,
    ProjectRegistryItem,
)
from studio.backend.services.project_paths import ProjectPathService

from studio.backend.services.project_registry import (
    project_registry,
)

router = APIRouter(prefix="/projects", tags=["projects"])
service = ProjectPathService()


@router.post("/validate-path", response_model=ProjectPathResult)
def validate_project_path(
    request: ProjectPathRequest,
) -> ProjectPathResult:
    return service.validate(request.path)


@router.get(
    "/registry",
    response_model=list[ProjectRegistryItem],
)
def list_registered_projects():

    return [

        ProjectRegistryItem(

            id=project.id,

            name=project.name,

            path=project.path,

            status=project.status,

        )

        for project in project_registry.list()

    ]

