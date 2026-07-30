from pathlib import Path
from types import SimpleNamespace

from aidk.commands.deps_lock_cmd import (
    DependenciesLockCommand,
)


def test_deps_lock_passes(
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

    result = DependenciesLockCommand().run(
        SimpleNamespace(
            path=str(project),
            json=False,
            fail_score=70,
            strict=False,
        )
    )

    output = capsys.readouterr().out

    assert result == 0
    assert "Lock score: 100/100" in output
    assert "Status: PASS" in output


def test_deps_lock_fails_missing_lock(
    tmp_path: Path,
    capsys,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "package.json"
    ).write_text(
        '{"name": "demo"}',
        encoding="utf-8",
    )

    result = DependenciesLockCommand().run(
        SimpleNamespace(
            path=str(project),
            json=False,
            fail_score=70,
            strict=False,
        )
    )

    output = capsys.readouterr().out

    assert result == 1
    assert "missing-lockfile" in output
    assert "Status: FAIL" in output


def test_deps_lock_strict(
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

    result = DependenciesLockCommand().run(
        SimpleNamespace(
            path=str(project),
            json=False,
            fail_score=70,
            strict=True,
        )
    )

    assert result == 1


def test_deps_lock_missing_path(
    tmp_path: Path,
    capsys,
) -> None:
    result = DependenciesLockCommand().run(
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
