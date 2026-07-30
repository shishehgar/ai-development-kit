"""Synchronous application event bus."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import RLock
from typing import Any
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class ApplicationEvent:
    """Application-level event."""

    name: str
    payload: dict[str, Any] = field(
        default_factory=dict
    )
    event_id: str = field(
        default_factory=lambda: str(
            uuid4()
        )
    )
    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )


EventHandler = Callable[
    [ApplicationEvent],
    None,
]


class EventBus:
    """Small thread-safe synchronous event bus."""

    def __init__(self) -> None:
        self._handlers: dict[
            str,
            list[EventHandler],
        ] = defaultdict(list)

        self._lock = RLock()

    def subscribe(
        self,
        event_name: str,
        handler: EventHandler,
    ) -> None:
        with self._lock:
            if handler not in self._handlers[
                event_name
            ]:
                self._handlers[
                    event_name
                ].append(handler)

    def unsubscribe(
        self,
        event_name: str,
        handler: EventHandler,
    ) -> None:
        with self._lock:
            handlers = self._handlers.get(
                event_name,
                [],
            )

            if handler in handlers:
                handlers.remove(handler)

            if not handlers:
                self._handlers.pop(
                    event_name,
                    None,
                )

    def emit(
        self,
        event: ApplicationEvent,
    ) -> None:
        with self._lock:
            handlers = tuple(
                self._handlers.get(
                    event.name,
                    (),
                )
            )

        for handler in handlers:
            handler(event)

    def publish(
        self,
        name: str,
        **payload: Any,
    ) -> ApplicationEvent:
        event = ApplicationEvent(
            name=name,
            payload=payload,
        )

        self.emit(event)

        return event

    def clear(self) -> None:
        with self._lock:
            self._handlers.clear()
