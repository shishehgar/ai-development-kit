"""Tests for the workspace Git report service."""

from __future__ import annotations

import subprocess
from pathlib import Path

from aidk.application.git_report_service import (
    GitReportService,
)
from aidk.application.workspace_service import (
    WorkspaceService,
)


def run_git(
    path: Path,
    *args: str,
) -> None:
    subprocess.run(
        ["git", *args],
        cwd=path,
        check=True,
        capture_output=True,
        text=True,
    )


def test_empty_workspace_returns_empty_report(
    tmp_path: Path,
) -> None:
    report = GitReportService(
        projects_root=tmp_path,
    ).run()

    assert report.root == str(
        tmp_path.resolve()
    )
    assert report.total_projects == 0
    assert report.clean_repositories == 0
    assert report.dirty_repositories == 0
    assert report.branches == {}
    assert report.risks == ()


def test_clean_repository_is_counted(
    tmp_path: Path,
) -> None:
    project = tmp_path / "clean-project"
    project.mkdir()

    run_git(
        project,
        "init",
        "-b",
        "main",
    )

    report = GitReportService(
        projects_root=tmp_path,
    ).run()

    assert report.total_projects == 1
    assert report.clean_repositories == 1
    assert report.dirty_repositories == 0
    assert report.branches["main"] == 1


def test_dirty_repository_creates_risk(
    tmp_path: Path,
) -> None:
    project = tmp_path / "dirty-project"
    project.mkdir()

    run_git(
        project,
        "init",
        "-b",
        "main",
    )

    (project / "example.txt").write_text(
        "untracked",
        encoding="utf-8",
    )

    report = GitReportService(
        projects_root=tmp_path,
    ).run()

    assert report.total_projects == 1
    assert report.dirty_repositories == 1
    assert len(report.risks) == 1
    assert report.risks[0].project == (
        "dirty-project"
    )


def test_report_is_serializable(
    tmp_path: Path,
) -> None:
    report = GitReportService(
        projects_root=tmp_path,
    ).run()

    payload = report.to_dict()

    assert payload["root"] == str(
        tmp_path.resolve()
    )
    assert isinstance(
        payload["branches"],
        dict,
    )
    assert isinstance(
        payload["risks"],
        list,
    )


def test_service_accepts_shared_workspace(
    tmp_path: Path,
) -> None:
    workspace_service = WorkspaceService(
        root=tmp_path,
    )

    service = GitReportService(
        workspace_service=workspace_service,
    )

    assert (
        service.workspace_service
        is workspace_service
    )
