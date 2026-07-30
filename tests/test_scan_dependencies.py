from pathlib import Path
from types import SimpleNamespace

from aidk.commands.scan_cmd import ScanCommand
from aidk.db.dependency_repository import (
    DependencyRepository,
)
from aidk.db.engine import DatabaseEngine


def test_scan_persists_dependencies(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "projects"
    workspace.mkdir()

    project = workspace / "demo"
    project.mkdir()

    (
        project / "requirements.txt"
    ).write_text(
        "requests==2.32.0\n",
        encoding="utf-8",
    )

    database = tmp_path / "workspace.db"

    result = ScanCommand().run(
        SimpleNamespace(
            path=str(workspace),
            database=database,
            clear=True,
            skip_dependencies=False,
        )
    )

    assert result == 0

    repository = DependencyRepository(
        DatabaseEngine(database)
    )

    report = repository.get_project_report(
        "demo"
    )

    assert report is not None
    assert report["total"] == 1
    assert (
        report["dependencies"][0]["name"]
        == "requests"
    )
