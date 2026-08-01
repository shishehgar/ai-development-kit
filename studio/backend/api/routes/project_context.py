"""Project context API."""

from fastapi import APIRouter


from studio.backend.services.project_registry import (
    project_registry,
)



router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)



@router.get(
    "/context"
)
def list_project_context():

    return [
        {
            "id": project.id,
            "name": project.name,
            "path": project.path,
            "status": project.status,
        }

        for project

        in project_registry.list()

    ]
