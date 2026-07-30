"""Tests for the structured Audit service."""

from __future__ import annotations

from pathlib import Path

from aidk.application.audit_service import (
    AuditService,
)
from aidk.application.workspace_service import (
    WorkspaceService,
)


def test_empty_workspace_returns_empty_audit(
    tmp_path: Path,
) -> None:
    service = AuditService(
        projects_root=tmp_path,
    )

    report = service.run()

    assert report.root == str(
        tmp_path.resolve()
    )
    assert report.total_projects == 0
    assert report.average_score == 0
    assert report.grade_distribution == {}
    assert report.critical_projects == ()


def test_audit_uses_shared_workspace_service(
    tmp_path: Path,
) -> None:
    workspace_service = WorkspaceService(
        root=tmp_path,
    )

    audit_service = AuditService(
        workspace_service=workspace_service,
    )

    assert (
        audit_service.workspace_service
        is workspace_service
    )


def test_audit_report_is_serializable(
    tmp_path: Path,
) -> None:
    project = tmp_path / "sample-project"
    project.mkdir()

    report = AuditService(
        projects_root=tmp_path,
    ).run()

    payload = report.to_dict()

    assert payload["root"] == str(
        tmp_path.resolve()
    )
    assert payload["total_projects"] == 1
    assert isinstance(
        payload["grade_distribution"],
        dict,
    )
    assert isinstance(
        payload["critical_projects"],
        list,
    )
    assert isinstance(
        payload["recommendations"],
        list,
    )


def test_project_without_components_is_reported(
    tmp_path: Path,
) -> None:
    project = tmp_path / "incomplete-project"
    project.mkdir()

    report = AuditService(
        projects_root=tmp_path,
    ).run()

    assert report.total_projects == 1
    assert report.missing_readme == 1
    assert report.missing_tests == 1
    assert report.missing_ai_config == 1
    assert report.missing_license == 1
    assert report.missing_docker == 1
