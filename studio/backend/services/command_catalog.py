"""Discover AIDK capabilities from the existing command registry."""

from __future__ import annotations

from aidk.core.load_commands import build_registry

from studio.backend.help.catalog import HELP_CATALOG
from studio.backend.schemas.commands import CommandSummary


class CommandCatalogService:
    """Expose registered AIDK commands without duplicating CLI definitions."""

    def list_commands(self) -> list[CommandSummary]:
        registry = build_registry()
        commands: list[CommandSummary] = []

        for command in registry.all():
            help_entry = HELP_CATALOG.get(command.name, {})

            commands.append(
                CommandSummary(
                    name=command.name,
                    title_fa=help_entry.get("title_fa", command.name),
                    description=command.help,
                    description_fa=help_entry.get(
                        "description_fa",
                        command.help,
                    ),
                    category=help_entry.get("category", "other"),
                    safety=help_entry.get("safety", "unknown"),
                    cli_equivalent=f"aidk {command.name}",
                )
            )

        return commands

    def get_command(self, command_name: str) -> CommandSummary | None:
        for command in self.list_commands():
            if command.name == command_name:
                return command

        return None
