"""API response models for system information."""

from __future__ import annotations

from pydantic import BaseModel


class SystemStatus(BaseModel):
    name: str
    version: str
    status: str
    api_prefix: str
    workspace_root: str
    command_count: int
