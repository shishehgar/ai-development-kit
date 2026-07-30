"""Runtime configuration for AIDK Studio."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class StudioSettings:
    """Application settings loaded from environment variables."""

    app_name: str = "AIDK Studio"
    version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    host: str = "127.0.0.1"
    port: int = 8765
    workspace_root: Path = Path.home() / "my_services" / "projects"

    @classmethod
    def from_environment(cls) -> "StudioSettings":
        workspace = Path(
            os.getenv(
                "AIDK_STUDIO_WORKSPACE",
                str(Path.home() / "my_services" / "projects"),
            )
        ).expanduser()

        return cls(
            host=os.getenv("AIDK_STUDIO_HOST", "127.0.0.1"),
            port=int(os.getenv("AIDK_STUDIO_PORT", "8765")),
            workspace_root=workspace.resolve(),
        )


settings = StudioSettings.from_environment()
