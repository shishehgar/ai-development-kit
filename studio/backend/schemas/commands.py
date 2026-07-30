"""Command catalog API schemas."""

from __future__ import annotations

from pydantic import BaseModel


class CommandSummary(BaseModel):
    name: str
    title_fa: str
    description: str
    description_fa: str
    category: str
    safety: str
    cli_equivalent: str
    available: bool = True


class CommandCollection(BaseModel):
    count: int
    commands: list[CommandSummary]
