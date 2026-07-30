"""Filesystem analyzer for knowledge scanning."""

from __future__ import annotations

from pathlib import Path

from aidk.knowledge.types import (
    Language,
)


PYTHON_SUFFIXES = {
    ".py",
}


def detect_language(
    path: Path,
) -> Language:
    """Detect file language."""

    suffix = path.suffix.lower()

    if suffix in PYTHON_SUFFIXES:
        return Language.PYTHON

    return Language.UNKNOWN



def iter_source_files(
    root: Path,
):
    """
    Iterate project source files.

    Ignores:
        .git
        .venv
        node_modules
    """

    ignored = {
        ".git",
        ".venv",
        "venv",
        "node_modules",
        "__pycache__",
    }

    for path in root.rglob("*"):

        if not path.is_file():
            continue


        if any(
            part in ignored
            for part in path.parts
        ):
            continue


        yield path
