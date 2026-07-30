"""Tests for application lifecycle."""

from __future__ import annotations

from aidk.app.lifecycle import LifecycleManager


def test_lifecycle_hooks() -> None:
    lifecycle = LifecycleManager()
    calls: list[str] = []

    lifecycle.on_startup(
        lambda: calls.append(
            "start"
        )
    )

    lifecycle.on_shutdown(
        lambda: calls.append(
            "stop"
        )
    )

    assert lifecycle.start() is True
    assert lifecycle.start() is False
    assert lifecycle.started is True

    assert lifecycle.stop() is True
    assert lifecycle.stop() is False
    assert lifecycle.started is False

    assert calls == [
        "start",
        "stop",
    ]


def test_shutdown_hooks_run_in_reverse_order() -> None:
    lifecycle = LifecycleManager()
    calls: list[str] = []

    lifecycle.on_shutdown(
        lambda: calls.append(
            "first"
        )
    )

    lifecycle.on_shutdown(
        lambda: calls.append(
            "second"
        )
    )

    lifecycle.start()
    lifecycle.stop()

    assert calls == [
        "second",
        "first",
    ]
