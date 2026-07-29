"""
Version command.
"""

from __future__ import annotations

import platform
import sys
from pathlib import Path

from aidk.core.services import services
from aidk.version import __version__


class VersionCommand:
    """Display version and environment information."""

    def run(self) -> int:
        root = Path(__file__).resolve().parents[2]

        print()
        print("AI Development Kit")
        print()
        print(f"Version      : {__version__}")
        print(f"Python       : {platform.python_version()}")
        print(f"Platform     : {platform.system()}")
        print(f"Workspace    : {services.environment.workspace}")
        print(f"Project Root : {root}")
        print()

        return 0
