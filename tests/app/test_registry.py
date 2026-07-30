"""Tests for the AIDK dependency registry."""

from __future__ import annotations

import pytest

from aidk.app.registry import (
    ServiceLifetime,
    ServiceRegistrationError,
    ServiceRegistry,
    ServiceResolutionErrorLookup,
)


class ExampleService:
    pass


class AlternateService(
    ExampleService
):
    pass


def test_register_and_resolve_instance() -> None:
    registry = ServiceRegistry()
    instance = ExampleService()

    registry.register_instance(
        ExampleService,
        instance,
    )

    assert (
        registry.resolve(
            ExampleService
        )
        is instance
    )


def test_singleton_factory_runs_once() -> None:
    registry = ServiceRegistry()
    calls: list[int] = []

    def factory(
        _registry: ServiceRegistry,
    ) -> ExampleService:
        calls.append(1)
        return ExampleService()

    registry.register_singleton(
        ExampleService,
        factory=factory,
    )

    first = registry.resolve(
        ExampleService
    )

    second = registry.resolve(
        ExampleService
    )

    assert first is second
    assert calls == [1]


def test_transient_factory_runs_each_time() -> None:
    registry = ServiceRegistry()

    registry.register_transient(
        ExampleService
    )

    first = registry.resolve(
        ExampleService
    )

    second = registry.resolve(
        ExampleService
    )

    assert first is not second


def test_named_registration() -> None:
    registry = ServiceRegistry()

    registry.register_instance(
        ExampleService,
        ExampleService(),
        name="default",
    )

    alternate = AlternateService()

    registry.register_instance(
        ExampleService,
        alternate,
        name="alternate",
    )

    assert (
        registry.resolve(
            ExampleService,
            name="alternate",
        )
        is alternate
    )


def test_duplicate_registration_fails() -> None:
    registry = ServiceRegistry()

    registry.register_instance(
        ExampleService,
        ExampleService(),
    )

    with pytest.raises(
        ServiceRegistrationError
    ):
        registry.register_instance(
            ExampleService,
            ExampleService(),
        )


def test_registration_can_be_replaced() -> None:
    registry = ServiceRegistry()

    registry.register_instance(
        ExampleService,
        ExampleService(),
    )

    replacement = AlternateService()

    registry.register_instance(
        ExampleService,
        replacement,
        replace=True,
    )

    assert (
        registry.resolve(
            ExampleService
        )
        is replacement
    )


def test_missing_service_fails() -> None:
    registry = ServiceRegistry()

    with pytest.raises(
        ServiceResolutionErrorLookup
    ):
        registry.resolve(
            ExampleService
        )


def test_describe_registration() -> None:
    registry = ServiceRegistry()

    registry.register_singleton(
        ExampleService
    )

    descriptions = (
        registry.describe()
    )

    assert len(descriptions) == 1
    assert descriptions[0].lifetime == (
        ServiceLifetime.SINGLETON.value
    )
    assert descriptions[0].initialized is False
