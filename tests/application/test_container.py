"""Tests for the AIDK application service container."""

from __future__ import annotations

from pathlib import Path

from aidk.application.container import (
    ApplicationServices,
    build_services,
    services,
)
from aidk.application.doctor_service import DoctorService
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


def test_container_accepts_custom_paths(
    tmp_path: Path,
) -> None:
    system_root = tmp_path / "system"
    projects_root = tmp_path / "projects"

    system_root.mkdir()
    projects_root.mkdir()

    container = build_services(
        workspace=system_root,
        projects_root=projects_root,
    )

    doctor_report = container.doctor.run()
    workspace_report = container.workspace.run()

    assert doctor_report.workspace == str(
        system_root.resolve()
    )

    assert workspace_report.root == str(
        projects_root.resolve()
    )
