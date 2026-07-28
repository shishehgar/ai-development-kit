"""
Environment and path management for AIDK.
"""

from __future__ import annotations

import os
from pathlib import Path
from dataclasses import dataclass


@dataclass(slots=True)
class Environment:

    workspace: Path
    projects: Path
    continue_dir: Path
    templates: Path
    logs: Path
    cache: Path

    @classmethod
    def discover(cls) -> "Environment":

        workspace = Path(
            os.getenv(
                "AIDK_WORKSPACE",
                "/home/ubuntu/my_services",
            )
        )

        return cls(
            workspace=workspace,
            projects=workspace / "projects",
            continue_dir=workspace / ".continue",
            templates=workspace / "_ai_standards",
            logs=workspace / "logs",
            cache=workspace / ".cache",
        )


_environment: Environment | None = None


def get_environment() -> Environment:

    global _environment

    if _environment is None:
        _environment = Environment.discover()

    return _environment
