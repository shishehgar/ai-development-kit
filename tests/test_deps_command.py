from pathlib import Path
from types import SimpleNamespace

from aidk.commands.deps_cmd import (
    DependenciesCommand,
)


def test_dependencies_command(
    tmp_path: Path,
    capsys,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "requirements.txt"
    ).write_text(
        "requests==2.32.0\n",
        encoding="utf-8",
    )

    command = DependenciesCommand()

    result = command.run(
        SimpleNamespace(
            path=str(project),
            json=False,
            duplicates_only=False,
        )
    )

    output = capsys.readouterr().out

    assert result == 0
    assert "requests" in output
    assert "Dependencies: 1" in output


def test_dependencies_command_missing_path(
    tmp_path: Path,
    capsys,
) -> None:
    command = DependenciesCommand()

    result = command.run(
        SimpleNamespace(
            path=str(
                tmp_path / "missing"
            ),
            json=False,
            duplicates_only=False,
        )
    )

    output = capsys.readouterr().out

    assert result == 1
    assert "Path not found" in output
