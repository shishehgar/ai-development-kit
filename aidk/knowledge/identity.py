"""Stable identity helpers for knowledge entities."""

from __future__ import annotations

from pathlib import PurePath
from uuid import UUID, uuid5


AIDK_ENTITY_NAMESPACE = UUID(
    "7f8c5e44-7f4b-4c54-8d13-2e3f6c9d8a11"
)


def normalize_identity_path(
    path: str,
) -> str:
    """
    Normalize a logical project-relative identity path.

    The path must not depend on the deployment mount point.
    """

    normalized = (
        path
        .replace("\\", "/")
        .strip()
    )

    while normalized.startswith("./"):
        normalized = normalized[2:]

    return str(
        PurePath(normalized)
    ).replace("\\", "/")


def stable_entity_id(
    *,
    project: str,
    kind: str,
    path: str,
    qualified_name: str | None,
    name: str,
) -> UUID:
    """Generate a deterministic UUID5 for a knowledge entity."""

    project_key = (
        project.strip()
        or "unknown"
    )

    kind_key = kind.strip()

    path_key = normalize_identity_path(
        path
    )

    symbol_key = (
        qualified_name
        or name
    ).strip()

    identity_key = "|".join(
        [
            project_key,
            kind_key,
            path_key,
            symbol_key,
        ]
    )

    return uuid5(
        AIDK_ENTITY_NAMESPACE,
        identity_key,
    )
