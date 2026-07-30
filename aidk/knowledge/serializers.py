"""Serialization helpers for knowledge graph."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def save_snapshot(
    path: str | Path,
    payload: dict[str, Any],
) -> None:
    """
    Save knowledge snapshot.
    """

    target = Path(path)

    target.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    target.write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )



def load_snapshot(
    path: str | Path,
) -> dict[str, Any]:

    source = Path(path)

    return json.loads(
        source.read_text(
            encoding="utf-8"
        )
    )
