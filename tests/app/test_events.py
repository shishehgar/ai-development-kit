"""Tests for the application event bus."""

from __future__ import annotations

from aidk.app.events import (
    ApplicationEvent,
    EventBus,
)


def test_event_is_delivered() -> None:
    bus = EventBus()
    received: list[
        ApplicationEvent
    ] = []

    bus.subscribe(
        "workspace.loaded",
        received.append,
    )

    event = bus.publish(
        "workspace.loaded",
        project_count=4,
    )

    assert received == [event]
    assert event.payload[
        "project_count"
    ] == 4


def test_unsubscribe_removes_handler() -> None:
    bus = EventBus()
    received: list[
        ApplicationEvent
    ] = []

    bus.subscribe(
        "audit.finished",
        received.append,
    )

    bus.unsubscribe(
        "audit.finished",
        received.append,
    )

    bus.publish(
        "audit.finished"
    )

    assert received == []
