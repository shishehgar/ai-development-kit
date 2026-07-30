"""Plugin discovery and lifecycle management."""

from __future__ import annotations

import importlib
import logging
from dataclasses import dataclass
from importlib import metadata
from threading import RLock
from typing import Any

from aidk.app.registry import ServiceRegistry
from aidk.plugins.base import Plugin


PLUGIN_ENTRYPOINT_GROUP = "aidk.plugins"


class PluginError(RuntimeError):
    """Base error raised by the plugin subsystem."""


class PluginLoadError(PluginError):
    """Raised when a plugin cannot be loaded."""


@dataclass(slots=True)
class PluginRecord:
    """Runtime plugin state."""

    name: str
    version: str
    plugin: Plugin
    source: str
    loaded: bool = True
    started: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "source": self.source,
            "loaded": self.loaded,
            "started": self.started,
        }


class PluginManager:
    """Discover, register and manage AIDK plugins."""

    def __init__(
        self,
        *,
        registry: ServiceRegistry,
        logger: logging.Logger,
    ) -> None:
        self.registry = registry
        self.logger = logger

        self._plugins: dict[
            str,
            PluginRecord,
        ] = {}

        self._lock = RLock()

    @staticmethod
    def _validate_plugin(
        plugin: object,
    ) -> Plugin:
        if not isinstance(
            plugin,
            Plugin,
        ):
            raise PluginLoadError(
                "Object does not implement the "
                "AIDK Plugin protocol."
            )

        if not plugin.name.strip():
            raise PluginLoadError(
                "Plugin name cannot be empty."
            )

        if not plugin.version.strip():
            raise PluginLoadError(
                "Plugin version cannot be empty."
            )

        return plugin

    def register(
        self,
        plugin: Plugin,
        *,
        source: str = "manual",
        replace: bool = False,
    ) -> PluginRecord:
        """Register a plugin instance."""

        validated = self._validate_plugin(
            plugin
        )

        name = validated.name.strip()

        with self._lock:
            if (
                name in self._plugins
                and not replace
            ):
                raise PluginLoadError(
                    f"Plugin is already loaded: {name}"
                )

        validated.register(
            self.registry
        )

        record = PluginRecord(
            name=name,
            version=validated.version.strip(),
            plugin=validated,
            source=source,
        )

        with self._lock:
            self._plugins[name] = record

        self.logger.info(
            "Plugin loaded: %s %s",
            record.name,
            record.version,
        )

        return record

    def load_module(
        self,
        module_path: str,
        *,
        attribute: str = "plugin",
        replace: bool = False,
    ) -> PluginRecord:
        """Load a plugin instance from a Python module."""

        try:
            module = importlib.import_module(
                module_path
            )
        except Exception as exc:
            raise PluginLoadError(
                f"Cannot import plugin module: "
                f"{module_path}"
            ) from exc

        try:
            plugin = getattr(
                module,
                attribute,
            )
        except AttributeError as exc:
            raise PluginLoadError(
                f"Plugin attribute '{attribute}' "
                f"not found in {module_path}."
            ) from exc

        if isinstance(plugin, type):
            plugin = plugin()

        return self.register(
            plugin,
            source=module_path,
            replace=replace,
        )

    def discover(
        self,
    ) -> tuple[metadata.EntryPoint, ...]:
        """Discover installed AIDK entry-point plugins."""

        entry_points = metadata.entry_points()

        if hasattr(
            entry_points,
            "select",
        ):
            discovered = entry_points.select(
                group=PLUGIN_ENTRYPOINT_GROUP
            )
        else:
            discovered = entry_points.get(
                PLUGIN_ENTRYPOINT_GROUP,
                (),
            )

        return tuple(
            sorted(
                discovered,
                key=lambda item: item.name,
            )
        )

    def load_all(
        self,
        *,
        start: bool = False,
        ignore_errors: bool = False,
    ) -> tuple[PluginRecord, ...]:
        """Discover and load all installed plugins."""

        loaded: list[
            PluginRecord
        ] = []

        for entry_point in self.discover():
            try:
                candidate = entry_point.load()

                if isinstance(
                    candidate,
                    type,
                ):
                    candidate = candidate()

                record = self.register(
                    candidate,
                    source=(
                        f"entrypoint:"
                        f"{entry_point.name}"
                    ),
                )

                if start:
                    self.start(
                        record.name
                    )

                loaded.append(record)

            except Exception as exc:
                if not ignore_errors:
                    raise PluginLoadError(
                        "Failed to load plugin "
                        f"entry point: "
                        f"{entry_point.name}"
                    ) from exc

                self.logger.exception(
                    "Plugin load failed: %s",
                    entry_point.name,
                )

        return tuple(loaded)

    def start(
        self,
        name: str,
    ) -> bool:
        """Start a loaded plugin."""

        with self._lock:
            record = self._plugins.get(
                name
            )

        if record is None:
            raise PluginLoadError(
                f"Plugin is not loaded: {name}"
            )

        if record.started:
            return False

        record.plugin.start()
        record.started = True

        self.logger.info(
            "Plugin started: %s",
            name,
        )

        return True

    def stop(
        self,
        name: str,
    ) -> bool:
        """Stop a running plugin."""

        with self._lock:
            record = self._plugins.get(
                name
            )

        if record is None:
            raise PluginLoadError(
                f"Plugin is not loaded: {name}"
            )

        if not record.started:
            return False

        record.plugin.stop()
        record.started = False

        self.logger.info(
            "Plugin stopped: %s",
            name,
        )

        return True

    def start_all(self) -> None:
        for record in self.list():
            self.start(
                record.name
            )

    def stop_all(self) -> None:
        records = tuple(
            reversed(
                self.list()
            )
        )

        for record in records:
            if record.started:
                self.stop(
                    record.name
                )

    def get(
        self,
        name: str,
    ) -> PluginRecord:
        with self._lock:
            record = self._plugins.get(
                name
            )

        if record is None:
            raise PluginLoadError(
                f"Plugin is not loaded: {name}"
            )

        return record

    def list(
        self,
    ) -> tuple[PluginRecord, ...]:
        with self._lock:
            records = tuple(
                self._plugins.values()
            )

        return tuple(
            sorted(
                records,
                key=lambda item: item.name,
            )
        )

    def describe(
        self,
    ) -> list[dict[str, Any]]:
        return [
            record.to_dict()
            for record in self.list()
        ]

    def __len__(self) -> int:
        with self._lock:
            return len(self._plugins)
