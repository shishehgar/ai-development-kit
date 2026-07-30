"""Top-level AIDK application object."""

from __future__ import annotations

import logging
from threading import RLock
from typing import TypeVar

from aidk.app.cache import TTLCache
from aidk.app.config import ApplicationConfig
from aidk.app.context import (
    ApplicationContext,
    build_context,
)
from aidk.app.events import EventBus
from aidk.app.lifecycle import LifecycleManager
from aidk.app.plugins import PluginManager
from aidk.app.registry import ServiceRegistry
from aidk.application.container import (
    ApplicationServices,
)


T = TypeVar("T")


class Application:
    """Main entry point for shared AIDK runtime state."""

    def __init__(
        self,
        context: ApplicationContext | None = None,
    ) -> None:
        self._context = (
            context
            or build_context()
        )

        self._lock = RLock()

    @property
    def context(self) -> ApplicationContext:
        return self._context

    @property
    def config(self) -> ApplicationConfig:
        return self._context.config

    @property
    def services(self) -> ApplicationServices:
        """Compatibility facade for existing adapters."""

        return self._context.services

    @property
    def logger(self) -> logging.Logger:
        return self._context.logger

    @property
    def events(self) -> EventBus:
        return self._context.events

    @property
    def cache(self) -> TTLCache:
        return self._context.cache

    @property
    def lifecycle(self) -> LifecycleManager:
        return self._context.lifecycle

    @property
    def registry(self) -> ServiceRegistry:
        return self._context.registry

    @property
    def plugins(self) -> PluginManager:
        return self._context.plugins

    @property
    def started(self) -> bool:
        return self.lifecycle.started

    def resolve(
        self,
        service_type: type[T],
        *,
        name: str | None = None,
    ) -> T:
        """Resolve a dependency from the application registry."""

        return self.registry.resolve(
            service_type,
            name=name,
        )

    def try_resolve(
        self,
        service_type: type[T],
        *,
        name: str | None = None,
        default: T | None = None,
    ) -> T | None:
        return self.registry.try_resolve(
            service_type,
            name=name,
            default=default,
        )

    def start(self) -> bool:
        return self.lifecycle.start()

    def stop(self) -> bool:
        return self.lifecycle.stop()

    def reload(
        self,
        config: ApplicationConfig | None = None,
    ) -> ApplicationContext:
        with self._lock:
            was_started = self.started

            if was_started:
                self.stop()

            self._context = build_context(
                config=config
            )

            if was_started:
                self.start()

            return self._context


app = Application()
