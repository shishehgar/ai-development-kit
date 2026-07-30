from pathlib import Path

from aidk.dependency.engine import (
    DependencyEngine,
)


def test_requirements_parser(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "requirements.txt"
    ).write_text(
        "\n".join(
            (
                "requests==2.32.0",
                "fastapi>=0.100",
                "uvicorn[standard]~=0.30",
                "# comment",
                "",
            )
        ),
        encoding="utf-8",
    )

    report = DependencyEngine().inspect(
        project
    )

    assert report.total == 3
    assert report.unique_total == 3

    names = {
        dependency.name
        for dependency in report.dependencies
    }

    assert names == {
        "requests",
        "fastapi",
        "uvicorn",
    }


def test_requirements_dev_group(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "requirements-dev.txt"
    ).write_text(
        "pytest>=8\nruff==0.6\n",
        encoding="utf-8",
    )

    report = DependencyEngine().inspect(
        project
    )

    assert report.development_total == 2


def test_pyproject_pep621_parser(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "pyproject.toml"
    ).write_text(
        """
[project]
name = "demo"
dependencies = [
    "requests>=2",
    "pydantic>=2",
]

[project.optional-dependencies]
dev = [
    "pytest>=8",
]
""".strip(),
        encoding="utf-8",
    )

    report = DependencyEngine().inspect(
        project
    )

    assert report.total == 3
    assert report.optional_total == 1


def test_poetry_parser(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "pyproject.toml"
    ).write_text(
        """
[tool.poetry.dependencies]
python = "^3.10"
requests = "^2.32"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
""".strip(),
        encoding="utf-8",
    )

    report = DependencyEngine().inspect(
        project
    )

    names = {
        dependency.name
        for dependency in report.dependencies
    }

    assert "python" not in names
    assert "requests" in names
    assert "pytest" in names


def test_package_json_parser(
    tmp_path: Path,
) -> None:
    project = tmp_path / "demo"
    project.mkdir()

    (
        project / "package.json"
    ).write_text(
        """
{
  "dependencies": {
    "express": "^4.21.0"
  },
  "devDependencies": {
    "eslint": "^9.0.0"
  }
}
""".strip(),
        encoding="utf-8",
    )

    report = DependencyEngine().inspect(
        project
    )

    assert report.total == 2
    assert report.runtime_total == 1
    assert report.development_total == 1


def test_duplicate_detection(
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
    "requests>=2.32",
]
""".strip(),
        encoding="utf-8",
    )

    report = DependencyEngine().inspect(
        project
    )

    assert "requests" in report.duplicates
    assert len(
        report.duplicates["requests"]
    ) == 2
