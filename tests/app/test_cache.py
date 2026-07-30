"""Tests for the AIDK TTL cache."""

from __future__ import annotations

import time

from aidk.app.cache import TTLCache


def test_cache_stores_value() -> None:
    cache = TTLCache(
        default_ttl=60
    )

    cache.set(
        "project",
        {"name": "aidk"},
    )

    assert cache.get(
        "project"
    ) == {"name": "aidk"}

    assert cache.has(
        "project"
    )


def test_zero_ttl_does_not_expire() -> None:
    cache = TTLCache(
        default_ttl=0
    )

    cache.set(
        "persistent",
        42,
    )

    assert cache.get(
        "persistent"
    ) == 42


def test_expired_value_is_removed() -> None:
    cache = TTLCache(
        default_ttl=60
    )

    cache.set(
        "temporary",
        "value",
        ttl=1,
    )

    time.sleep(1.05)

    assert cache.get(
        "temporary"
    ) is None

    assert len(cache) == 0


def test_delete_returns_status() -> None:
    cache = TTLCache()

    cache.set(
        "item",
        1,
    )

    assert cache.delete(
        "item"
    ) is True

    assert cache.delete(
        "item"
    ) is False
