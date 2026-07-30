"""
Database command.
"""

from __future__ import annotations

import json
from argparse import ArgumentParser, Namespace
from pathlib import Path

from aidk.core.command import Command
from aidk.db.engine import DatabaseEngine
from aidk.db.repository import WorkspaceRepository


class DatabaseCommand(Command):

    @property
    def name(self):
        return "db"

    @property
    def help(self):
        return "Manage workspace database"

    def configure(
        self,
        parser: ArgumentParser,
    ):
        parser.add_argument(
            "--database",
            type=Path,
            default=None,
        )

        subcommands = parser.add_subparsers(
            dest="db_command",
        )

        subcommands.add_parser(
            "status",
            help="Show database status",
        )

        list_parser = subcommands.add_parser(
            "list",
            help="List stored projects",
        )

        list_parser.add_argument(
            "--json",
            action="store_true",
        )

        show_parser = subcommands.add_parser(
            "show",
            help="Show stored project",
        )

        show_parser.add_argument(
            "name",
        )

        show_parser.add_argument(
            "--json",
            action="store_true",
        )

        clear_parser = subcommands.add_parser(
            "clear",
            help="Clear database",
        )

        clear_parser.add_argument(
            "--yes",
            action="store_true",
        )

        subcommands.add_parser(
            "migrations",
            help="Show migration history",
        )

        return parser

    def run(
        self,
        args: Namespace,
    ):
        engine = DatabaseEngine(
            args.database
        )

        repository = WorkspaceRepository(
            engine
        )

        command = args.db_command or "status"

        if command == "status":
            return self._status(
                engine,
                repository,
            )

        if command == "list":
            return self._list(
                repository,
                args.json,
            )

        if command == "show":
            return self._show(
                repository,
                args.name,
                args.json,
            )

        if command == "clear":
            return self._clear(
                repository,
                args.yes,
            )

        if command == "migrations":
            return self._migrations(
                engine
            )

        return 1

    @staticmethod
    def _status(
        engine: DatabaseEngine,
        repository: WorkspaceRepository,
    ) -> int:
        projects = repository.list_projects()

        print(f"Database: {engine.database_path}")
        print(f"Exists: {engine.database_path.exists()}")
        print(f"Schema version: {engine.migration_version()}")
        print(f"Projects: {len(projects)}")

        return 0

    @staticmethod
    def _list(
        repository: WorkspaceRepository,
        as_json: bool,
    ) -> int:
        projects = repository.list_projects()

        if as_json:
            print(
                json.dumps(
                    projects,
                    indent=2,
                    ensure_ascii=False,
                    default=str,
                )
            )

            return 0

        if not projects:
            print("No projects found.")
            return 0

        name_width = max(
            len("NAME"),
            max(
                len(project["name"])
                for project in projects
            ),
        )

        language_width = max(
            len("LANGUAGE"),
            max(
                len(project["language"])
                for project in projects
            ),
        )

        print(
            f"{'NAME':<{name_width}}  "
            f"{'LANGUAGE':<{language_width}}  "
            f"{'ENGINEERING':>11}  "
            f"{'MATURITY':>8}  "
            f"LEVEL"
        )

        print(
            f"{'-' * name_width}  "
            f"{'-' * language_width}  "
            f"{'-' * 11}  "
            f"{'-' * 8}  "
            f"{'-' * 12}"
        )

        for project in projects:
            print(
                f"{project['name']:<{name_width}}  "
                f"{project['language']:<{language_width}}  "
                f"{project['engineering_score']:>11}  "
                f"{project['maturity_score']:>8}  "
                f"{project['maturity_level']}"
            )

        return 0

    @staticmethod
    def _show(
        repository: WorkspaceRepository,
        name: str,
        as_json: bool,
    ) -> int:
        project = repository.get_project(
            name
        )

        if project is None:
            print(
                f"Project not found: {name}"
            )

            return 1

        if as_json:
            print(
                json.dumps(
                    project,
                    indent=2,
                    ensure_ascii=False,
                    default=str,
                )
            )

            return 0

        print(f"Name: {project['name']}")
        print(f"Path: {project['path']}")
        print(f"Language: {project['language']}")
        print(
            "Engineering score: "
            f"{project['engineering_score']}"
        )
        print(
            "Knowledge score: "
            f"{project['knowledge_score']}"
        )
        print(
            "Security score: "
            f"{project['security_score']}"
        )
        print(
            "Deployment score: "
            f"{project['deployment_score']}"
        )
        print(
            "Maturity score: "
            f"{project['maturity_score']}"
        )
        print(
            "Maturity level: "
            f"{project['maturity_level']}"
        )

        features = project.get(
            "features"
        )

        if features:
            print("")
            print("Features")
            print(
                f"Docker: {bool(features['docker'])}"
            )
            print(
                "Continue: "
                f"{bool(features['continue_config'])}"
            )
            print(
                f"README: {bool(features['readme'])}"
            )
            print(
                f"License: {bool(features['license'])}"
            )
            print(
                f"Tests: {bool(features['tests'])}"
            )

        recommendations = project.get(
            "recommendations",
            [],
        )

        if recommendations:
            print("")
            print("Recommendations")

            for recommendation in recommendations:
                print(
                    f"- {recommendation}"
                )

        return 0

    @staticmethod
    def _clear(
        repository: WorkspaceRepository,
        confirmed: bool,
    ) -> int:
        if not confirmed:
            print(
                "Use --yes to confirm database clear."
            )

            return 1

        repository.clear()

        print("Database cleared.")

        return 0

    @staticmethod
    def _migrations(
        engine: DatabaseEngine,
    ) -> int:
        history = engine.migration_history()

        if not history:
            print("No migrations found.")
            return 0

        for migration in history:
            print(
                f"{migration['version']}: "
                f"{migration['name']} "
                f"({migration['applied_at']})"
            )

        return 0
