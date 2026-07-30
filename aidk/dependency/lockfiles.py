"""
Dependency lockfile analysis.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
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
class LockfileIssue:
    issue_type: str
    message: str
    severity: str
    file: str = ""


@dataclass
class LockfileReport:
    project_name: str
    project_path: Path
    manifests: list[str] = field(default_factory=list)
    lockfiles: list[str] = field(default_factory=list)
    package_managers: list[str] = field(default_factory=list)
    issues: list[LockfileIssue] = field(default_factory=list)

    @property
    def score(self) -> int:
        penalties = {
            "critical": 30,
            "high": 15,
            "medium": 7,
            "low": 2,
        }

        value = 100

        for issue in self.issues:
            value -= penalties.get(
                issue.severity,
                0,
            )

        return max(0, value)

    @property
    def healthy(self) -> bool:
        return not any(
            issue.severity in {
                "critical",
                "high",
            }
            for issue in self.issues
        )


class LockfileAnalyzer:

    PYTHON_MANIFESTS = (
        "pyproject.toml",
        "requirements.txt",
        "requirements-dev.txt",
        "requirements-test.txt",
        "Pipfile",
        "environment.yml",
        "environment.yaml",
    )

    PYTHON_LOCKFILES = (
        "poetry.lock",
        "uv.lock",
        "Pipfile.lock",
        "requirements.lock",
        "requirements.txt",
        "conda-lock.yml",
        "conda-lock.yaml",
    )

    NODE_MANIFESTS = (
        "package.json",
    )

    NODE_LOCKFILES = (
        "package-lock.json",
        "npm-shrinkwrap.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        "bun.lock",
        "bun.lockb",
    )

    def analyze(
        self,
        project_path: Path | str,
    ) -> LockfileReport:
        path = Path(
            project_path
        ).expanduser().resolve()

        report = LockfileReport(
            project_name=path.name,
            project_path=path,
        )

        self._inspect_python(
            path,
            report,
        )

        self._inspect_node(
            path,
            report,
        )

        self._inspect_multiple_lockfiles(
            report
        )

        self._inspect_gitignore(
            path,
            report,
        )

        report.manifests = sorted(
            set(report.manifests)
        )

        report.lockfiles = sorted(
            set(report.lockfiles)
        )

        report.package_managers = sorted(
            set(report.package_managers)
        )

        report.issues.sort(
            key=lambda issue: (
                self._severity_rank(
                    issue.severity
                ),
                issue.issue_type,
                issue.file,
            )
        )

        return report

    def _inspect_python(
        self,
        path: Path,
        report: LockfileReport,
    ) -> None:
        manifests = [
            name
            for name in self.PYTHON_MANIFESTS
            if (path / name).is_file()
        ]

        lockfiles = [
            name
            for name in self.PYTHON_LOCKFILES
            if (path / name).is_file()
        ]

        if not manifests:
            return

        report.manifests.extend(manifests)
        report.lockfiles.extend(lockfiles)

        pyproject_path = path / "pyproject.toml"

        manager = self._detect_python_manager(
            pyproject_path
        )

        if manager:
            report.package_managers.append(
                manager
            )

        if "Pipfile" in manifests:
            report.package_managers.append(
                "pipenv"
            )

        if any(
            name.startswith("requirements")
            for name in manifests
        ):
            report.package_managers.append(
                "pip"
            )

        if any(
            name.startswith("environment.")
            for name in manifests
        ):
            report.package_managers.append(
                "conda"
            )

        expected_lockfile = {
            "poetry": "poetry.lock",
            "uv": "uv.lock",
            "pipenv": "Pipfile.lock",
        }.get(manager)

        if (
            manager == "pipenv"
            or "Pipfile" in manifests
        ):
            expected_lockfile = "Pipfile.lock"

        if expected_lockfile:
            if expected_lockfile not in lockfiles:
                report.issues.append(
                    LockfileIssue(
                        issue_type="missing-lockfile",
                        message=(
                            f"{manager or 'pipenv'} "
                            "manifest exists but its "
                            "lockfile is missing."
                        ),
                        severity="high",
                        file=expected_lockfile,
                    )
                )

        elif (
            "pyproject.toml" in manifests
            and not lockfiles
        ):
            report.issues.append(
                LockfileIssue(
                    issue_type="missing-lockfile",
                    message=(
                        "Python dependency manifest "
                        "exists without a detected "
                        "lockfile."
                    ),
                    severity="high",
                    file="pyproject.toml",
                )
            )

        self._inspect_requirements_pinning(
            path,
            manifests,
            report,
        )

        self._inspect_pipfile_lock(
            path,
            report,
        )

    def _inspect_node(
        self,
        path: Path,
        report: LockfileReport,
    ) -> None:
        package_json = path / "package.json"

        if not package_json.is_file():
            return

        report.manifests.append(
            "package.json"
        )

        lockfiles = [
            name
            for name in self.NODE_LOCKFILES
            if (path / name).is_file()
        ]

        report.lockfiles.extend(
            lockfiles
        )

        package_manager = (
            self._read_node_package_manager(
                package_json
            )
        )

        if package_manager:
            report.package_managers.append(
                package_manager
            )

        detected_managers = {
            self._node_manager_for_lockfile(name)
            for name in lockfiles
        }

        detected_managers.discard(None)

        report.package_managers.extend(
            sorted(detected_managers)
        )

        if not lockfiles:
            report.issues.append(
                LockfileIssue(
                    issue_type="missing-lockfile",
                    message=(
                        "package.json exists without "
                        "a Node.js lockfile."
                    ),
                    severity="high",
                    file="package.json",
                )
            )

        if (
            package_manager
            and detected_managers
            and package_manager
            not in detected_managers
        ):
            report.issues.append(
                LockfileIssue(
                    issue_type=(
                        "package-manager-mismatch"
                    ),
                    message=(
                        "package.json packageManager "
                        "does not match the detected "
                        "lockfile."
                    ),
                    severity="high",
                    file="package.json",
                )
            )

        self._inspect_package_lock(
            path,
            report,
        )

    def _inspect_requirements_pinning(
        self,
        path: Path,
        manifests: list[str],
        report: LockfileReport,
    ) -> None:
        requirement_files = [
            name
            for name in manifests
            if name.startswith(
                "requirements"
            )
            and name.endswith(".txt")
        ]

        for filename in requirement_files:
            file_path = path / filename

            try:
                lines = file_path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                ).splitlines()
            except OSError as error:
                report.issues.append(
                    LockfileIssue(
                        issue_type="read-error",
                        message=str(error),
                        severity="high",
                        file=filename,
                    )
                )
                continue

            unpinned = 0

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
                    )
                ):
                    continue

                if "==" not in line:
                    unpinned += 1

            if unpinned:
                report.issues.append(
                    LockfileIssue(
                        issue_type=(
                            "requirements-not-locked"
                        ),
                        message=(
                            f"{unpinned} requirement"
                            f"{'s are' if unpinned != 1 else ' is'} "
                            "not pinned with ==."
                        ),
                        severity="medium",
                        file=filename,
                    )
                )

    def _inspect_pipfile_lock(
        self,
        path: Path,
        report: LockfileReport,
    ) -> None:
        file_path = path / "Pipfile.lock"

        if not file_path.is_file():
            return

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
            report.issues.append(
                LockfileIssue(
                    issue_type="invalid-lockfile",
                    message=str(error),
                    severity="critical",
                    file="Pipfile.lock",
                )
            )
            return

        if "_meta" not in data:
            report.issues.append(
                LockfileIssue(
                    issue_type="invalid-lockfile",
                    message=(
                        "Pipfile.lock does not contain "
                        "the _meta section."
                    ),
                    severity="high",
                    file="Pipfile.lock",
                )
            )

    def _inspect_package_lock(
        self,
        path: Path,
        report: LockfileReport,
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
                report.issues.append(
                    LockfileIssue(
                        issue_type="invalid-lockfile",
                        message=str(error),
                        severity="critical",
                        file=filename,
                    )
                )
                continue

            lockfile_version = data.get(
                "lockfileVersion"
            )

            if lockfile_version is None:
                report.issues.append(
                    LockfileIssue(
                        issue_type="invalid-lockfile",
                        message=(
                            "Node lockfile does not "
                            "contain lockfileVersion."
                        ),
                        severity="high",
                        file=filename,
                    )
                )

    def _inspect_multiple_lockfiles(
        self,
        report: LockfileReport,
    ) -> None:
        node_lockfiles = [
            name
            for name in report.lockfiles
            if name in self.NODE_LOCKFILES
        ]

        if len(node_lockfiles) > 1:
            report.issues.append(
                LockfileIssue(
                    issue_type=(
                        "multiple-node-lockfiles"
                    ),
                    message=(
                        "Multiple Node.js lockfiles "
                        "were detected."
                    ),
                    severity="high",
                    file=", ".join(
                        sorted(node_lockfiles)
                    ),
                )
            )

        python_tool_lockfiles = [
            name
            for name in report.lockfiles
            if name in {
                "poetry.lock",
                "uv.lock",
                "Pipfile.lock",
                "conda-lock.yml",
                "conda-lock.yaml",
            }
        ]

        if len(python_tool_lockfiles) > 1:
            report.issues.append(
                LockfileIssue(
                    issue_type=(
                        "multiple-python-lockfiles"
                    ),
                    message=(
                        "Multiple Python package "
                        "manager lockfiles were "
                        "detected."
                    ),
                    severity="medium",
                    file=", ".join(
                        sorted(
                            python_tool_lockfiles
                        )
                    ),
                )
            )

    def _inspect_gitignore(
        self,
        path: Path,
        report: LockfileReport,
    ) -> None:
        gitignore = path / ".gitignore"

        if not gitignore.is_file():
            return

        try:
            entries = {
                line.strip().lstrip("/")
                for line in gitignore.read_text(
                    encoding="utf-8",
                    errors="ignore",
                ).splitlines()
                if line.strip()
                and not line.lstrip().startswith("#")
            }
        except OSError:
            return

        for lockfile in report.lockfiles:
            if (
                lockfile in entries
                or f"**/{lockfile}" in entries
                or f"*{lockfile}" in entries
            ):
                report.issues.append(
                    LockfileIssue(
                        issue_type=(
                            "ignored-lockfile"
                        ),
                        message=(
                            "Lockfile is excluded by "
                            ".gitignore."
                        ),
                        severity="high",
                        file=lockfile,
                    )
                )

    def _detect_python_manager(
        self,
        pyproject_path: Path,
    ) -> str | None:
        if not pyproject_path.is_file():
            return None

        if tomllib is None:
            return None

        try:
            with pyproject_path.open("rb") as stream:
                data = tomllib.load(stream)
        except (
            OSError,
            ValueError,
        ):
            return None

        tool = data.get(
            "tool",
            {},
        )

        if "poetry" in tool:
            return "poetry"

        if "uv" in tool:
            return "uv"

        build_system = data.get(
            "build-system",
            {},
        )

        backend = str(
            build_system.get(
                "build-backend",
                "",
            )
        ).lower()

        if "poetry" in backend:
            return "poetry"

        if "hatch" in backend:
            return "hatch"

        if "pdm" in backend:
            return "pdm"

        return None

    @staticmethod
    def _read_node_package_manager(
        package_json: Path,
    ) -> str | None:
        try:
            data: dict[str, Any] = json.loads(
                package_json.read_text(
                    encoding="utf-8"
                )
            )
        except (
            OSError,
            json.JSONDecodeError,
        ):
            return None

        value = str(
            data.get(
                "packageManager",
                "",
            )
        ).strip()

        if not value:
            return None

        return value.split(
            "@",
            1,
        )[0].lower()

    @staticmethod
    def _node_manager_for_lockfile(
        filename: str,
    ) -> str | None:
        mapping = {
            "package-lock.json": "npm",
            "npm-shrinkwrap.json": "npm",
            "yarn.lock": "yarn",
            "pnpm-lock.yaml": "pnpm",
            "bun.lock": "bun",
            "bun.lockb": "bun",
        }

        return mapping.get(filename)

    @staticmethod
    def _severity_rank(
        severity: str,
    ) -> int:
        return {
            "critical": 0,
            "high": 1,
            "medium": 2,
            "low": 3,
        }.get(
            severity,
            4,
        )
