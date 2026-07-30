"""
Database bootstrap.
"""

from __future__ import annotations

from aidk.db.engine import DatabaseEngine


def bootstrap_database() -> DatabaseEngine:
    """Initialize and return the default database engine."""

    engine = DatabaseEngine()
    engine.initialize()

    return engine
