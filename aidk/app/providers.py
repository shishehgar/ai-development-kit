"""Service provider contracts and built-in registrations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from aidk.app.cache import TTLCache
from aidk.app.config import ApplicationConfig
from aidk.app.events import EventBus
from aidk.app.lifecycle import LifecycleManager
from aidk.app.registry import ServiceRegistry
from aidk.application.audit_service import AuditService
from aidk.application.doctor_service import DoctorService
from aidk.application.git_report_service import (
    GitReportService,
)
from aidk.application.git_service import GitService
from aidk.application.workspace_service import (
    WorkspaceService,
)
from aidk.application.container import (
    ApplicationServices,
)


@runtime_checkable
class ServiceProvider(Protocol):
    """Contract implemented by dependency providers."""

    @property
    def name(self) -> str:
        ...

    def register(
        self,
        registry: ServiceRegistry,
    ) -> None:
        ...


@dataclass(slots=True)
class CoreServiceProvider:
    """Register application kernel dependencies."""

    config: ApplicationConfig
    services: ApplicationServices
    events: EventBus
    cache: TTLCache
    lifecycle: LifecycleManager

    @property
    def name(self) -> str:
        return "aidk.core"

    def register(
        self,
        registry: ServiceRegistry,
    ) -> None:
        registry.register_instance(
            ApplicationConfig,
            self.config,
        )

        registry.register_instance(
            EventBus,
            self.events,
        )

        registry.register_instance(
            TTLCache,
            self.cache,
        )

        registry.register_instance(
            LifecycleManager,
            self.lifecycle,
        )

        registry.register_instance(
            ApplicationServices,
            self.services,
        )

        registry.register_instance(
            DoctorService,
            self.services.doctor,
        )

        registry.register_instance(
            WorkspaceService,
            self.services.workspace,
        )

        registry.register_instance(
            AuditService,
            self.services.audit,
        )

        registry.register_instance(
            GitService,
            self.services.git,
        )

        registry.register_instance(
            GitReportService,
            self.services.git_report,
        )
