"""
Command Dispatcher for AIDK.

Loads command implementations lazily.
"""

from __future__ import annotations

from importlib import import_module


class CommandDispatcher:

    def dispatch(self, command: str | None) -> int:

        if command is None:
            return 0

        commands = {
            "version": (
                "aidk.commands.version",
                "VersionCommand",
            ),
            "doctor": (
                "aidk.commands.doctor",
                "Doctor",
            ),
        }

        if command not in commands:
            raise ValueError(f"Unknown command: {command}")

        module_name, class_name = commands[command]

        module = import_module(module_name)

        command_class = getattr(module, class_name)

        return command_class().run()
