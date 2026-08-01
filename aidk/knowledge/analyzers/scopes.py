"""Python AST scope tracking utilities."""

from __future__ import annotations

from contextlib import contextmanager
from collections.abc import Iterator


class PythonScope:
    """Track nested Python symbol scopes."""

    def __init__(self) -> None:
        self._parts: list[str] = []

    @property
    def parts(self) -> tuple[str, ...]:
        """Return the current immutable scope."""

        return tuple(
            self._parts
        )

    def qualify(
        self,
        name: str,
    ) -> str:
        """Return a name qualified by the current scope."""

        normalized = name.strip()

        if not normalized:
            raise ValueError(
                "Scope name cannot be empty."
            )

        return ".".join(
            [
                *self._parts,
                normalized,
            ]
        )

    @contextmanager
    def enter(
        self,
        name: str,
    ) -> Iterator[None]:
        """Enter and leave a nested scope safely."""

        normalized = name.strip()

        if not normalized:
            raise ValueError(
                "Scope name cannot be empty."
            )

        self._parts.append(
            normalized
        )

        try:
            yield
        finally:
            self._parts.pop()
