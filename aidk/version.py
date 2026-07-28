"""
AIDK Version Information.

Single source of truth for version metadata.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VersionInfo:
    """
    Immutable version information.
    """

    major: int = 0
    minor: int = 1
    patch: int = 0
    stage: str = "alpha"

    @property
    def full(self) -> str:
        """
        Returns the complete version string.
        """
        return (
            f"{self.major}."
            f"{self.minor}."
            f"{self.patch}-"
            f"{self.stage}"
        )


VERSION = VersionInfo()


def get_version() -> str:
    """
    Returns application version.
    """
    return VERSION.full
