"""AIDK application kernel."""

from aidk.app.application import (
    Application,
    app,
)
from aidk.app.cache import TTLCache
from aidk.app.config import ApplicationConfig
from aidk.app.context import (
    ApplicationContext,
    build_context,
)
from aidk.app.events import (
    ApplicationEvent,
    EventBus,
)
from aidk.app.lifecycle import LifecycleManager
from aidk.app.plugins import (
    PluginManager,
    PluginRecord,
)
from aidk.app.providers import (
    CoreServiceProvider,
    ServiceProvider,
)
from aidk.app.registry import (
    RegisteredService,
    ServiceLifetime,
    ServiceRegistry,
)

__all__ = [
    "Application",
    "ApplicationConfig",
    "ApplicationContext",
    "ApplicationEvent",
    "CoreServiceProvider",
    "EventBus",
    "LifecycleManager",
    "PluginManager",
    "PluginRecord",
    "RegisteredService",
    "ServiceLifetime",
    "ServiceProvider",
    "ServiceRegistry",
    "TTLCache",
    "app",
    "build_context",
]
