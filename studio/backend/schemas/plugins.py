"""Plugin API schemas."""

from __future__ import annotations

from pydantic import BaseModel


class PluginResponse(BaseModel):
    name: str
    version: str
    source: str
    loaded: bool
    started: bool


class PluginsResponse(BaseModel):
    loaded: int
    discovered: int
    plugins: list[PluginResponse]
