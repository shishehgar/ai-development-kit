"""
Configuration management for AIDK.

This module provides a lightweight configuration manager.
Future versions will support YAML, .env files, environment
variables, runtime overrides, and profile-based settings.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from aidk.constants import (
    CONFIG_FILE_NAME,
    DEFAULT_WORKSPACE,
)


@dataclass(slots=True)
class Config:
    """
    Global application configuration.

    Attributes
    ----------
    workspace:
        Root workspace directory.

    config_file:
        Configuration file path.
    """

    workspace: Path
    config_file: Path

    @classmethod
    def create(cls) -> "Config":
        """
        Create configuration using default values.
        """

        workspace = DEFAULT_WORKSPACE

        return cls(
            workspace=workspace,
            config_file=workspace / CONFIG_FILE_NAME,
        )

    def exists(self) -> bool:
        """
        Check whether config file exists.
        """

        return self.config_file.exists()

    def as_dict(self) -> dict[str, Any]:
        """
        Convert configuration to dictionary.
        """

        return {
            "workspace": str(self.workspace),
            "config_file": str(self.config_file),
        }


_CONFIG: Config | None = None


def get_config() -> Config:
    """
    Return singleton configuration object.
    """

    global _CONFIG

    if _CONFIG is None:
        _CONFIG = Config.create()

    return _CONFIG


def reload_config() -> Config:
    """
    Recreate configuration object.
    """

    global _CONFIG

    _CONFIG = Config.create()

    return _CONFIG
