"""Structured workspace Git report service for AIDK."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from aidk.application.workspace_service import WorkspaceService
from aidk.git.report.engine import GitReportEngine
from aidk.workspace.scanner import WorkspaceScanner


@dataclass(frozen=True)
class GitRisk:
    """Serializable Git risk for one project."""

    project: str
    level: str
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["reasons"] = list(self.reasons)
        return payload


@dataclass(frozen=True)
class GitWorkspaceReport:
    """Serializable Git report for all workspace projects."""

    root: str
    total_projects: int
    clean_repositories: int
    dirty_repositories: int
    branches: dict[str, int]
    remote_count: int
    no_remote_count: int
    risks: tuple[GitRisk, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "root": self.root,
            "total_projects": self.total_projects,
            "clean_repositories": self.clean_repositories,
            "dirty_repositories": self.dirty_repositories,
            "branches": dict(self.branches),
            "remote_count": self.remote_count,
            "no_remote_count": self.no_remote_count,
            "risks": [
                risk.to_dict()
                for risk in self.risks
            ],
        }


class GitReportService:
    """Generate workspace-wide Git reports without printing."""

    def __init__(
        self,
        *,
        workspace_service: WorkspaceService | None = None,
        projects_root: Path | str | None = None,
    ) -> None:
        if workspace_service is not None:
            self.workspace_service = workspace_service
        else:
            self.workspace_service = WorkspaceService(
                root=projects_root,
            )

    def run(self) -> GitWorkspaceReport:
        projects = WorkspaceScanner(
            root=self.workspace_service.root,
        ).scan()

        report = GitReportEngine().generate(
            projects
        )

        risks = tuple(
            GitRisk(
                project=item.project,
                level=item.level,
                reasons=tuple(item.reasons),
            )
            for item in report.risks
        )

        return GitWorkspaceReport(
            root=str(
                self.workspace_service.root
            ),
            total_projects=report.total_projects,
            clean_repositories=(
                report.clean_repositories
            ),
            dirty_repositories=(
                report.dirty_repositories
            ),
            branches=dict(report.branches),
            remote_count=report.remote_count,
            no_remote_count=report.no_remote_count,
            risks=risks,
        )
