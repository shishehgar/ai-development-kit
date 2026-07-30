from pathlib import Path
from types import SimpleNamespace

from aidk.commands.db_cmd import DatabaseCommand
from aidk.db.engine import DatabaseEngine
from aidk.db.repository import WorkspaceRepository
from aidk.workspace.project import Project


def test_db_status(
    tmp_path: Path,
    capsys,
) -> None:
    database = tmp_path / "workspace.db"

    command = DatabaseCommand()

    result = command.run(
        SimpleNamespace(
            database=database,
            db_command="status",
        )
    )

    output = capsys.readouterr().out

    assert result == 0
    assert "Schema version: 2" in output
    assert "Projects: 0" in output


def test_db_list(
    tmp_path: Path,
    capsys,
) -> None:
    database = tmp_path / "workspace.db"

    repository = WorkspaceRepository(
        DatabaseEngine(database)
    )

    repository.save_project(
        Project(
            name="demo",
            path=tmp_path / "demo",
            language="Python",
        )
    )

    command = DatabaseCommand()

    result = command.run(
        SimpleNamespace(
            database=database,
            db_command="list",
            json=False,
        )
    )

    output = capsys.readouterr().out

    assert result == 0
    assert "demo" in output
    assert "Python" in output


def test_db_show_missing_project(
    tmp_path: Path,
    capsys,
) -> None:
    command = DatabaseCommand()

    result = command.run(
        SimpleNamespace(
            database=tmp_path / "workspace.db",
            db_command="show",
            name="missing",
            json=False,
        )
    )

    output = capsys.readouterr().out

    assert result == 1
    assert "Project not found" in output


def test_db_clear_requires_confirmation(
    tmp_path: Path,
    capsys,
) -> None:
    command = DatabaseCommand()

    result = command.run(
        SimpleNamespace(
            database=tmp_path / "workspace.db",
            db_command="clear",
            yes=False,
        )
    )

    output = capsys.readouterr().out

    assert result == 1
    assert "--yes" in output
