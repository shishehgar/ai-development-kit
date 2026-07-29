"""
Simple in-memory cache.

This module provides a lightweight cache used by expensive
detectors and analyzers during a single execution.
"""

from __future__ import annotations

from typing import Any


class Cache:
    """Simple dictionary-based cache."""

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    def has(self, key: str) -> bool:
        return key in self._data

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def clear(self) -> None:
        self._data.clear()

    @property
    def size(self) -> int:
        return len(self._data)


cache = Cache()
