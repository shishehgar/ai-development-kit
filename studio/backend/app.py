"""AIDK Studio FastAPI application."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from studio.backend.api.routes.commands import router as commands_router
from studio.backend.api.routes.doctor import router as doctor_router
from studio.backend.api.routes.workspace import router as workspace_router
from studio.backend.api.routes.audit import router as audit_router
from studio.backend.api.routes.git import router as git_router
from studio.backend.api.routes.git_report import router as git_report_router
from studio.backend.api.routes.projects import router as projects_router
from studio.backend.api.routes.system import router as system_router
from studio.backend.api.routes.registry import router as registry_router
from studio.backend.api.routes.plugins import router as plugins_router
from studio.backend.core.config import settings

from studio.backend.api.routes import impact
from studio.backend.api.routes import graph
from studio.backend.api.routes import knowledge

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        description="Visual engineering workspace for AIDK.",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url=f"{settings.api_prefix}/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(system_router, prefix=settings.api_prefix)
    app.include_router(commands_router, prefix=settings.api_prefix)
    app.include_router(doctor_router, prefix=settings.api_prefix)
    app.include_router(workspace_router, prefix=settings.api_prefix)
    app.include_router(audit_router, prefix=settings.api_prefix)
    app.include_router(git_router, prefix=settings.api_prefix)
    app.include_router(git_report_router, prefix=settings.api_prefix)
    app.include_router(projects_router, prefix=settings.api_prefix)
    app.include_router(impact.router)
    app.include_router(knowledge.router)

    @app.get("/", tags=["root"])
    def root() -> dict[str, str]:
        return {
            "name": settings.app_name,
            "status": "ready",
            "documentation": "/docs",
        }

    app.include_router(registry_router, prefix=settings.api_prefix)
    app.include_router(plugins_router, prefix=settings.api_prefix)
    app.include_router(graph.router)
    return app


app = create_app()
