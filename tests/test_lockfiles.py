from pathlib import Path

from aidk.dependency.lockfiles import (
    LockfileAnalyzer,
)


def test_poetry_lockfile_present(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "pyproject.toml"
    ).write_text(
        """
[tool.poetry]
name = "demo"
version = "0.1.0"
""".strip(),
        encoding="utf-8",
    )

    (
        project / "poetry.lock"
    ).write_text(
        "# lock",
        encoding="utf-8",
    )

    report = LockfileAnalyzer().analyze(
        project
    )

    assert "poetry" in report.package_managers
    assert "poetry.lock" in report.lockfiles
    assert report.healthy is True


def test_poetry_lockfile_missing(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "pyproject.toml"
    ).write_text(
        """
[tool.poetry]
name = "demo"
version = "0.1.0"
""".strip(),
        encoding="utf-8",
    )

    report = LockfileAnalyzer().analyze(
        project
    )

    assert report.healthy is False
    assert any(
        issue.issue_type == "missing-lockfile"
        for issue in report.issues
    )


def test_pinned_requirements(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "requirements.txt"
    ).write_text(
        "requests==2.32.0\n",
        encoding="utf-8",
    )

    report = LockfileAnalyzer().analyze(
        project
    )

    assert report.score == 100
    assert report.issues == []


def test_unpinned_requirements(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "requirements.txt"
    ).write_text(
        "requests>=2.30\nfastapi\n",
        encoding="utf-8",
    )

    report = LockfileAnalyzer().analyze(
        project
    )

    assert any(
        issue.issue_type
        == "requirements-not-locked"
        for issue in report.issues
    )


def test_node_lockfile_missing(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "package.json"
    ).write_text(
        """
{
  "name": "demo",
  "dependencies": {
    "express": "^4.0.0"
  }
}
""".strip(),
        encoding="utf-8",
    )

    report = LockfileAnalyzer().analyze(
        project
    )

    assert report.healthy is False
    assert any(
        issue.issue_type == "missing-lockfile"
        for issue in report.issues
    )


def test_node_package_manager_mismatch(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "package.json"
    ).write_text(
        """
{
  "name": "demo",
  "packageManager": "pnpm@9.0.0"
}
""".strip(),
        encoding="utf-8",
    )

    (
        project / "package-lock.json"
    ).write_text(
        """
{
  "name": "demo",
  "lockfileVersion": 3
}
""".strip(),
        encoding="utf-8",
    )

    report = LockfileAnalyzer().analyze(
        project
    )

    assert any(
        issue.issue_type
        == "package-manager-mismatch"
        for issue in report.issues
    )


def test_multiple_node_lockfiles(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "package.json"
    ).write_text(
        '{"name": "demo"}',
        encoding="utf-8",
    )

    (
        project / "package-lock.json"
    ).write_text(
        '{"lockfileVersion": 3}',
        encoding="utf-8",
    )

    (
        project / "yarn.lock"
    ).write_text(
        "# yarn",
        encoding="utf-8",
    )

    report = LockfileAnalyzer().analyze(
        project
    )

    assert any(
        issue.issue_type
        == "multiple-node-lockfiles"
        for issue in report.issues
    )


def test_invalid_package_lock(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "package.json"
    ).write_text(
        '{"name": "demo"}',
        encoding="utf-8",
    )

    (
        project / "package-lock.json"
    ).write_text(
        "{invalid",
        encoding="utf-8",
    )

    report = LockfileAnalyzer().analyze(
        project
    )

    assert any(
        issue.issue_type
        == "invalid-lockfile"
        and issue.severity == "critical"
        for issue in report.issues
    )


def test_ignored_lockfile(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "package.json"
    ).write_text(
        '{"name": "demo"}',
        encoding="utf-8",
    )

    (
        project / "package-lock.json"
    ).write_text(
        '{"lockfileVersion": 3}',
        encoding="utf-8",
    )

    (
        project / ".gitignore"
    ).write_text(
        "package-lock.json\n",
        encoding="utf-8",
    )

    report = LockfileAnalyzer().analyze(
        project
    )

    assert any(
        issue.issue_type == "ignored-lockfile"
        for issue in report.issues
    )
