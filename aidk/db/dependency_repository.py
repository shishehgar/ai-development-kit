"""
Dependency database repository.
"""

from __future__ import annotations

from aidk.db.engine import DatabaseEngine
from aidk.dependency.models import DependencyReport


class DependencyRepository:

    def __init__(
        self,
        engine: DatabaseEngine | None = None,
    ) -> None:
        self.engine = engine or DatabaseEngine()
        self.engine.initialize()

    def save_report(
        self,
        project_id: int,
        report: DependencyReport,
    ) -> None:
        with self.engine.connect() as connection:
            connection.execute(
                """
                DELETE FROM dependency_errors
                WHERE project_id = ?
                """,
                (project_id,),
            )

            connection.execute(
                """
                DELETE FROM dependency_files
                WHERE project_id = ?
                """,
                (project_id,),
            )

            connection.execute(
                """
                DELETE FROM dependencies
                WHERE project_id = ?
                """,
                (project_id,),
            )

            connection.execute(
                """
                DELETE FROM dependency_scans
                WHERE project_id = ?
                """,
                (project_id,),
            )

            connection.execute(
                """
                INSERT INTO dependency_scans (
                    project_id,
                    total,
                    unique_total,
                    runtime_total,
                    development_total,
                    optional_total,
                    duplicate_total,
                    error_total,
                    scanned_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """,
                (
                    project_id,
                    report.total,
                    report.unique_total,
                    report.runtime_total,
                    report.development_total,
                    report.optional_total,
                    len(report.duplicates),
                    len(report.errors),
                ),
            )

            connection.executemany(
                """
                INSERT INTO dependencies (
                    project_id,
                    normalized_name,
                    name,
                    version,
                    source,
                    dependency_group,
                    optional
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        project_id,
                        dependency.normalized_name,
                        dependency.name,
                        dependency.version,
                        dependency.source,
                        dependency.group,
                        int(dependency.optional),
                    )
                    for dependency in report.dependencies
                ],
            )

            connection.executemany(
                """
                INSERT INTO dependency_files (
                    project_id,
                    path
                )
                VALUES (?, ?)
                """,
                [
                    (
                        project_id,
                        str(file_path),
                    )
                    for file_path in report.files
                ],
            )

            connection.executemany(
                """
                INSERT INTO dependency_errors (
                    project_id,
                    error
                )
                VALUES (?, ?)
                """,
                [
                    (
                        project_id,
                        error,
                    )
                    for error in report.errors
                ],
            )

            connection.commit()

    def get_report(
        self,
        project_id: int,
    ) -> dict | None:
        scan = self.engine.fetch_one(
            """
            SELECT *
            FROM dependency_scans
            WHERE project_id = ?
            """,
            (project_id,),
        )

        if scan is None:
            return None

        dependencies = self.engine.fetch_all(
            """
            SELECT
                normalized_name,
                name,
                version,
                source,
                dependency_group,
                optional
            FROM dependencies
            WHERE project_id = ?
            ORDER BY normalized_name, dependency_group, source
            """,
            (project_id,),
        )

        files = self.engine.fetch_all(
            """
            SELECT path
            FROM dependency_files
            WHERE project_id = ?
            ORDER BY path
            """,
            (project_id,),
        )

        errors = self.engine.fetch_all(
            """
            SELECT error
            FROM dependency_errors
            WHERE project_id = ?
            ORDER BY id
            """,
            (project_id,),
        )

        result = dict(scan)

        result["dependencies"] = [
            dict(row)
            for row in dependencies
        ]

        result["files"] = [
            row["path"]
            for row in files
        ]

        result["errors"] = [
            row["error"]
            for row in errors
        ]

        return result

    def get_project_report(
        self,
        project_name: str,
    ) -> dict | None:
        project = self.engine.fetch_one(
            """
            SELECT id, name, path
            FROM projects
            WHERE name = ?
            """,
            (project_name,),
        )

        if project is None:
            return None

        report = self.get_report(
            int(project["id"])
        )

        if report is None:
            return None

        report["project_name"] = project["name"]
        report["project_path"] = project["path"]

        return report

    def list_summary(self) -> list[dict]:
        rows = self.engine.fetch_all(
            """
            SELECT
                projects.name AS project_name,
                projects.path AS project_path,
                dependency_scans.total,
                dependency_scans.unique_total,
                dependency_scans.runtime_total,
                dependency_scans.development_total,
                dependency_scans.optional_total,
                dependency_scans.duplicate_total,
                dependency_scans.error_total,
                dependency_scans.scanned_at
            FROM dependency_scans
            INNER JOIN projects
                ON projects.id = dependency_scans.project_id
            ORDER BY projects.name
            """
        )

        return [
            dict(row)
            for row in rows
        ]

    def find_dependency(
        self,
        dependency_name: str,
    ) -> list[dict]:
        normalized_name = (
            dependency_name
            .strip()
            .lower()
            .replace("_", "-")
        )

        rows = self.engine.fetch_all(
            """
            SELECT
                projects.name AS project_name,
                projects.path AS project_path,
                dependencies.name,
                dependencies.normalized_name,
                dependencies.version,
                dependencies.source,
                dependencies.dependency_group,
                dependencies.optional
            FROM dependencies
            INNER JOIN projects
                ON projects.id = dependencies.project_id
            WHERE dependencies.normalized_name = ?
            ORDER BY projects.name, dependencies.source
            """,
            (normalized_name,),
        )

        return [
            dict(row)
            for row in rows
        ]
