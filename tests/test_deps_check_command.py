from pathlib import Path
from types import SimpleNamespace

from aidk.commands.deps_check_cmd import (
    DependenciesCheckCommand,
)


def test_deps_check_passes_exact_versions(
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

    result = DependenciesCheckCommand().run(
        SimpleNamespace(
            path=str(project),
            json=False,
            fail_score=70,
            strict=False,
        )
    )

    output = capsys.readouterr().out

    assert result == 0
    assert "Health score: 100/100" in output
    assert "Status: PASS" in output


def test_deps_check_fails_unpinned(
    tmp_path: Path,
    capsys,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "requirements.txt"
    ).write_text(
        "requests\n",
        encoding="utf-8",
    )

    result = DependenciesCheckCommand().run(
        SimpleNamespace(
            path=str(project),
            json=False,
            fail_score=70,
            strict=False,
        )
    )

    output = capsys.readouterr().out

    assert result == 1
    assert "unpinned" in output
    assert "Status: FAIL" in output


def test_deps_check_strict_mode(
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

    result = DependenciesCheckCommand().run(
        SimpleNamespace(
            path=str(project),
            json=False,
            fail_score=70,
            strict=True,
        )
    )

    assert result == 1


def test_deps_check_missing_path(
    tmp_path: Path,
    capsys,
) -> None:
    result = DependenciesCheckCommand().run(
        SimpleNamespace(
            path=str(
                tmp_path / "missing"
            ),
            json=False,
            fail_score=70,
            strict=False,
        )
    )

    output = capsys.readouterr().out

    assert result == 1
    assert "Path not found" in output
