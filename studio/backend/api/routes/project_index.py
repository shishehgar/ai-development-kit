"""Project indexing API routes."""

from __future__ import annotations


from fastapi import APIRouter, HTTPException


from studio.backend.services.project_index import (
    project_index_service,
)


from studio.backend.services.project_registry import (
    project_registry,
)


router = APIRouter(
    prefix="/projects",
    tags=["project-index"],
)



@router.post(
    "/{project_id}/index",
)
def index_project(
    project_id: str,
):

    project = project_registry.get(
        project_id
    )


    if project is None:

        raise HTTPException(
            status_code=404,
            detail=(
                f"Project '{project_id}' "
                "not found."
            ),
        )


    result = (
        project_index_service.index_project(
            project_id,
            project.path,
        )
    )


    return {
        "status": "indexed",
        **result,
    }
