"""Tests for the AIDK plugin manager."""

from __future__ import annotations

import logging

import pytest

from aidk.app.plugins import (
    PluginLoadError,
    PluginManager,
)
from aidk.app.registry import (
    ServiceRegistry,
)


class PluginService:
    def message(self) -> str:
        return "plugin-ready"


class ExamplePlugin:
    name = "example"
    version = "1.0.0"

    def __init__(self) -> None:
        self.started = False
        self.stopped = False

    def register(
        self,
        registry: ServiceRegistry,
    ) -> None:
        registry.register_instance(
            PluginService,
            PluginService(),
        )

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.stopped = True


def build_manager() -> PluginManager:
    return PluginManager(
        registry=ServiceRegistry(),
        logger=logging.getLogger(
            "aidk.tests.plugins"
        ),
    )


def test_register_plugin() -> None:
    manager = build_manager()
    plugin = ExamplePlugin()

    record = manager.register(
        plugin
    )

    assert record.name == "example"

    service = manager.registry.resolve(
        PluginService
    )

    assert service.message() == (
        "plugin-ready"
    )


def test_plugin_lifecycle() -> None:
    manager = build_manager()
    plugin = ExamplePlugin()

    manager.register(
        plugin
    )

    assert manager.start(
        "example"
    ) is True

    assert manager.start(
        "example"
    ) is False

    assert plugin.started is True

    assert manager.stop(
        "example"
    ) is True

    assert manager.stop(
        "example"
    ) is False

    assert plugin.stopped is True


def test_duplicate_plugin_fails() -> None:
    manager = build_manager()

    manager.register(
        ExamplePlugin()
    )

    with pytest.raises(
        PluginLoadError
    ):
        manager.register(
            ExamplePlugin()
        )


def test_plugin_description() -> None:
    manager = build_manager()

    manager.register(
        ExamplePlugin()
    )

    description = (
        manager.describe()
    )

    assert description == [
        {
            "name": "example",
            "version": "1.0.0",
            "source": "manual",
            "loaded": True,
            "started": False,
        }
    ]
