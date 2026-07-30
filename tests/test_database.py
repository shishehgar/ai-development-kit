from pathlib import Path

from aidk.db.engine import DatabaseEngine
from aidk.db.repository import WorkspaceRepository
from aidk.workspace.project import Project


def test_database_initialization(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "workspace.db"

    engine = DatabaseEngine(database_path)
    engine.initialize()

    assert database_path.exists()


def test_repository_saves_project(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "workspace.db"

    repository = WorkspaceRepository(
        DatabaseEngine(database_path)
    )

    project = Project(
        name="demo",
        path=tmp_path / "demo",
        language="Python",
    )

    project.intelligence_score = 70
    project.readme = True
    project.tests = True

    project_id = repository.save_project(project)

    assert project_id > 0

    stored = repository.get_project("demo")

    assert stored is not None
    assert stored["name"] == "demo"
    assert stored["language"] == "Python"
    assert stored["engineering_score"] == 70


def test_repository_lists_projects(
    tmp_path: Path,
) -> None:
    repository = WorkspaceRepository(
        DatabaseEngine(
            tmp_path / "workspace.db"
        )
    )

    first = Project(
        name="alpha",
        path=tmp_path / "alpha",
    )

    second = Project(
        name="beta",
        path=tmp_path / "beta",
    )

    repository.save_projects(
        [first, second]
    )

    projects = repository.list_projects()

    assert len(projects) == 2
    assert projects[0]["name"] == "alpha"
    assert projects[1]["name"] == "beta"


def test_repository_clear(
    tmp_path: Path,
) -> None:
    repository = WorkspaceRepository(
        DatabaseEngine(
            tmp_path / "workspace.db"
        )
    )

    repository.save_project(
        Project(
            name="demo",
            path=tmp_path / "demo",
        )
    )

    repository.clear()

    assert repository.list_projects() == []
