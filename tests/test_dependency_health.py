from pathlib import Path

from aidk.dependency.engine import (
    DependencyEngine,
)
from aidk.dependency.health import (
    DependencyHealthAnalyzer,
    Severity,
)


def test_exact_version_is_healthy(
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

    dependency_report = (
        DependencyEngine().inspect(project)
    )

    health_report = (
        DependencyHealthAnalyzer().analyze(
            dependency_report
        )
    )

    assert health_report.score == 100
    assert health_report.issues == []
    assert health_report.healthy is True


def test_unpinned_dependency_is_high_risk(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "requirements.txt"
    ).write_text(
        "requests\n",
        encoding="utf-8",
    )

    dependency_report = (
        DependencyEngine().inspect(project)
    )

    health_report = (
        DependencyHealthAnalyzer().analyze(
            dependency_report
        )
    )

    assert health_report.high_total == 1
    assert health_report.score == 85
    assert health_report.healthy is False


def test_version_range_is_low_risk(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "requirements.txt"
    ).write_text(
        "requests>=2.30\n",
        encoding="utf-8",
    )

    dependency_report = (
        DependencyEngine().inspect(project)
    )

    health_report = (
        DependencyHealthAnalyzer().analyze(
            dependency_report
        )
    )

    assert health_report.low_total == 1
    assert health_report.score == 98


def test_conflicting_versions_are_high_risk(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "requirements.txt"
    ).write_text(
        "requests==2.31.0\n",
        encoding="utf-8",
    )

    (
        project / "pyproject.toml"
    ).write_text(
        """
[project]
name = "demo"
dependencies = [
    "requests==2.32.0",
]
""".strip(),
        encoding="utf-8",
    )

    dependency_report = (
        DependencyEngine().inspect(project)
    )

    health_report = (
        DependencyHealthAnalyzer().analyze(
            dependency_report
        )
    )

    issues = {
        issue.issue_type: issue
        for issue in health_report.issues
    }

    assert "version-conflict" in issues
    assert (
        issues["version-conflict"].severity
        == Severity.HIGH
    )


def test_remote_git_without_commit_is_high_risk(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "requirements.txt"
    ).write_text(
        (
            "example @ "
            "git+https://github.com/org/repo.git\n"
        ),
        encoding="utf-8",
    )

    dependency_report = (
        DependencyEngine().inspect(project)
    )

    health_report = (
        DependencyHealthAnalyzer().analyze(
            dependency_report
        )
    )

    assert any(
        issue.issue_type == "remote-source"
        and issue.severity == Severity.HIGH
        for issue in health_report.issues
    )


def test_dev_dependency_in_runtime_group(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "requirements.txt"
    ).write_text(
        "pytest==9.1.1\n",
        encoding="utf-8",
    )

    dependency_report = (
        DependencyEngine().inspect(project)
    )

    health_report = (
        DependencyHealthAnalyzer().analyze(
            dependency_report
        )
    )

    assert any(
        issue.issue_type
        == "dev-runtime-mismatch"
        for issue in health_report.issues
    )
