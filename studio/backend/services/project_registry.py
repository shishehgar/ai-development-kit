"""Project registry service."""

from __future__ import annotations

import os
from threading import RLock

from studio.backend.models.project import (
    ProjectInfo,
)


DEFAULT_PROJECT_ID = "ai-development-kit"

DEFAULT_PROJECT_NAME = "AIDK Studio"

DEFAULT_HOST_PROJECT_ROOT = (
    "/home/ubuntu/my_services/"
    "projects/ai-development-kit"
)


def get_default_project_root() -> str:
    """
    Return the configured default project path.

    The environment variable allows the same code to work in both
    environments:

    Host:
        /home/ubuntu/my_services/projects/ai-development-kit

    Docker:
        /app
    """

    configured_path = os.getenv(
        "AIDK_PROJECT_ROOT",
        DEFAULT_HOST_PROJECT_ROOT,
    ).strip()

    return (
        configured_path
        or DEFAULT_HOST_PROJECT_ROOT
    )


class ProjectRegistry:
    """Store projects available to AIDK Studio."""

    def __init__(self) -> None:
        """Initialize an empty thread-safe registry."""

        self._projects: dict[
            str,
            ProjectInfo,
        ] = {}

        self._lock = RLock()

    def register(
        self,
        project: ProjectInfo,
    ) -> None:
        """Register or replace a project."""

        with self._lock:
            self._projects[
                project.id
            ] = project

    def get(
        self,
        project_id: str,
    ) -> ProjectInfo | None:
        """Return a project by identifier."""

        normalized_id = project_id.strip()

        if not normalized_id:
            return None

        with self._lock:
            return self._projects.get(
                normalized_id
            )

    def list(
        self,
    ) -> list[ProjectInfo]:
        """Return all registered projects."""

        with self._lock:
            return list(
                self._projects.values()
            )


project_registry = ProjectRegistry()


project_registry.register(
    ProjectInfo(
        id=DEFAULT_PROJECT_ID,
        name=DEFAULT_PROJECT_NAME,
        path=get_default_project_root(),
        status="registered",
    )
)
