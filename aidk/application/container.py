"""Application service container for AIDK."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from aidk.application.audit_service import AuditService
from aidk.application.doctor_service import DoctorService
from aidk.application.git_service import GitService
from aidk.application.workspace_service import WorkspaceService


@dataclass(frozen=True)
class ApplicationServices:
    """Services shared by AIDK interfaces."""

    doctor: DoctorService
    workspace: WorkspaceService
    audit: AuditService
    git: GitService


def build_services(
    *,
    workspace: Path | None = None,
    projects_root: Path | None = None,
    git_path: Path | None = None,
) -> ApplicationServices:
    """Build the application service container."""

    workspace_service = WorkspaceService(
        root=projects_root,
    )

    return ApplicationServices(
        doctor=DoctorService(
            workspace=workspace,
        ),
        workspace=workspace_service,
        audit=AuditService(
            workspace_service=workspace_service,
        ),
        git=GitService(
            path=git_path,
        ),
    )


services = build_services()
