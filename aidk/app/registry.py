"""Runtime service registry and dependency resolution."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass
from enum import Enum
from threading import RLock
from typing import Any, Generic, TypeVar, cast


T = TypeVar("T")
Factory = Callable[["ServiceRegistry"], Any]


class ServiceLifetime(str, Enum):
    """Supported dependency lifetimes."""

    SINGLETON = "singleton"
    TRANSIENT = "transient"


class ServiceRegistrationError(RuntimeError):
    """Raised when a registration operation is invalid."""


class ServiceResolutionErrorLookup(LookupError):
    """Raised when a dependency cannot be resolved."""


@dataclass(slots=True)
class ServiceDescriptor(Generic[T]):
    """Metadata describing one registered dependency."""

    service_type: type[T]
    factory: Factory
    lifetime: ServiceLifetime
    implementation_type: type[Any] | None = None
    name: str | None = None
    instance: T | None = None

    @property
    def key(self) -> str:
        return self.name or self.service_type.__qualname__


@dataclass(frozen=True, slots=True)
class RegisteredService:
    """Serializable service-registration summary."""

    service: str
    implementation: str
    lifetime: str
    name: str | None
    initialized: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "service": self.service,
            "implementation": self.implementation,
            "lifetime": self.lifetime,
            "name": self.name,
            "initialized": self.initialized,
        }


class ServiceRegistry:
    """Thread-safe dependency registry and resolver."""

    def __init__(self) -> None:
        self._services: dict[
            tuple[type[Any], str | None],
            ServiceDescriptor[Any],
        ] = {}

        self._lock = RLock()
        self._resolving: set[
            tuple[type[Any], str | None]
        ] = set()

    @staticmethod
    def _registration_key(
        service_type: type[Any],
        name: str | None,
    ) -> tuple[type[Any], str | None]:
        return service_type, name

    def register_instance(
        self,
        service_type: type[T],
        instance: T,
        *,
        name: str | None = None,
        replace: bool = False,
    ) -> T:
        """Register an existing singleton instance."""

        return self.register_factory(
            service_type,
            lambda _: instance,
            lifetime=ServiceLifetime.SINGLETON,
            implementation_type=type(instance),
            name=name,
            replace=replace,
            instance=instance,
        )

    def register_factory(
        self,
        service_type: type[T],
        factory: Callable[["ServiceRegistry"], T],
        *,
        lifetime: ServiceLifetime = ServiceLifetime.SINGLETON,
        implementation_type: type[Any] | None = None,
        name: str | None = None,
        replace: bool = False,
        instance: T | None = None,
    ) -> T:
        """Register a factory for a service type."""

        key = self._registration_key(
            service_type,
            name,
        )

        with self._lock:
            if key in self._services and not replace:
                raise ServiceRegistrationError(
                    "Service is already registered: "
                    f"{service_type.__qualname__}"
                    + (
                        f" [{name}]"
                        if name
                        else ""
                    )
                )

            descriptor = ServiceDescriptor(
                service_type=service_type,
                factory=cast(
                    Factory,
                    factory,
                ),
                lifetime=lifetime,
                implementation_type=implementation_type,
                name=name,
                instance=instance,
            )

            self._services[key] = descriptor

        return cast(T, instance)

    def register_singleton(
        self,
        service_type: type[T],
        implementation_type: type[T] | None = None,
        *,
        factory: Callable[
            ["ServiceRegistry"],
            T,
        ] | None = None,
        name: str | None = None,
        replace: bool = False,
    ) -> None:
        """Register a lazily created singleton."""

        implementation = (
            implementation_type
            or service_type
        )

        resolved_factory = (
            factory
            or (
                lambda _: implementation()
            )
        )

        self.register_factory(
            service_type,
            resolved_factory,
            lifetime=ServiceLifetime.SINGLETON,
            implementation_type=implementation,
            name=name,
            replace=replace,
        )

    def register_transient(
        self,
        service_type: type[T],
        implementation_type: type[T] | None = None,
        *,
        factory: Callable[
            ["ServiceRegistry"],
            T,
        ] | None = None,
        name: str | None = None,
        replace: bool = False,
    ) -> None:
        """Register a service created on every resolution."""

        implementation = (
            implementation_type
            or service_type
        )

        resolved_factory = (
            factory
            or (
                lambda _: implementation()
            )
        )

        self.register_factory(
            service_type,
            resolved_factory,
            lifetime=ServiceLifetime.TRANSIENT,
            implementation_type=implementation,
            name=name,
            replace=replace,
        )

    def resolve(
        self,
        service_type: type[T],
        *,
        name: str | None = None,
    ) -> T:
        """Resolve a registered dependency."""

        key = self._registration_key(
            service_type,
            name,
        )

        with self._lock:
            descriptor = self._services.get(
                key
            )

            if descriptor is None:
                raise ServiceResolutionErrorLookup(
                    "Service is not registered: "
                    f"{service_type.__qualname__}"
                    + (
                        f" [{name}]"
                        if name
                        else ""
                    )
                )

            if (
                descriptor.lifetime
                is ServiceLifetime.SINGLETON
                and descriptor.instance is not None
            ):
                return cast(
                    T,
                    descriptor.instance,
                )

            if key in self._resolving:
                raise ServiceRegistrationError(
                    "Circular dependency detected while "
                    "resolving "
                    f"{service_type.__qualname__}."
                )

            self._resolving.add(key)

        try:
            instance = descriptor.factory(
                self
            )
        finally:
            with self._lock:
                self._resolving.discard(
                    key
                )

        if instance is None:
            raise ServiceRegistrationError(
                "Service factory returned None: "
                f"{service_type.__qualname__}"
            )

        if descriptor.lifetime is ServiceLifetime.SINGLETON:
            with self._lock:
                current = self._services[key]

                if current.instance is None:
                    current.instance = instance

                instance = current.instance

        return cast(T, instance)

    def try_resolve(
        self,
        service_type: type[T],
        *,
        name: str | None = None,
        default: T | None = None,
    ) -> T | None:
        """Resolve a service or return a default."""

        try:
            return self.resolve(
                service_type,
                name=name,
            )
        except ServiceResolutionErrorLookup:
            return default

    def contains(
        self,
        service_type: type[Any],
        *,
        name: str | None = None,
    ) -> bool:
        key = self._registration_key(
            service_type,
            name,
        )

        with self._lock:
            return key in self._services

    def unregister(
        self,
        service_type: type[Any],
        *,
        name: str | None = None,
    ) -> bool:
        key = self._registration_key(
            service_type,
            name,
        )

        with self._lock:
            return (
                self._services.pop(
                    key,
                    None,
                )
                is not None
            )

    def describe(
        self,
    ) -> tuple[RegisteredService, ...]:
        """Return registration metadata."""

        with self._lock:
            descriptors = tuple(
                self._services.values()
            )

        result: list[
            RegisteredService
        ] = []

        for descriptor in descriptors:
            implementation = (
                descriptor.implementation_type
                or (
                    type(descriptor.instance)
                    if descriptor.instance is not None
                    else descriptor.service_type
                )
            )

            result.append(
                RegisteredService(
                    service=(
                        f"{descriptor.service_type.__module__}."
                        f"{descriptor.service_type.__qualname__}"
                    ),
                    implementation=(
                        f"{implementation.__module__}."
                        f"{implementation.__qualname__}"
                    ),
                    lifetime=descriptor.lifetime.value,
                    name=descriptor.name,
                    initialized=(
                        descriptor.instance
                        is not None
                    ),
                )
            )

        return tuple(
            sorted(
                result,
                key=lambda item: (
                    item.service,
                    item.name or "",
                ),
            )
        )

    def clear(self) -> None:
        with self._lock:
            self._services.clear()
            self._resolving.clear()

    def __len__(self) -> int:
        with self._lock:
            return len(self._services)

    def __iter__(
        self,
    ) -> Iterator[RegisteredService]:
        return iter(
            self.describe()
        )
