"""Tests for the structured Workspace service."""

from __future__ import annotations

from pathlib import Path

from aidk.application.workspace_service import (
    WorkspaceService,
)


def test_empty_workspace_returns_empty_report(
    tmp_path: Path,
) -> None:
    report = WorkspaceService(
        root=tmp_path,
    ).run()

    assert report.root == str(
        tmp_path.resolve()
    )
    assert report.project_count == 0
    assert report.projects == ()


def test_workspace_discovers_project_directory(
    tmp_path: Path,
) -> None:
    project = tmp_path / "sample-project"
    project.mkdir()

    report = WorkspaceService(
        root=tmp_path,
    ).run()

    assert report.project_count == 1
    assert report.projects[0].name == (
        "sample-project"
    )
    assert report.projects[0].path == str(
        project.resolve()
    )


def test_workspace_skips_hidden_directory(
    tmp_path: Path,
) -> None:
    hidden = tmp_path / ".hidden-project"
    hidden.mkdir()

    report = WorkspaceService(
        root=tmp_path,
    ).run()

    assert report.project_count == 0


def test_workspace_report_is_serializable(
    tmp_path: Path,
) -> None:
    project = tmp_path / "serializable"
    project.mkdir()

    report = WorkspaceService(
        root=tmp_path,
    ).run()

    payload = report.to_dict()

    assert payload["root"] == str(
        tmp_path.resolve()
    )
    assert payload["project_count"] == 1
    assert isinstance(
        payload["projects"],
        list,
    )
