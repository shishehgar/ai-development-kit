"""Application context construction."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from aidk.app.cache import TTLCache
from aidk.app.config import ApplicationConfig
from aidk.app.events import EventBus
from aidk.app.lifecycle import LifecycleManager
from aidk.app.logger import build_logger
from aidk.app.plugins import PluginManager
from aidk.app.providers import CoreServiceProvider
from aidk.app.registry import ServiceRegistry
from aidk.application.container import (
    ApplicationServices,
    build_services,
)


@dataclass(slots=True)
class ApplicationContext:
    """Shared runtime dependencies for AIDK."""

    config: ApplicationConfig
    services: ApplicationServices
    logger: logging.Logger
    events: EventBus
    cache: TTLCache
    lifecycle: LifecycleManager
    registry: ServiceRegistry
    plugins: PluginManager


def build_context(
    config: ApplicationConfig | None = None,
) -> ApplicationContext:
    """Build a complete AIDK application context."""

    resolved_config = (
        config
        or ApplicationConfig.from_environment()
    )

    logger = build_logger(
        debug=resolved_config.debug,
    )

    events = EventBus()

    cache = TTLCache(
        default_ttl=(
            resolved_config.cache_ttl_seconds
        ),
    )

    lifecycle = LifecycleManager()

    services = build_services(
        workspace=resolved_config.workspace,
        projects_root=(
            resolved_config.projects_root
        ),
        git_path=resolved_config.workspace,
    )

    registry = ServiceRegistry()

    provider = CoreServiceProvider(
        config=resolved_config,
        services=services,
        events=events,
        cache=cache,
        lifecycle=lifecycle,
    )

    provider.register(
        registry
    )

    plugins = PluginManager(
        registry=registry,
        logger=logger,
    )

    registry.register_instance(
        ServiceRegistry,
        registry,
    )

    registry.register_instance(
        PluginManager,
        plugins,
    )

    context = ApplicationContext(
        config=resolved_config,
        services=services,
        logger=logger,
        events=events,
        cache=cache,
        lifecycle=lifecycle,
        registry=registry,
        plugins=plugins,
    )

    lifecycle.on_startup(
        lambda: logger.debug(
            "AIDK application context started."
        )
    )

    lifecycle.on_startup(
        lambda: events.publish(
            "application.started",
            environment=(
                resolved_config.environment
            ),
            workspace=str(
                resolved_config.workspace
            ),
        )
    )

    lifecycle.on_shutdown(
        plugins.stop_all
    )

    lifecycle.on_shutdown(
        lambda: events.publish(
            "application.stopping"
        )
    )

    lifecycle.on_shutdown(
        cache.clear
    )

    lifecycle.on_shutdown(
        lambda: logger.debug(
            "AIDK application context stopped."
        )
    )

    return context
