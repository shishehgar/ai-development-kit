"""
Dependency analysis engine.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from aidk.dependency.models import (
    Dependency,
    DependencyReport,
)

try:
    import tomllib
except ModuleNotFoundError:
    try:
        import tomli as tomllib
    except ModuleNotFoundError:
        tomllib = None


class DependencyEngine:

    REQUIREMENTS_FILES = (
        "requirements.txt",
        "requirements-dev.txt",
        "requirements-test.txt",
        "requirements-prod.txt",
        "constraints.txt",
    )

    def inspect(
        self,
        project_path: Path | str,
    ) -> DependencyReport:
        path = Path(
            project_path
        ).expanduser().resolve()

        report = DependencyReport(
            project_name=path.name,
            project_path=path,
        )

        self._parse_requirements_files(
            path,
            report,
        )

        self._parse_pyproject(
            path,
            report,
        )

        self._parse_pipfile(
            path,
            report,
        )

        self._parse_package_json(
            path,
            report,
        )

        report.duplicates = self._find_duplicates(
            report.dependencies
        )

        report.dependencies.sort(
            key=lambda dependency: (
                dependency.normalized_name,
                dependency.group,
                dependency.source,
            )
        )

        return report

    def inspect_many(
        self,
        project_paths,
    ) -> list[DependencyReport]:
        return [
            self.inspect(project_path)
            for project_path in project_paths
        ]

    def _parse_requirements_files(
        self,
        path: Path,
        report: DependencyReport,
    ) -> None:
        candidates = {
            path / filename
            for filename in self.REQUIREMENTS_FILES
        }

        requirements_directory = path / "requirements"

        if requirements_directory.is_dir():
            candidates.update(
                requirements_directory.glob("*.txt")
            )

        for file_path in sorted(candidates):
            if not file_path.is_file():
                continue

            report.files.append(file_path)

            try:
                dependencies = (
                    self._read_requirements_file(
                        file_path
                    )
                )
                report.dependencies.extend(
                    dependencies
                )
            except OSError as error:
                report.errors.append(
                    f"{file_path}: {error}"
                )

    def _read_requirements_file(
        self,
        file_path: Path,
    ) -> list[Dependency]:
        dependencies = []

        group = self._requirements_group(
            file_path
        )

        for raw_line in file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        ).splitlines():
            line = raw_line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            if line.startswith(("-r", "--requirement")):
                continue

            if line.startswith(("-c", "--constraint")):
                continue

            if line.startswith(("-e", "--editable")):
                dependency = self._parse_editable(
                    line,
                    file_path.name,
                    group,
                )

                if dependency:
                    dependencies.append(
                        dependency
                    )

                continue

            if line.startswith(
                (
                    "git+",
                    "http://",
                    "https://",
                    "file:",
                )
            ):
                dependency = self._parse_url_dependency(
                    line,
                    file_path.name,
                    group,
                )

                if dependency:
                    dependencies.append(
                        dependency
                    )

                continue

            dependency = self._parse_requirement_line(
                line,
                file_path.name,
                group,
            )

            if dependency:
                dependencies.append(
                    dependency
                )

        return dependencies

    @staticmethod
    def _requirements_group(
        file_path: Path,
    ) -> str:
        name = file_path.name.lower()

        if any(
            token in name
            for token in (
                "dev",
                "test",
                "lint",
                "docs",
            )
        ):
            return "development"

        return "runtime"

    @staticmethod
    def _parse_requirement_line(
        line: str,
        source: str,
        group: str,
    ) -> Dependency | None:
        line = line.split(
            " #",
            1,
        )[0].strip()

        marker_free = line.split(
            ";",
            1,
        )[0].strip()

        match = re.match(
            r"^([A-Za-z0-9_.-]+)"
            r"(?:\[[^\]]+\])?"
            r"\s*(.*)$",
            marker_free,
        )

        if not match:
            return None

        name = match.group(1)
        version = match.group(2).strip()

        return Dependency(
            name=name,
            version=version,
            source=source,
            group=group,
        )

    @staticmethod
    def _parse_editable(
        line: str,
        source: str,
        group: str,
    ) -> Dependency | None:
        value = re.sub(
            r"^(?:-e|--editable)\s+",
            "",
            line,
        ).strip()

        egg_match = re.search(
            r"[#&]egg=([A-Za-z0-9_.-]+)",
            value,
        )

        if egg_match:
            name = egg_match.group(1)
        else:
            name = Path(
                value.rstrip("/")
            ).name

        if not name:
            return None

        return Dependency(
            name=name,
            version=value,
            source=source,
            group=group,
        )

    @staticmethod
    def _parse_url_dependency(
        line: str,
        source: str,
        group: str,
    ) -> Dependency | None:
        egg_match = re.search(
            r"[#&]egg=([A-Za-z0-9_.-]+)",
            line,
        )

        if egg_match:
            name = egg_match.group(1)
        else:
            direct_match = re.match(
                r"^([A-Za-z0-9_.-]+)\s*@\s*(.+)$",
                line,
            )

            if direct_match:
                name = direct_match.group(1)
            else:
                name = Path(
                    line.split("#", 1)[0].rstrip("/")
                ).stem

        if not name:
            return None

        return Dependency(
            name=name,
            version=line,
            source=source,
            group=group,
        )

    def _parse_pyproject(
        self,
        path: Path,
        report: DependencyReport,
    ) -> None:
        file_path = path / "pyproject.toml"

        if not file_path.is_file():
            return

        report.files.append(file_path)

        if tomllib is None:
            report.errors.append(
                "pyproject.toml: tomllib is unavailable"
            )
            return

        try:
            with file_path.open("rb") as stream:
                data = tomllib.load(stream)
        except (OSError, ValueError) as error:
            report.errors.append(
                f"{file_path}: {error}"
            )
            return

        self._parse_pep621_dependencies(
            data,
            report,
            file_path.name,
        )

        self._parse_poetry_dependencies(
            data,
            report,
            file_path.name,
        )

        self._parse_uv_dependencies(
            data,
            report,
            file_path.name,
        )

    def _parse_pep621_dependencies(
        self,
        data: dict[str, Any],
        report: DependencyReport,
        source: str,
    ) -> None:
        project = data.get(
            "project",
            {},
        )

        for item in project.get(
            "dependencies",
            [],
        ):
            dependency = self._parse_requirement_line(
                str(item),
                source,
                "runtime",
            )

            if dependency:
                report.dependencies.append(
                    dependency
                )

        optional_dependencies = project.get(
            "optional-dependencies",
            {},
        )

        for group_name, items in optional_dependencies.items():
            for item in items:
                dependency = self._parse_requirement_line(
                    str(item),
                    source,
                    "development",
                )

                if dependency:
                    report.dependencies.append(
                        Dependency(
                            name=dependency.name,
                            version=dependency.version,
                            source=source,
                            group=str(group_name),
                            optional=True,
                        )
                    )

    def _parse_poetry_dependencies(
        self,
        data: dict[str, Any],
        report: DependencyReport,
        source: str,
    ) -> None:
        poetry = (
            data.get("tool", {})
            .get("poetry", {})
        )

        dependencies = poetry.get(
            "dependencies",
            {},
        )

        for name, value in dependencies.items():
            if name.lower() == "python":
                continue

            report.dependencies.append(
                self._dependency_from_toml_value(
                    name=name,
                    value=value,
                    source=source,
                    group="runtime",
                )
            )

        dev_dependencies = poetry.get(
            "dev-dependencies",
            {},
        )

        for name, value in dev_dependencies.items():
            report.dependencies.append(
                self._dependency_from_toml_value(
                    name=name,
                    value=value,
                    source=source,
                    group="development",
                )
            )

        groups = poetry.get(
            "group",
            {},
        )

        for group_name, group_data in groups.items():
            group_dependencies = group_data.get(
                "dependencies",
                {},
            )

            for name, value in group_dependencies.items():
                report.dependencies.append(
                    self._dependency_from_toml_value(
                        name=name,
                        value=value,
                        source=source,
                        group=str(group_name),
                    )
                )

    def _parse_uv_dependencies(
        self,
        data: dict[str, Any],
        report: DependencyReport,
        source: str,
    ) -> None:
        dependency_groups = data.get(
            "dependency-groups",
            {},
        )

        for group_name, items in dependency_groups.items():
            for item in items:
                dependency = self._parse_requirement_line(
                    str(item),
                    source,
                    str(group_name),
                )

                if dependency:
                    report.dependencies.append(
                        dependency
                    )

        uv = (
            data.get("tool", {})
            .get("uv", {})
        )

        dev_dependencies = uv.get(
            "dev-dependencies",
            [],
        )

        for item in dev_dependencies:
            dependency = self._parse_requirement_line(
                str(item),
                source,
                "development",
            )

            if dependency:
                report.dependencies.append(
                    dependency
                )

    @staticmethod
    def _dependency_from_toml_value(
        name: str,
        value: Any,
        source: str,
        group: str,
    ) -> Dependency:
        optional = False

        if isinstance(value, dict):
            optional = bool(
                value.get(
                    "optional",
                    False,
                )
            )

            version = str(
                value.get(
                    "version",
                    value.get(
                        "git",
                        value.get(
                            "path",
                            value.get(
                                "url",
                                "",
                            ),
                        ),
                    ),
                )
            )
        else:
            version = str(value)

        return Dependency(
            name=name,
            version=version,
            source=source,
            group=group,
            optional=optional,
        )

    def _parse_pipfile(
        self,
        path: Path,
        report: DependencyReport,
    ) -> None:
        file_path = path / "Pipfile"

        if not file_path.is_file():
            return

        report.files.append(file_path)

        if tomllib is None:
            report.errors.append(
                "Pipfile: tomllib is unavailable"
            )
            return

        try:
            with file_path.open("rb") as stream:
                data = tomllib.load(stream)
        except (OSError, ValueError) as error:
            report.errors.append(
                f"{file_path}: {error}"
            )
            return

        for section, group in (
            ("packages", "runtime"),
            ("dev-packages", "development"),
        ):
            for name, value in data.get(
                section,
                {},
            ).items():
                report.dependencies.append(
                    self._dependency_from_toml_value(
                        name=name,
                        value=value,
                        source=file_path.name,
                        group=group,
                    )
                )

    def _parse_package_json(
        self,
        path: Path,
        report: DependencyReport,
    ) -> None:
        file_path = path / "package.json"

        if not file_path.is_file():
            return

        report.files.append(file_path)

        try:
            data = json.loads(
                file_path.read_text(
                    encoding="utf-8",
                )
            )
        except (
            OSError,
            json.JSONDecodeError,
        ) as error:
            report.errors.append(
                f"{file_path}: {error}"
            )
            return

        for section, group in (
            ("dependencies", "runtime"),
            ("devDependencies", "development"),
            ("peerDependencies", "peer"),
            ("optionalDependencies", "optional"),
        ):
            for name, version in data.get(
                section,
                {},
            ).items():
                report.dependencies.append(
                    Dependency(
                        name=name,
                        version=str(version),
                        source=file_path.name,
                        group=group,
                        optional=(
                            section
                            == "optionalDependencies"
                        ),
                    )
                )

    @staticmethod
    def _find_duplicates(
        dependencies: list[Dependency],
    ) -> dict[str, list[Dependency]]:
        grouped: dict[
            str,
            list[Dependency],
        ] = {}

        for dependency in dependencies:
            grouped.setdefault(
                dependency.normalized_name,
                [],
            ).append(
                dependency
            )

        return {
            name: items
            for name, items in grouped.items()
            if len(items) > 1
        }
