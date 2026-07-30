"""Application service container for AIDK."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from aidk.application.doctor_service import DoctorService
from aidk.application.workspace_service import WorkspaceService


@dataclass(frozen=True)
class ApplicationServices:
    """Services shared by AIDK interfaces."""

    doctor: DoctorService
    workspace: WorkspaceService


def build_services(
    *,
    workspace: Path | None = None,
    projects_root: Path | None = None,
) -> ApplicationServices:
    """Build the application service container."""

    return ApplicationServices(
        doctor=DoctorService(
            workspace=workspace,
        ),
        workspace=WorkspaceService(
            root=projects_root,
        ),
    )


services = build_services()
