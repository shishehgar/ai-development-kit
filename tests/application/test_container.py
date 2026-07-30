"""Tests for the AIDK application service container."""

from __future__ import annotations

from pathlib import Path

from aidk.application.container import (
    ApplicationServices,
    build_services,
    services,
)
from aidk.application.doctor_service import DoctorService


def test_default_container_has_doctor_service() -> None:
    assert isinstance(
        services,
        ApplicationServices,
    )

    assert isinstance(
        services.doctor,
        DoctorService,
    )


def test_container_can_use_custom_workspace(
    tmp_path: Path,
) -> None:
    container = build_services(
        workspace=tmp_path,
    )

    report = container.doctor.run()

    assert report.workspace == str(
        tmp_path.resolve()
    )


def test_container_instances_are_independent(
    tmp_path: Path,
) -> None:
    first_workspace = tmp_path / "first"
    second_workspace = tmp_path / "second"

    first_workspace.mkdir()
    second_workspace.mkdir()

    first = build_services(
        workspace=first_workspace,
    )

    second = build_services(
        workspace=second_workspace,
    )

    assert (
        first.doctor.workspace
        != second.doctor.workspace
    )
