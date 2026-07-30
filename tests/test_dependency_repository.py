from pathlib import Path

from aidk.db.dependency_repository import (
    DependencyRepository,
)
from aidk.db.engine import DatabaseEngine
from aidk.db.repository import WorkspaceRepository
from aidk.dependency.engine import DependencyEngine
from aidk.workspace.project import Project


def test_save_dependency_report(
    tmp_path: Path,
) -> None:
    database = tmp_path / "workspace.db"

    workspace_repository = WorkspaceRepository(
        DatabaseEngine(database)
    )

    dependency_repository = DependencyRepository(
        DatabaseEngine(database)
    )

    project_path = tmp_path / "demo"
    project_path.mkdir()

    (
        project_path / "requirements.txt"
    ).write_text(
        "requests==2.32.0\npytest>=8\n",
        encoding="utf-8",
    )

    project_id = workspace_repository.save_project(
        Project(
            name="demo",
            path=project_path,
            language="Python",
        )
    )

    report = DependencyEngine().inspect(
        project_path
    )

    dependency_repository.save_report(
        project_id,
        report,
    )

    stored = dependency_repository.get_report(
        project_id
    )

    assert stored is not None
    assert stored["total"] == 2
    assert stored["unique_total"] == 2
    assert len(stored["dependencies"]) == 2
    assert len(stored["files"]) == 1


def test_dependency_report_replaced(
    tmp_path: Path,
) -> None:
    database = tmp_path / "workspace.db"

    workspace_repository = WorkspaceRepository(
        DatabaseEngine(database)
    )

    dependency_repository = DependencyRepository(
        DatabaseEngine(database)
    )

    project_path = tmp_path / "demo"
    project_path.mkdir()

    requirements = (
        project_path / "requirements.txt"
    )

    requirements.write_text(
        "requests==2.32.0\n",
        encoding="utf-8",
    )

    project_id = workspace_repository.save_project(
        Project(
            name="demo",
            path=project_path,
        )
    )

    dependency_repository.save_report(
        project_id,
        DependencyEngine().inspect(
            project_path
        ),
    )

    requirements.write_text(
        "fastapi>=0.100\n",
        encoding="utf-8",
    )

    dependency_repository.save_report(
        project_id,
        DependencyEngine().inspect(
            project_path
        ),
    )

    stored = dependency_repository.get_report(
        project_id
    )

    assert stored is not None
    assert stored["total"] == 1
    assert (
        stored["dependencies"][0]["name"]
        == "fastapi"
    )


def test_find_dependency(
    tmp_path: Path,
) -> None:
    database = tmp_path / "workspace.db"

    workspace_repository = WorkspaceRepository(
        DatabaseEngine(database)
    )

    dependency_repository = DependencyRepository(
        DatabaseEngine(database)
    )

    project_path = tmp_path / "demo"
    project_path.mkdir()

    (
        project_path / "requirements.txt"
    ).write_text(
        "requests==2.32.0\n",
        encoding="utf-8",
    )

    project_id = workspace_repository.save_project(
        Project(
            name="demo",
            path=project_path,
        )
    )

    dependency_repository.save_report(
        project_id,
        DependencyEngine().inspect(
            project_path
        ),
    )

    matches = dependency_repository.find_dependency(
        "requests"
    )

    assert len(matches) == 1
    assert matches[0]["project_name"] == "demo"
