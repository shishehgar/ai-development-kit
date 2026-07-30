"""Application lifecycle management."""

from __future__ import annotations

from collections.abc import Callable
from threading import RLock


LifecycleHook = Callable[[], None]


class LifecycleManager:
    """Manage application startup and shutdown hooks."""

    def __init__(self) -> None:
        self._startup_hooks: list[
            LifecycleHook
        ] = []
        self._shutdown_hooks: list[
            LifecycleHook
        ] = []
        self._started = False
        self._lock = RLock()

    @property
    def started(self) -> bool:
        with self._lock:
            return self._started

    def on_startup(
        self,
        hook: LifecycleHook,
    ) -> None:
        with self._lock:
            if hook not in self._startup_hooks:
                self._startup_hooks.append(
                    hook
                )

    def on_shutdown(
        self,
        hook: LifecycleHook,
    ) -> None:
        with self._lock:
            if hook not in self._shutdown_hooks:
                self._shutdown_hooks.append(
                    hook
                )

    def start(self) -> bool:
        with self._lock:
            if self._started:
                return False

            hooks = tuple(
                self._startup_hooks
            )

            self._started = True

        try:
            for hook in hooks:
                hook()
        except Exception:
            with self._lock:
                self._started = False
            raise

        return True

    def stop(self) -> bool:
        with self._lock:
            if not self._started:
                return False

            hooks = tuple(
                reversed(
                    self._shutdown_hooks
                )
            )

            self._started = False

        for hook in hooks:
            hook()

        return True
