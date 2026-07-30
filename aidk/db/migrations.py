"""
Database migrations.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Callable

from aidk.db.schema import SCHEMA


@dataclass(frozen=True)
class Migration:
    version: int
    name: str
    apply: Callable[[sqlite3.Connection], None]


def migration_001_initial_schema(
    connection: sqlite3.Connection,
) -> None:
    connection.executescript(SCHEMA)


def migration_002_dependencies(
    connection: sqlite3.Connection,
) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS dependency_scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL UNIQUE,
            total INTEGER NOT NULL DEFAULT 0,
            unique_total INTEGER NOT NULL DEFAULT 0,
            runtime_total INTEGER NOT NULL DEFAULT 0,
            development_total INTEGER NOT NULL DEFAULT 0,
            optional_total INTEGER NOT NULL DEFAULT 0,
            duplicate_total INTEGER NOT NULL DEFAULT 0,
            error_total INTEGER NOT NULL DEFAULT 0,
            scanned_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id)
                REFERENCES projects(id)
                ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS dependencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            normalized_name TEXT NOT NULL,
            name TEXT NOT NULL,
            version TEXT NOT NULL DEFAULT '',
            source TEXT NOT NULL DEFAULT '',
            dependency_group TEXT NOT NULL DEFAULT 'runtime',
            optional INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id)
                REFERENCES projects(id)
                ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS dependency_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            path TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(project_id, path),
            FOREIGN KEY (project_id)
                REFERENCES projects(id)
                ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS dependency_errors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            error TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id)
                REFERENCES projects(id)
                ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_dependencies_project
        ON dependencies(project_id);

        CREATE INDEX IF NOT EXISTS idx_dependencies_name
        ON dependencies(normalized_name);

        CREATE INDEX IF NOT EXISTS idx_dependency_files_project
        ON dependency_files(project_id);

        CREATE INDEX IF NOT EXISTS idx_dependency_errors_project
        ON dependency_errors(project_id);
        """
    )


MIGRATIONS = (
    Migration(
        version=1,
        name="initial_schema",
        apply=migration_001_initial_schema,
    ),
    Migration(
        version=2,
        name="dependencies",
        apply=migration_002_dependencies,
    ),
)


class MigrationManager:

    def __init__(
        self,
        connection: sqlite3.Connection,
    ) -> None:
        self.connection = connection

    def migrate(self) -> int:
        self._create_migration_table()

        current_version = self.current_version()
        applied = 0

        for migration in MIGRATIONS:
            if migration.version <= current_version:
                continue

            try:
                migration.apply(self.connection)

                self.connection.execute(
                    """
                    INSERT INTO schema_migrations (
                        version,
                        name
                    )
                    VALUES (?, ?)
                    """,
                    (
                        migration.version,
                        migration.name,
                    ),
                )

                self.connection.commit()
                applied += 1

            except Exception:
                self.connection.rollback()
                raise

        return applied

    def current_version(self) -> int:
        self._create_migration_table()

        row = self.connection.execute(
            """
            SELECT COALESCE(MAX(version), 0) AS version
            FROM schema_migrations
            """
        ).fetchone()

        return int(row["version"])

    def history(self) -> list[dict]:
        self._create_migration_table()

        rows = self.connection.execute(
            """
            SELECT
                version,
                name,
                applied_at
            FROM schema_migrations
            ORDER BY version
            """
        ).fetchall()

        return [
            dict(row)
            for row in rows
        ]

    def _create_migration_table(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        self.connection.commit()
