"""Structured engineering audit service for AIDK."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from aidk.audit.engine import AuditEngine
from aidk.application.workspace_service import WorkspaceService
from aidk.workspace.analyzer import WorkspaceAnalyzer
from aidk.workspace.scanner import WorkspaceScanner


@dataclass(frozen=True)
class AuditReport:
    """Serializable engineering audit report."""

    root: str
    total_projects: int
    average_score: float
    grade_distribution: dict[str, int]
    missing_readme: int
    missing_tests: int
    missing_ai_config: int
    missing_license: int
    missing_docker: int
    critical_projects: tuple[str, ...]
    recommendations: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)

        payload["critical_projects"] = list(
            self.critical_projects
        )
        payload["recommendations"] = list(
            self.recommendations
        )

        return payload


class AuditService:
    """Generate audit reports without printing output."""

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

    def run(self) -> AuditReport:
        projects = WorkspaceScanner(
            root=self.workspace_service.root,
        ).scan()

        projects = WorkspaceAnalyzer().analyze(
            projects
        )

        audit = AuditEngine().generate(
            projects
        )

        return AuditReport(
            root=str(
                self.workspace_service.root
            ),
            total_projects=audit.total_projects,
            average_score=audit.average_score,
            grade_distribution=dict(
                audit.grade_distribution
            ),
            missing_readme=audit.missing_readme,
            missing_tests=audit.missing_tests,
            missing_ai_config=audit.missing_ai_config,
            missing_license=audit.missing_license,
            missing_docker=audit.missing_docker,
            critical_projects=tuple(
                audit.critical_projects
            ),
            recommendations=tuple(
                audit.recommendations
            ),
        )
