"""Tests for application dependency resolution."""

from __future__ import annotations

from pathlib import Path

from aidk.app.application import Application
from aidk.app.config import ApplicationConfig
from aidk.app.context import build_context
from aidk.app.plugins import PluginManager
from aidk.app.registry import ServiceRegistry
from aidk.application.audit_service import (
    AuditService,
)
from aidk.application.git_service import (
    GitService,
)
from aidk.application.workspace_service import (
    WorkspaceService,
)


def build_config(
    root: Path,
) -> ApplicationConfig:
    return ApplicationConfig(
        workspace=root.resolve(),
        projects_root=root.resolve(),
        api_host="127.0.0.1",
        api_port=8000,
        debug=True,
        environment="test",
        cache_ttl_seconds=30,
    )


def test_application_resolves_services(
    tmp_path: Path,
) -> None:
    application = Application(
        build_context(
            build_config(
                tmp_path
            )
        )
    )

    assert (
        application.resolve(
            WorkspaceService
        )
        is application.services.workspace
    )

    assert (
        application.resolve(
            AuditService
        )
        is application.services.audit
    )

    assert (
        application.resolve(
            GitService
        )
        is application.services.git
    )


def test_kernel_dependencies_are_registered(
    tmp_path: Path,
) -> None:
    application = Application(
        build_context(
            build_config(
                tmp_path
            )
        )
    )

    assert (
        application.resolve(
            ServiceRegistry
        )
        is application.registry
    )

    assert (
        application.resolve(
            PluginManager
        )
        is application.plugins
    )


def test_registry_lists_services(
    tmp_path: Path,
) -> None:
    application = Application(
        build_context(
            build_config(
                tmp_path
            )
        )
    )

    service_names = {
        item.service
        for item
        in application.registry.describe()
    }

    assert any(
        name.endswith(
            ".WorkspaceService"
        )
        for name in service_names
    )

    assert any(
        name.endswith(
            ".AuditService"
        )
        for name in service_names
    )
