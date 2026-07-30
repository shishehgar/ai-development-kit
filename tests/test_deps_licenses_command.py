from pathlib import Path
from types import SimpleNamespace

from aidk.commands.deps_licenses_cmd import (
    DependenciesLicensesCommand,
)


def test_license_command_passes(
    tmp_path: Path,
    capsys,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "poetry.lock"
    ).write_text(
        """
[[package]]
name = "requests"
version = "2.32.0"
license = "Apache-2.0"
""".strip(),
        encoding="utf-8",
    )

    result = DependenciesLicensesCommand().run(
        SimpleNamespace(
            path=str(project),
            json=False,
            allow_unknown=False,
            deny_category=None,
            deny_license=None,
        )
    )

    output = capsys.readouterr().out

    assert result == 0
    assert "Status: PASS" in output
    assert "Apache-2.0" in output


def test_license_command_fails(
    tmp_path: Path,
    capsys,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "poetry.lock"
    ).write_text(
        """
[[package]]
name = "copyleft"
version = "1.0.0"
license = "GPL-3.0"
""".strip(),
        encoding="utf-8",
    )

    result = DependenciesLicensesCommand().run(
        SimpleNamespace(
            path=str(project),
            json=False,
            allow_unknown=False,
            deny_category=None,
            deny_license=None,
        )
    )

    output = capsys.readouterr().out

    assert result == 1
    assert "Status: FAIL" in output
    assert "GPL-3.0" in output


def test_license_command_allow_unknown(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "poetry.lock"
    ).write_text(
        """
[[package]]
name = "custom"
version = "1.0.0"
license = "Custom License"
""".strip(),
        encoding="utf-8",
    )

    result = DependenciesLicensesCommand().run(
        SimpleNamespace(
            path=str(project),
            json=False,
            allow_unknown=True,
            deny_category=None,
            deny_license=None,
        )
    )

    assert result == 0


def test_license_command_missing_path(
    tmp_path: Path,
    capsys,
) -> None:
    result = DependenciesLicensesCommand().run(
        SimpleNamespace(
            path=str(
                tmp_path / "missing"
            ),
            json=False,
            allow_unknown=False,
            deny_category=None,
            deny_license=None,
        )
    )

    output = capsys.readouterr().out

    assert result == 1
    assert "Path not found" in output
