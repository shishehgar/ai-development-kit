"""Structured workspace analysis service for AIDK."""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from aidk.workspace.analyzer import WorkspaceAnalyzer
from aidk.workspace.project import Project
from aidk.workspace.scanner import WorkspaceScanner


DEFAULT_PROJECTS_ROOT = Path(
    "/home/ubuntu/my_services/projects"
)


@dataclass(frozen=True)
class WorkspaceProjectSummary:
    """Serializable summary of one analyzed project."""

    name: str
    path: str
    language: str
    git: bool
    docker: bool
    continue_config: bool
    readme: bool
    license: bool
    tests: bool
    score: int
    intelligence_score: int
    grade: str
    documentation_score: int
    strengths: tuple[str, ...]
    weaknesses: tuple[str, ...]
    recommendations: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class WorkspaceReport:
    """Structured result of a workspace analysis."""

    root: str
    project_count: int
    projects: tuple[WorkspaceProjectSummary, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "root": self.root,
            "project_count": self.project_count,
            "projects": [
                project.to_dict()
                for project in self.projects
            ],
        }


class WorkspaceService:
    """Scan and analyze projects without printing output."""

    def __init__(
        self,
        root: Path | str | None = None,
    ) -> None:
        configured_root = os.getenv(
            "AIDK_STUDIO_WORKSPACE",
        )

        selected_root: Path | str

        if root is not None:
            selected_root = root
        elif configured_root:
            selected_root = configured_root
        else:
            selected_root = DEFAULT_PROJECTS_ROOT

        self.root = Path(
            selected_root
        ).expanduser().resolve()

    @staticmethod
    def _summarize(
        project: Project,
    ) -> WorkspaceProjectSummary:
        return WorkspaceProjectSummary(
            name=project.name,
            path=str(project.path),
            language=project.language,
            git=project.git,
            docker=project.docker,
            continue_config=project.continue_config,
            readme=project.readme,
            license=project.license,
            tests=project.tests,
            score=project.score,
            intelligence_score=project.intelligence_score,
            grade=project.grade,
            documentation_score=project.documentation_score,
            strengths=tuple(project.strengths),
            weaknesses=tuple(project.weaknesses),
            recommendations=tuple(
                project.recommendations
            ),
        )

    def run(self) -> WorkspaceReport:
        scanner = WorkspaceScanner(
            root=self.root,
        )

        analyzer = WorkspaceAnalyzer()

        projects = scanner.scan()
        analyzed_projects = analyzer.analyze(
            projects
        )

        summaries = tuple(
            self._summarize(project)
            for project in analyzed_projects
        )

        return WorkspaceReport(
            root=str(self.root),
            project_count=len(summaries),
            projects=summaries,
        )
