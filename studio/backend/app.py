"""AIDK Studio FastAPI application."""

from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(
    PROJECT_ROOT / ".env"
)


from studio.backend.api.routes import (
    reindex,
    ai_status,
    assistant,
    graph,
    impact,
    knowledge,
    project_index,
)
from studio.backend.api.routes.audit import (
    router as audit_router,
)
from studio.backend.api.routes.commands import (
    router as commands_router,
)
from studio.backend.api.routes.doctor import (
    router as doctor_router,
)
from studio.backend.api.routes.git import (
    router as git_router,
)
from studio.backend.api.routes.git_report import (
    router as git_report_router,
)
from studio.backend.api.routes.plugins import (
    router as plugins_router,
)
from studio.backend.api.routes.projects import (
    router as projects_router,
)
from studio.backend.api.routes.registry import (
    router as registry_router,
)
from studio.backend.api.routes.system import (
    router as system_router,
)
from studio.backend.api.routes.workspace import (
    router as workspace_router,
)
from studio.backend.core.config import settings


def create_app() -> FastAPI:
    """Create and configure the AIDK Studio application."""

    application = FastAPI(
        title=settings.app_name,
        version=settings.version,
        description=(
            "Visual engineering workspace for AIDK."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url=(
            f"{settings.api_prefix}/openapi.json"
        ),
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    prefixed_routers = (
        system_router,
        commands_router,
        doctor_router,
        workspace_router,
        audit_router,
        git_router,
        git_report_router,
        projects_router,
        registry_router,
        plugins_router,
        project_index.router,
        reindex.router,
        knowledge.router,
        graph.router,
        impact.router,
        ai_status.router,
        assistant.router,
    )

    for router in prefixed_routers:
        application.include_router(
            router,
            prefix=settings.api_prefix,
        )

    # Backward-compatible Knowledge API routes.
    #
    # Current API:
    #     /api/v1/knowledge/*
    #
    # Legacy Studio API:
    #     /knowledge/*
    application.include_router(
        knowledge.router,
    )

    @application.get(
        "/",
        tags=["root"],
    )
    def root() -> dict[str, str]:
        """Return the application readiness response."""

        return {
            "name": settings.app_name,
            "status": "ready",
            "documentation": "/docs",
        }

    return application


app = create_app()
