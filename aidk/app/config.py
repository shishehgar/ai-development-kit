"""Application configuration for AIDK."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _environment_path(
    name: str,
    default: Path,
) -> Path:
    value = os.getenv(name)

    if value:
        return Path(value).expanduser().resolve()

    return default.expanduser().resolve()


def _environment_bool(
    name: str,
    default: bool = False,
) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def _environment_int(
    name: str,
    default: int,
) -> int:
    value = os.getenv(name)

    if value is None:
        return default

    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(
            f"{name} must be an integer."
        ) from exc


@dataclass(frozen=True, slots=True)
class ApplicationConfig:
    """Runtime configuration shared by all AIDK interfaces."""

    workspace: Path
    projects_root: Path
    api_host: str
    api_port: int
    debug: bool
    environment: str
    cache_ttl_seconds: int

    @classmethod
    def from_environment(
        cls,
    ) -> "ApplicationConfig":
        current_directory = Path.cwd().resolve()

        workspace = _environment_path(
            "AIDK_WORKSPACE",
            current_directory,
        )

        projects_root = _environment_path(
            "AIDK_STUDIO_WORKSPACE",
            workspace,
        )

        return cls(
            workspace=workspace,
            projects_root=projects_root,
            api_host=os.getenv(
                "AIDK_API_HOST",
                "127.0.0.1",
            ),
            api_port=_environment_int(
                "AIDK_API_PORT",
                8000,
            ),
            debug=_environment_bool(
                "AIDK_DEBUG",
                False,
            ),
            environment=os.getenv(
                "AIDK_ENVIRONMENT",
                "development",
            ),
            cache_ttl_seconds=_environment_int(
                "AIDK_CACHE_TTL_SECONDS",
                60,
            ),
        )
