"""Structured health-check service for AIDK."""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Final


DEFAULT_WORKSPACE: Final[Path] = Path("/home/ubuntu/my_services")

DEFAULT_TOOLS: Final[tuple[tuple[str, str], ...]] = (
    ("Git", "git"),
    ("Python", "python3"),
    ("Docker", "docker"),
    ("Node", "node"),
    ("npm", "npm"),
    ("GitHub CLI", "gh"),
    ("AWS CLI", "aws"),
    ("Ollama", "ollama"),
)


@dataclass(frozen=True)
class DoctorCheck:
    """Result of one environment health check."""

    key: str
    title: str
    status: str
    installed: bool
    required: bool
    executable: str | None = None
    path: str | None = None
    version: str | None = None
    message: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class DoctorReport:
    """Complete AIDK environment health report."""

    status: str
    health_score: int
    passed: int
    failed: int
    warnings: int
    python_version: str
    platform: str
    workspace: str
    checks: tuple[DoctorCheck, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            **asdict(self),
            "checks": [
                check.to_dict()
                for check in self.checks
            ],
        }


class DoctorService:
    """Inspect the local AIDK runtime without printing output."""

    def __init__(
        self,
        workspace: Path | None = None,
    ) -> None:
        configured_workspace = os.getenv(
            "AIDK_WORKSPACE_ROOT",
        )

        if workspace is not None:
            selected_workspace = workspace
        elif configured_workspace:
            selected_workspace = Path(configured_workspace)
        else:
            selected_workspace = DEFAULT_WORKSPACE

        self.workspace = selected_workspace.expanduser().resolve()

    @staticmethod
    def _get_version(
        executable: str,
    ) -> str | None:
        try:
            result = subprocess.run(
                [executable, "--version"],
                capture_output=True,
                check=False,
                text=True,
                timeout=3,
            )
        except (
            OSError,
            subprocess.SubprocessError,
        ):
            return None

        text = result.stdout.strip() or result.stderr.strip()

        if not text:
            return None

        return text.splitlines()[0].strip()

    def _check_tool(
        self,
        title: str,
        executable: str,
        *,
        required: bool,
    ) -> DoctorCheck:
        executable_path = shutil.which(executable)

        if executable_path is None:
            return DoctorCheck(
                key=f"tool:{executable}",
                title=title,
                status="failed" if required else "warning",
                installed=False,
                required=required,
                executable=executable,
                message=(
                    "Required executable was not found."
                    if required
                    else "Optional executable was not found."
                ),
            )

        return DoctorCheck(
            key=f"tool:{executable}",
            title=title,
            status="passed",
            installed=True,
            required=required,
            executable=executable,
            path=executable_path,
            version=self._get_version(executable),
            message="Executable is available.",
        )

    def _check_workspace(self) -> DoctorCheck:
        exists = self.workspace.is_dir()

        return DoctorCheck(
            key="workspace",
            title="Workspace",
            status="passed" if exists else "failed",
            installed=exists,
            required=True,
            path=str(self.workspace),
            message=(
                "Workspace directory is available."
                if exists
                else "Workspace directory does not exist."
            ),
        )

    def run(self) -> DoctorReport:
        checks: list[DoctorCheck] = []

        for title, executable in DEFAULT_TOOLS:
            required = executable in {
                "git",
                "python3",
            }

            checks.append(
                self._check_tool(
                    title,
                    executable,
                    required=required,
                )
            )

        checks.append(self._check_workspace())

        passed = sum(
            check.status == "passed"
            for check in checks
        )
        failed = sum(
            check.status == "failed"
            for check in checks
        )
        warnings = sum(
            check.status == "warning"
            for check in checks
        )

        required_checks = [
            check
            for check in checks
            if check.required
        ]

        required_passed = sum(
            check.status == "passed"
            for check in required_checks
        )

        health_score = (
            int(
                required_passed
                / len(required_checks)
                * 100
            )
            if required_checks
            else 100
        )

        if failed:
            overall_status = "unhealthy"
        elif warnings:
            overall_status = "degraded"
        else:
            overall_status = "healthy"

        return DoctorReport(
            status=overall_status,
            health_score=health_score,
            passed=passed,
            failed=failed,
            warnings=warnings,
            python_version=platform.python_version(),
            platform=platform.platform(),
            workspace=str(self.workspace),
            checks=tuple(checks),
        )
