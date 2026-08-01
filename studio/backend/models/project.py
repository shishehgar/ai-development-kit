"""Project models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectInfo:
    """
    Registered engineering project.
    """

    id: str

    name: str

    path: str

    status: str = "unknown"
