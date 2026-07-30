"""
Dependency license analysis.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from importlib import metadata
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:
    try:
        import tomli as tomllib
    except ModuleNotFoundError:
        tomllib = None


@dataclass(frozen=True)
class LicenseRecord:
    name: str
    version: str
    license: str
    category: str
    source: str
    allowed: bool
    reason: str = ""


@dataclass
class LicenseReport:
    project_name: str
    project_path: Path
    records: list[LicenseRecord] = field(
        default_factory=list
    )
    errors: list[str] = field(
        default_factory=list
    )

    @property
    def total(self) -> int:
        return len(self.records)

    @property
    def allowed_total(self) -> int:
        return sum(
            1
            for record in self.records
            if record.allowed
        )

    @property
    def denied_total(self) -> int:
        return sum(
            1
            for record in self.records
            if not record.allowed
        )

    @property
    def unknown_total(self) -> int:
        return sum(
            1
            for record in self.records
            if record.category == "unknown"
        )

    @property
    def compliant(self) -> bool:
        return (
            self.denied_total == 0
            and not self.errors
        )


class LicensePolicy:

    PERMISSIVE = {
        "mit",
        "bsd",
        "bsd-2-clause",
        "bsd-3-clause",
        "apache-2.0",
        "apache 2.0",
        "apache license 2.0",
        "isc",
        "zlib",
        "unlicense",
        "public domain",
        "cc0-1.0",
        "python-2.0",
        "psf",
        "mpl-2.0",
    }

    WEAK_COPYLEFT = {
        "lgpl",
        "lgpl-2.0",
        "lgpl-2.1",
        "lgpl-3.0",
        "mpl",
        "mpl-2.0",
        "epl",
        "epl-1.0",
        "epl-2.0",
        "cddl",
        "cddl-1.0",
    }

    STRONG_COPYLEFT = {
        "gpl",
        "gpl-2.0",
        "gpl-3.0",
        "agpl",
        "agpl-3.0",
        "sspl",
        "sspl-1.0",
    }

    PROPRIETARY = {
        "proprietary",
        "commercial",
        "closed source",
        "all rights reserved",
    }

    DEFAULT_DENIED_CATEGORIES = {
        "strong-copyleft",
        "proprietary",
    }

    def __init__(
        self,
        denied_categories: set[str] | None = None,
        denied_licenses: set[str] | None = None,
        allow_unknown: bool = False,
    ) -> None:
        self.denied_categories = (
            denied_categories
            if denied_categories is not None
            else set(
                self.DEFAULT_DENIED_CATEGORIES
            )
        )

        self.denied_licenses = {
            self.normalize(value)
            for value in (
                denied_licenses or set()
            )
        }

        self.allow_unknown = allow_unknown

    def evaluate(
        self,
        license_name: str,
    ) -> tuple[str, bool, str]:
        normalized = self.normalize(
            license_name
        )

        category = self.classify(
            normalized
        )

        if normalized in self.denied_licenses:
            return (
                category,
                False,
                "License is explicitly denied.",
            )

        if category in self.denied_categories:
            return (
                category,
                False,
                (
                    "License category is denied "
                    "by policy."
                ),
            )

        if (
            category == "unknown"
            and not self.allow_unknown
        ):
            return (
                category,
                False,
                (
                    "Unknown licenses are not "
                    "allowed."
                ),
            )

        return (
            category,
            True,
            "",
        )

    def classify(
        self,
        normalized_license: str,
    ) -> str:
        if not normalized_license:
            return "unknown"

        tokens = self._license_tokens(
            normalized_license
        )

        if any(
            token in self.PROPRIETARY
            for token in tokens
        ):
            return "proprietary"

        if any(
            token in self.STRONG_COPYLEFT
            for token in tokens
        ):
            return "strong-copyleft"

        if any(
            token in self.WEAK_COPYLEFT
            for token in tokens
        ):
            return "weak-copyleft"

        if any(
            token in self.PERMISSIVE
            for token in tokens
        ):
            return "permissive"

        if self._contains_pattern(
            normalized_license,
            (
                r"\bagpl\b",
                r"\bgpl\b",
                r"server side public license",
            ),
        ):
            return "strong-copyleft"

        if self._contains_pattern(
            normalized_license,
            (
                r"\blgpl\b",
                r"\bmpl\b",
                r"\bepl\b",
                r"\bcddl\b",
            ),
        ):
            return "weak-copyleft"

        if self._contains_pattern(
            normalized_license,
            (
                r"\bmit\b",
                r"\bbsd\b",
                r"\bapache\b",
                r"\bisc\b",
                r"\bzlib\b",
            ),
        ):
            return "permissive"

        return "unknown"

    @staticmethod
    def normalize(
        value: str | None,
    ) -> str:
        if value is None:
            return ""

        normalized = str(value).strip().lower()

        normalized = normalized.replace(
            "_",
            "-",
        )

        normalized = re.sub(
            r"\s+",
            " ",
            normalized,
        )

        return normalized

    @staticmethod
    def _license_tokens(
        value: str,
    ) -> set[str]:
        parts = re.split(
            r"\s+(?:or|and)\s+|[(),/|]",
            value,
        )

        return {
            part.strip()
            for part in parts
            if part.strip()
        }

    @staticmethod
    def _contains_pattern(
        value: str,
        patterns: tuple[str, ...],
    ) -> bool:
        return any(
            re.search(
                pattern,
                value,
                re.IGNORECASE,
            )
            for pattern in patterns
        )


class LicenseAnalyzer:

    def __init__(
        self,
        policy: LicensePolicy | None = None,
    ) -> None:
        self.policy = policy or LicensePolicy()

    def analyze(
        self,
        project_path: Path | str,
    ) -> LicenseReport:
        path = Path(
            project_path
        ).expanduser().resolve()

        report = LicenseReport(
            project_name=path.name,
            project_path=path,
        )

        discovered: dict[
            tuple[str, str],
            LicenseRecord,
        ] = {}

        self._read_poetry_lock(
            path,
            report,
            discovered,
        )

        self._read_package_lock(
            path,
            report,
            discovered,
        )

        self._read_node_modules(
            path,
            report,
            discovered,
        )

        self._read_python_manifests(
            path,
            report,
            discovered,
        )

        report.records = sorted(
            discovered.values(),
            key=lambda record: (
                record.name.lower(),
                record.version,
                record.source,
            ),
        )

        return report

    def _read_poetry_lock(
        self,
        path: Path,
        report: LicenseReport,
        discovered: dict[
            tuple[str, str],
            LicenseRecord,
        ],
    ) -> None:
        file_path = path / "poetry.lock"

        if not file_path.is_file():
            return

        if tomllib is None:
            report.errors.append(
                "poetry.lock: TOML parser unavailable"
            )
            return

        try:
            with file_path.open("rb") as stream:
                data = tomllib.load(stream)
        except (
            OSError,
            ValueError,
        ) as error:
            report.errors.append(
                f"poetry.lock: {error}"
            )
            return

        packages = data.get(
            "package",
            [],
        )

        for package in packages:
            if not isinstance(package, dict):
                continue

            name = str(
                package.get(
                    "name",
                    "",
                )
            ).strip()

            if not name:
                continue

            self._add_record(
                discovered=discovered,
                name=name,
                version=str(
                    package.get(
                        "version",
                        "",
                    )
                ),
                license_name=str(
                    package.get(
                        "license",
                        "",
                    )
                ),
                source="poetry.lock",
            )

    def _read_package_lock(
        self,
        path: Path,
        report: LicenseReport,
        discovered: dict[
            tuple[str, str],
            LicenseRecord,
        ],
    ) -> None:
        for filename in (
            "package-lock.json",
            "npm-shrinkwrap.json",
        ):
            file_path = path / filename

            if not file_path.is_file():
                continue

            try:
                data = json.loads(
                    file_path.read_text(
                        encoding="utf-8"
                    )
                )
            except (
                OSError,
                json.JSONDecodeError,
            ) as error:
                report.errors.append(
                    f"{filename}: {error}"
                )
                continue

            packages = data.get(
                "packages",
                {},
            )

            if isinstance(packages, dict):
                for package_path, package in (
                    packages.items()
                ):
                    if not package_path:
                        continue

                    if not isinstance(
                        package,
                        dict,
                    ):
                        continue

                    name = package.get(
                        "name"
                    )

                    if not name:
                        name = self._node_name_from_path(
                            package_path
                        )

                    if not name:
                        continue

                    self._add_record(
                        discovered=discovered,
                        name=str(name),
                        version=str(
                            package.get(
                                "version",
                                "",
                            )
                        ),
                        license_name=self._license_value(
                            package.get(
                                "license"
                            )
                        ),
                        source=filename,
                    )

            dependencies = data.get(
                "dependencies",
                {},
            )

            if isinstance(
                dependencies,
                dict,
            ):
                self._walk_package_dependencies(
                    dependencies=dependencies,
                    source=filename,
                    discovered=discovered,
                )

    def _walk_package_dependencies(
        self,
        dependencies: dict[str, Any],
        source: str,
        discovered: dict[
            tuple[str, str],
            LicenseRecord,
        ],
    ) -> None:
        for name, package in dependencies.items():
            if not isinstance(package, dict):
                continue

            self._add_record(
                discovered=discovered,
                name=name,
                version=str(
                    package.get(
                        "version",
                        "",
                    )
                ),
                license_name=self._license_value(
                    package.get(
                        "license"
                    )
                ),
                source=source,
            )

            nested = package.get(
                "dependencies",
                {},
            )

            if isinstance(nested, dict):
                self._walk_package_dependencies(
                    dependencies=nested,
                    source=source,
                    discovered=discovered,
                )

    def _read_node_modules(
        self,
        path: Path,
        report: LicenseReport,
        discovered: dict[
            tuple[str, str],
            LicenseRecord,
        ],
    ) -> None:
        node_modules = path / "node_modules"

        if not node_modules.is_dir():
            return

        package_files = list(
            node_modules.glob(
                "*/package.json"
            )
        )

        package_files.extend(
            node_modules.glob(
                "@*/*/package.json"
            )
        )

        for file_path in package_files:
            try:
                data = json.loads(
                    file_path.read_text(
                        encoding="utf-8"
                    )
                )
            except (
                OSError,
                json.JSONDecodeError,
            ):
                continue

            name = str(
                data.get(
                    "name",
                    "",
                )
            ).strip()

            if not name:
                continue

            self._add_record(
                discovered=discovered,
                name=name,
                version=str(
                    data.get(
                        "version",
                        "",
                    )
                ),
                license_name=self._license_value(
                    data.get(
                        "license",
                        data.get(
                            "licenses",
                            "",
                        ),
                    )
                ),
                source="node_modules",
            )

    def _read_python_manifests(
        self,
        path: Path,
        report: LicenseReport,
        discovered: dict[
            tuple[str, str],
            LicenseRecord,
        ],
    ) -> None:
        dependency_names = self._python_dependency_names(
            path,
            report,
        )

        for dependency_name in dependency_names:
            key_matches = [
                key
                for key in discovered
                if key[0] == self._normalize_name(
                    dependency_name
                )
            ]

            if key_matches:
                continue

            try:
                distribution = metadata.distribution(
                    dependency_name
                )
            except metadata.PackageNotFoundError:
                self._add_record(
                    discovered=discovered,
                    name=dependency_name,
                    version="",
                    license_name="",
                    source="python-manifest",
                )
                continue

            metadata_license = (
                distribution.metadata.get(
                    "License",
                    "",
                )
            )

            if not metadata_license:
                metadata_license = (
                    self._license_from_classifiers(
                        distribution.metadata.get_all(
                            "Classifier",
                        )
                        or []
                    )
                )

            self._add_record(
                discovered=discovered,
                name=dependency_name,
                version=distribution.version,
                license_name=metadata_license,
                source="installed-metadata",
            )

    def _python_dependency_names(
        self,
        path: Path,
        report: LicenseReport,
    ) -> set[str]:
        names: set[str] = set()

        for file_path in path.glob(
            "requirements*.txt"
        ):
            try:
                lines = file_path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                ).splitlines()
            except OSError as error:
                report.errors.append(
                    f"{file_path.name}: {error}"
                )
                continue

            for raw_line in lines:
                line = raw_line.strip()

                if not line:
                    continue

                if line.startswith(
                    (
                        "#",
                        "-r",
                        "--requirement",
                        "-c",
                        "--constraint",
                        "-e",
                        "--editable",
                        "git+",
                        "http://",
                        "https://",
                    )
                ):
                    continue

                match = re.match(
                    r"^([A-Za-z0-9_.-]+)",
                    line,
                )

                if match:
                    names.add(
                        match.group(1)
                    )

        pyproject = path / "pyproject.toml"

        if (
            pyproject.is_file()
            and tomllib is not None
        ):
            try:
                with pyproject.open("rb") as stream:
                    data = tomllib.load(stream)
            except (
                OSError,
                ValueError,
            ) as error:
                report.errors.append(
                    f"pyproject.toml: {error}"
                )
                return names

            project = data.get(
                "project",
                {},
            )

            for item in project.get(
                "dependencies",
                [],
            ):
                match = re.match(
                    r"^([A-Za-z0-9_.-]+)",
                    str(item),
                )

                if match:
                    names.add(
                        match.group(1)
                    )

            poetry_dependencies = (
                data.get("tool", {})
                .get("poetry", {})
                .get("dependencies", {})
            )

            for name in poetry_dependencies:
                if name.lower() != "python":
                    names.add(name)

        return names

    def _add_record(
        self,
        discovered: dict[
            tuple[str, str],
            LicenseRecord,
        ],
        name: str,
        version: str,
        license_name: str,
        source: str,
    ) -> None:
        normalized_license = (
            license_name.strip()
            if license_name
            else "UNKNOWN"
        )

        category, allowed, reason = (
            self.policy.evaluate(
                normalized_license
            )
        )

        key = (
            self._normalize_name(name),
            version.strip(),
        )

        existing = discovered.get(key)

        candidate = LicenseRecord(
            name=name,
            version=version.strip(),
            license=normalized_license,
            category=category,
            source=source,
            allowed=allowed,
            reason=reason,
        )

        if existing is None:
            discovered[key] = candidate
            return

        if (
            existing.category == "unknown"
            and candidate.category != "unknown"
        ):
            discovered[key] = candidate

    @staticmethod
    def _normalize_name(
        name: str,
    ) -> str:
        return (
            name.strip()
            .lower()
            .replace("_", "-")
        )

    @staticmethod
    def _node_name_from_path(
        package_path: str,
    ) -> str:
        marker = "node_modules/"

        if marker not in package_path:
            return ""

        name = package_path.rsplit(
            marker,
            1,
        )[1]

        parts = name.split("/")

        if name.startswith("@"):
            return "/".join(
                parts[:2]
            )

        return parts[0]

    @staticmethod
    def _license_value(
        value: Any,
    ) -> str:
        if value is None:
            return ""

        if isinstance(value, str):
            return value

        if isinstance(value, dict):
            return str(
                value.get(
                    "type",
                    value.get(
                        "name",
                        "",
                    ),
                )
            )

        if isinstance(value, list):
            values = [
                LicenseAnalyzer._license_value(
                    item
                )
                for item in value
            ]

            return " OR ".join(
                item
                for item in values
                if item
            )

        return str(value)

    @staticmethod
    def _license_from_classifiers(
        classifiers: list[str],
    ) -> str:
        for classifier in classifiers:
            marker = "License ::"

            if marker not in classifier:
                continue

            return classifier.split(
                "::"
            )[-1].strip()

        return ""
