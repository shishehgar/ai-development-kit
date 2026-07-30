"""
SQLite database engine.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from aidk.db.migrations import MigrationManager


class DatabaseEngine:

    def __init__(
        self,
        database_path: Path | str | None = None,
    ) -> None:
        self.database_path = (
            Path(database_path).expanduser().resolve()
            if database_path is not None
            else Path.home() / ".aidk" / "workspace.db"
        )

    def initialize(self) -> None:
        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.connect() as connection:
            MigrationManager(connection).migrate()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.database_path
        )

        connection.row_factory = sqlite3.Row

        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        connection.execute(
            "PRAGMA journal_mode = WAL"
        )

        connection.execute(
            "PRAGMA synchronous = NORMAL"
        )

        connection.execute(
            "PRAGMA busy_timeout = 5000"
        )

        return connection

    def execute(
        self,
        statement: str,
        parameters: tuple | dict = (),
    ) -> None:
        with self.connect() as connection:
            connection.execute(
                statement,
                parameters,
            )
            connection.commit()

    def execute_many(
        self,
        statement: str,
        parameters: list[tuple] | tuple[tuple, ...],
    ) -> None:
        with self.connect() as connection:
            connection.executemany(
                statement,
                parameters,
            )
            connection.commit()

    def fetch_one(
        self,
        statement: str,
        parameters: tuple | dict = (),
    ) -> sqlite3.Row | None:
        with self.connect() as connection:
            cursor = connection.execute(
                statement,
                parameters,
            )

            return cursor.fetchone()

    def fetch_all(
        self,
        statement: str,
        parameters: tuple | dict = (),
    ) -> list[sqlite3.Row]:
        with self.connect() as connection:
            cursor = connection.execute(
                statement,
                parameters,
            )

            return list(cursor.fetchall())

    def migration_version(self) -> int:
        self.initialize()

        with self.connect() as connection:
            return MigrationManager(
                connection
            ).current_version()

    def migration_history(self) -> list[dict]:
        self.initialize()

        with self.connect() as connection:
            return MigrationManager(
                connection
            ).history()
