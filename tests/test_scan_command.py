from pathlib import Path
from types import SimpleNamespace

from aidk.commands.scan_cmd import ScanCommand
from aidk.db.engine import DatabaseEngine
from aidk.db.repository import WorkspaceRepository


def test_scan_command_empty_workspace(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "projects"
    workspace.mkdir()

    database = tmp_path / "workspace.db"

    command = ScanCommand()

    result = command.run(
        SimpleNamespace(
            path=str(workspace),
            database=database,
            clear=False,
            skip_dependencies=False,
        )
    )

    assert result == 0
    assert database.exists()

    repository = WorkspaceRepository(
        DatabaseEngine(database)
    )

    assert repository.list_projects() == []


def test_scan_command_saves_project(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "projects"
    workspace.mkdir()

    project = workspace / "demo"
    project.mkdir()

    (project / "README.md").write_text(
        "# Demo\n",
        encoding="utf-8",
    )

    (project / "main.py").write_text(
        "print('demo')\n",
        encoding="utf-8",
    )

    database = tmp_path / "workspace.db"

    command = ScanCommand()

    result = command.run(
        SimpleNamespace(
            path=str(workspace),
            database=database,
            clear=True,
            skip_dependencies=False,
        )
    )

    assert result == 0

    repository = WorkspaceRepository(
        DatabaseEngine(database)
    )

    stored = repository.get_project("demo")

    assert stored is not None
    assert stored["name"] == "demo"
    assert stored["path"] == str(project.resolve())
