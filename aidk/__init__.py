"""
AI Development Kit (AIDK)

Public package interface.

Only stable APIs should be exported from this module.
"""

from __future__ import annotations

from aidk.config import Config
from aidk.config import get_config
from aidk.config import reload_config

from aidk.version import VERSION
from aidk.version import VersionInfo
from aidk.version import get_version

__all__ = [
    "Config",
    "VersionInfo",
    "VERSION",
    "get_config",
    "reload_config",
    "get_version",
]
