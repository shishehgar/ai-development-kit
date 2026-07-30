"""Plugin contracts for AIDK."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from aidk.app.registry import ServiceRegistry


@runtime_checkable
class Plugin(Protocol):
    """Runtime contract for an AIDK plugin."""

    @property
    def name(self) -> str:
        ...

    @property
    def version(self) -> str:
        ...

    def register(
        self,
        registry: ServiceRegistry,
    ) -> None:
        ...

    def start(self) -> None:
        ...

    def stop(self) -> None:
        ...
