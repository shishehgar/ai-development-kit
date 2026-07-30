"""Runtime configuration for AIDK Studio."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class StudioSettings:
    """Application settings."""

    app_name: str
    version: str
    api_prefix: str
    host: str
    port: int
    workspace_root: Path

    @classmethod
    def from_environment(cls) -> "StudioSettings":
        workspace_root = Path(
            os.getenv(
                "AIDK_STUDIO_WORKSPACE",
                str(Path.home() / "my_services" / "projects"),
            )
        ).expanduser().resolve()

        return cls(
            app_name="AIDK Studio",
            version="0.1.0",
            api_prefix="/api/v1",
            host=os.getenv("AIDK_STUDIO_HOST", "127.0.0.1"),
            port=int(os.getenv("AIDK_STUDIO_PORT", "8765")),
            workspace_root=workspace_root,
        )


settings = StudioSettings.from_environment()
