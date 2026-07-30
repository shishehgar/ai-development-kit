"""
Workspace database repository.
"""

from __future__ import annotations

from pathlib import Path

from aidk.db.engine import DatabaseEngine


class WorkspaceRepository:
    """Persist and query analyzed workspace projects."""

    def __init__(
        self,
        engine: DatabaseEngine | None = None,
    ) -> None:
        self.engine = engine or DatabaseEngine()
        self.engine.initialize()

    def save_project(self, project) -> int:
        """Insert or update one analyzed project."""

        knowledge_score = getattr(
            getattr(project, "knowledge", None),
            "score",
            0,
        )

        security_score = getattr(
            getattr(project, "security", None),
            "score",
            0,
        )

        deployment_score = getattr(
            getattr(project, "deployment", None),
            "score",
            0,
        )

        maturity_score = getattr(
            getattr(project, "maturity", None),
            "score",
            0,
        )

        maturity_level = getattr(
            getattr(project, "maturity", None),
            "level",
            "Initial",
        )

        with self.engine.connect() as connection:
            connection.execute(
                """
                INSERT INTO projects (
                    name,
                    path,
                    language,
                    engineering_score,
                    knowledge_score,
                    security_score,
                    deployment_score,
                    maturity_score,
                    maturity_level,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(name) DO UPDATE SET
                    path = excluded.path,
                    language = excluded.language,
                    engineering_score = excluded.engineering_score,
                    knowledge_score = excluded.knowledge_score,
                    security_score = excluded.security_score,
                    deployment_score = excluded.deployment_score,
                    maturity_score = excluded.maturity_score,
                    maturity_level = excluded.maturity_level,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (
                    project.name,
                    str(Path(project.path).resolve()),
                    project.language,
                    project.intelligence_score,
                    knowledge_score,
                    security_score,
                    deployment_score,
                    maturity_score,
                    maturity_level,
                ),
            )

            row = connection.execute(
                """
                SELECT id
                FROM projects
                WHERE name = ?
                """,
                (project.name,),
            ).fetchone()

            project_id = int(row["id"])

            self._save_git_info(
                connection,
                project_id,
                project,
            )

            self._save_features(
                connection,
                project_id,
                project,
            )

            self._save_recommendations(
                connection,
                project_id,
                project,
            )

            connection.commit()

            return project_id

    def save_projects(self, projects) -> int:
        """Persist all analyzed projects."""

        count = 0

        for project in projects:
            self.save_project(project)
            count += 1

        return count

    def list_projects(self) -> list[dict]:
        """Return all stored projects."""

        rows = self.engine.fetch_all(
            """
            SELECT *
            FROM projects
            ORDER BY name
            """
        )

        return [
            dict(row)
            for row in rows
        ]

    def get_project(
        self,
        name: str,
    ) -> dict | None:
        """Return one project with related information."""

        project = self.engine.fetch_one(
            """
            SELECT *
            FROM projects
            WHERE name = ?
            """,
            (name,),
        )

        if project is None:
            return None

        project_data = dict(project)
        project_id = project_data["id"]

        git_info = self.engine.fetch_one(
            """
            SELECT *
            FROM git_info
            WHERE project_id = ?
            """,
            (project_id,),
        )

        features = self.engine.fetch_one(
            """
            SELECT *
            FROM project_features
            WHERE project_id = ?
            """,
            (project_id,),
        )

        recommendations = self.engine.fetch_all(
            """
            SELECT recommendation
            FROM recommendations
            WHERE project_id = ?
            ORDER BY id
            """,
            (project_id,),
        )

        project_data["git_info"] = (
            dict(git_info)
            if git_info is not None
            else None
        )

        project_data["features"] = (
            dict(features)
            if features is not None
            else None
        )

        project_data["recommendations"] = [
            row["recommendation"]
            for row in recommendations
        ]

        return project_data

    def clear(self) -> None:
        """Delete all stored workspace data."""

        with self.engine.connect() as connection:
            connection.execute(
                "DELETE FROM recommendations"
            )
            connection.execute(
                "DELETE FROM project_features"
            )
            connection.execute(
                "DELETE FROM git_info"
            )
            connection.execute(
                "DELETE FROM projects"
            )
            connection.commit()

    @staticmethod
    def _save_git_info(
        connection,
        project_id: int,
        project,
    ) -> None:
        git_info = getattr(
            project,
            "git_info",
            None,
        )

        if git_info is None:
            return

        connection.execute(
            """
            INSERT INTO git_info (
                project_id,
                branch,
                clean,
                remote,
                remote_name,
                remote_url,
                last_commit_hash,
                last_commit_author,
                last_commit_date,
                modified_files,
                staged_files,
                untracked_files
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(project_id) DO UPDATE SET
                branch = excluded.branch,
                clean = excluded.clean,
                remote = excluded.remote,
                remote_name = excluded.remote_name,
                remote_url = excluded.remote_url,
                last_commit_hash = excluded.last_commit_hash,
                last_commit_author = excluded.last_commit_author,
                last_commit_date = excluded.last_commit_date,
                modified_files = excluded.modified_files,
                staged_files = excluded.staged_files,
                untracked_files = excluded.untracked_files
            """,
            (
                project_id,
                git_info.branch,
                int(git_info.clean),
                int(git_info.remote),
                git_info.remote_name,
                git_info.remote_url,
                git_info.last_commit_hash,
                git_info.last_commit_author,
                git_info.last_commit_date,
                git_info.modified_files,
                git_info.staged_files,
                git_info.untracked_files,
            ),
        )

    @staticmethod
    def _save_features(
        connection,
        project_id: int,
        project,
    ) -> None:
        connection.execute(
            """
            INSERT INTO project_features (
                project_id,
                docker,
                continue_config,
                readme,
                license,
                tests
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(project_id) DO UPDATE SET
                docker = excluded.docker,
                continue_config = excluded.continue_config,
                readme = excluded.readme,
                license = excluded.license,
                tests = excluded.tests
            """,
            (
                project_id,
                int(project.docker),
                int(project.continue_config),
                int(project.readme),
                int(project.license),
                int(project.tests),
            ),
        )

    @staticmethod
    def _save_recommendations(
        connection,
        project_id: int,
        project,
    ) -> None:
        connection.execute(
            """
            DELETE FROM recommendations
            WHERE project_id = ?
            """,
            (project_id,),
        )

        for recommendation in project.recommendations:
            connection.execute(
                """
                INSERT INTO recommendations (
                    project_id,
                    recommendation
                )
                VALUES (?, ?)
                """,
                (
                    project_id,
                    recommendation,
                ),
            )
