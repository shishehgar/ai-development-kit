"""In-memory TTL cache for AIDK."""

from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from time import monotonic
from typing import Any


@dataclass(slots=True)
class CacheEntry:
    value: Any
    expires_at: float | None

    def expired(
        self,
        now: float,
    ) -> bool:
        return (
            self.expires_at is not None
            and now >= self.expires_at
        )


class TTLCache:
    """Thread-safe in-memory cache with TTL support."""

    def __init__(
        self,
        *,
        default_ttl: int = 60,
    ) -> None:
        if default_ttl < 0:
            raise ValueError(
                "default_ttl cannot be negative."
            )

        self.default_ttl = default_ttl
        self._entries: dict[
            str,
            CacheEntry,
        ] = {}
        self._lock = RLock()

    def set(
        self,
        key: str,
        value: Any,
        *,
        ttl: int | None = None,
    ) -> None:
        effective_ttl = (
            self.default_ttl
            if ttl is None
            else ttl
        )

        if effective_ttl < 0:
            raise ValueError(
                "ttl cannot be negative."
            )

        expires_at = (
            None
            if effective_ttl == 0
            else monotonic() + effective_ttl
        )

        with self._lock:
            self._entries[key] = CacheEntry(
                value=value,
                expires_at=expires_at,
            )

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        now = monotonic()

        with self._lock:
            entry = self._entries.get(key)

            if entry is None:
                return default

            if entry.expired(now):
                self._entries.pop(
                    key,
                    None,
                )
                return default

            return entry.value

    def has(
        self,
        key: str,
    ) -> bool:
        marker = object()

        return self.get(
            key,
            marker,
        ) is not marker

    def delete(
        self,
        key: str,
    ) -> bool:
        with self._lock:
            return (
                self._entries.pop(
                    key,
                    None,
                )
                is not None
            )

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()

    def purge_expired(self) -> int:
        now = monotonic()
        removed = 0

        with self._lock:
            expired_keys = [
                key
                for key, entry
                in self._entries.items()
                if entry.expired(now)
            ]

            for key in expired_keys:
                self._entries.pop(
                    key,
                    None,
                )
                removed += 1

        return removed

    def __len__(self) -> int:
        self.purge_expired()

        with self._lock:
            return len(self._entries)
