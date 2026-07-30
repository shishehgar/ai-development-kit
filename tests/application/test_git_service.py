"""Tests for the structured Git service."""

from __future__ import annotations

import subprocess
from pathlib import Path

from aidk.application.git_service import GitService


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


def test_non_git_directory(
    tmp_path: Path,
) -> None:
    report = GitService(
        path=tmp_path,
    ).run()

    assert report.path == str(
        tmp_path.resolve()
    )
    assert report.exists is False


def test_clean_git_repository(
    tmp_path: Path,
) -> None:
    run_git(
        tmp_path,
        "init",
        "-b",
        "main",
    )

    report = GitService(
        path=tmp_path,
    ).run()

    assert report.exists is True
    assert report.branch == "main"
    assert report.clean is True


def test_untracked_file_is_reported(
    tmp_path: Path,
) -> None:
    run_git(
        tmp_path,
        "init",
        "-b",
        "main",
    )

    file_path = tmp_path / "example.txt"
    file_path.write_text(
        "example",
        encoding="utf-8",
    )

    report = GitService(
        path=tmp_path,
    ).run()

    assert report.exists is True
    assert report.clean is False
    assert report.untracked_files == 1


def test_git_report_is_serializable(
    tmp_path: Path,
) -> None:
    report = GitService(
        path=tmp_path,
    ).run()

    payload = report.to_dict()

    assert payload["path"] == str(
        tmp_path.resolve()
    )
    assert "exists" in payload
    assert "branch" in payload
    assert "remote_url" in payload
