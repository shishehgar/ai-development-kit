"""Tests for the AIDK application service container."""

from __future__ import annotations

from pathlib import Path

from aidk.application.audit_service import AuditService
from aidk.application.container import (
    ApplicationServices,
    build_services,
    services,
)
from aidk.application.doctor_service import DoctorService
from aidk.application.git_report_service import (
    GitReportService,
)
from aidk.application.git_service import GitService
from aidk.application.workspace_service import WorkspaceService


def test_default_container_has_services() -> None:
    assert isinstance(
        services,
        ApplicationServices,
    )
    assert isinstance(
        services.doctor,
        DoctorService,
    )
    assert isinstance(
        services.workspace,
        WorkspaceService,
    )
    assert isinstance(
        services.audit,
        AuditService,
    )
    assert isinstance(
        services.git,
        GitService,
    )
    assert isinstance(
        services.git_report,
        GitReportService,
    )


def test_container_accepts_custom_paths(
    tmp_path: Path,
) -> None:
    system_root = tmp_path / "system"
    projects_root = tmp_path / "projects"
    git_path = tmp_path / "repository"

    system_root.mkdir()
    projects_root.mkdir()
    git_path.mkdir()

    container = build_services(
        workspace=system_root,
        projects_root=projects_root,
        git_path=git_path,
    )

    assert container.doctor.workspace == (
        system_root.resolve()
    )
    assert container.workspace.root == (
        projects_root.resolve()
    )
    assert container.git.path == (
        git_path.resolve()
    )


def test_services_share_workspace_instance(
    tmp_path: Path,
) -> None:
    container = build_services(
        projects_root=tmp_path,
    )

    assert (
        container.audit.workspace_service
        is container.workspace
    )

    assert (
        container.git_report.workspace_service
        is container.workspace
    )
