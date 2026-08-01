"""Application service container for AIDK."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from aidk.ai.engine import AssistantEngine
from aidk.ai.runtime import AIRuntime
from aidk.application.assistant_service import AssistantService
from aidk.application.audit_service import AuditService
from aidk.application.doctor_service import DoctorService
from aidk.application.git_report_service import GitReportService
from aidk.application.git_service import GitService
from aidk.application.workspace_service import WorkspaceService


@dataclass(frozen=True)
class ApplicationServices:
    """Services shared by AIDK interfaces."""

    doctor: DoctorService
    workspace: WorkspaceService
    audit: AuditService
    git: GitService
    git_report: GitReportService
    assistant: AssistantService | None = None


def build_services(
    *,
    workspace: Path | None = None,
    projects_root: Path | None = None,
    git_path: Path | None = None,
    assistant_engine: AssistantEngine | None = None,
    ai_runtime: AIRuntime | None = None,
) -> ApplicationServices:
    if (
        assistant_engine is not None
        and ai_runtime is not None
    ):
        raise ValueError(
            "Provide either assistant_engine or ai_runtime, "
            "not both."
        )

    resolved_assistant_engine = (
        ai_runtime.engine
        if ai_runtime is not None
        else assistant_engine
    )

    """Build the application service container."""

    workspace_service = WorkspaceService(
        root=projects_root,
    )

    return ApplicationServices(
        doctor=DoctorService(
            workspace=workspace,
        ),
        workspace=workspace_service,
        audit=AuditService(
            workspace_service=workspace_service,
        ),
        git=GitService(
            path=git_path,
        ),
        git_report=GitReportService(
            workspace_service=workspace_service,
        ),
        assistant=(
            AssistantService(
                engine=resolved_assistant_engine,
            )
            if resolved_assistant_engine is not None
            else None
        ),
    )


services = build_services()
