"""
Service container for AIDK.

Provides singleton access to shared services.
"""

from __future__ import annotations

from aidk.core.logger import get_logger
from aidk.core.environment import get_environment
from aidk.core.config_manager import ConfigManager


class Services:
    """
    Shared service container.
    """

    def __init__(self) -> None:
        self.logger = get_logger()
        self.environment = get_environment()
        self.config = ConfigManager()


services = Services()
