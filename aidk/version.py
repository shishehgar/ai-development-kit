"""AIDK package metadata."""

from __future__ import annotations


__title__ = "AI Development Kit"
__package_name__ = "aidk"
__description__ = "AI Development Kit command-line toolkit"
__version__ = "1.0.0"
__author__ = "AIDK Contributors"
__author_email__ = ""
__license__ = "MIT"
__url__ = ""
__copyright__ = "Copyright 2026 AIDK Contributors"


def get_version() -> str:
    """Return the current AIDK version."""
    return __version__


def get_version_info() -> tuple[int, int, int]:
    """Return the semantic version as a tuple."""
    parts = __version__.split(".")

    if len(parts) != 3:
        raise ValueError(
            f"Invalid semantic version: {__version__}"
        )

    try:
        return tuple(int(part) for part in parts)
    except ValueError as error:
        raise ValueError(
            f"Invalid semantic version: {__version__}"
        ) from error
