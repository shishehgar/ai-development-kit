"""Tests for the structured Doctor service."""

from __future__ import annotations

from pathlib import Path

from aidk.application.doctor_service import DoctorService


def test_doctor_report_is_structured(
    tmp_path: Path,
) -> None:
    report = DoctorService(
        workspace=tmp_path,
    ).run()

    assert report.workspace == str(tmp_path.resolve())
    assert report.health_score >= 0
    assert report.health_score <= 100
    assert report.status in {
        "healthy",
        "degraded",
        "unhealthy",
    }
    assert report.checks


def test_doctor_contains_workspace_check(
    tmp_path: Path,
) -> None:
    report = DoctorService(
        workspace=tmp_path,
    ).run()

    workspace_check = next(
        check
        for check in report.checks
        if check.key == "workspace"
    )

    assert workspace_check.status == "passed"
    assert workspace_check.required is True


def test_missing_workspace_is_failed(
    tmp_path: Path,
) -> None:
    missing = tmp_path / "not-created"

    report = DoctorService(
        workspace=missing,
    ).run()

    workspace_check = next(
        check
        for check in report.checks
        if check.key == "workspace"
    )

    assert workspace_check.status == "failed"
