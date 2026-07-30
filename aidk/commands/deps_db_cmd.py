"""
Stored dependencies command.
"""

from __future__ import annotations

import json
from argparse import ArgumentParser, Namespace
from pathlib import Path

from aidk.core.command import Command
from aidk.db.dependency_repository import DependencyRepository
from aidk.db.engine import DatabaseEngine


class DependenciesDatabaseCommand(Command):

    @property
    def name(self):
        return "deps-db"

    @property
    def help(self):
        return "Query stored dependency data"

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
            dest="deps_db_command",
        )

        list_parser = subcommands.add_parser(
            "list"
        )

        list_parser.add_argument(
            "--json",
            action="store_true",
        )

        show_parser = subcommands.add_parser(
            "show"
        )

        show_parser.add_argument(
            "project"
        )

        show_parser.add_argument(
            "--json",
            action="store_true",
        )

        find_parser = subcommands.add_parser(
            "find"
        )

        find_parser.add_argument(
            "dependency"
        )

        find_parser.add_argument(
            "--json",
            action="store_true",
        )

        return parser

    def run(
        self,
        args: Namespace,
    ):
        repository = DependencyRepository(
            DatabaseEngine(args.database)
        )

        command = (
            args.deps_db_command
            or "list"
        )

        if command == "list":
            return self._list(
                repository,
                args.json,
            )

        if command == "show":
            return self._show(
                repository,
                args.project,
                args.json,
            )

        if command == "find":
            return self._find(
                repository,
                args.dependency,
                args.json,
            )

        return 1

    @staticmethod
    def _list(
        repository: DependencyRepository,
        as_json: bool,
    ) -> int:
        reports = repository.list_summary()

        if as_json:
            print(
                json.dumps(
                    reports,
                    indent=2,
                    ensure_ascii=False,
                )
            )
            return 0

        if not reports:
            print("No dependency scans found.")
            return 0

        name_width = max(
            len("PROJECT"),
            max(
                len(report["project_name"])
                for report in reports
            ),
        )

        print(
            f"{'PROJECT':<{name_width}}  "
            f"{'TOTAL':>5}  "
            f"{'UNIQUE':>6}  "
            f"{'RUNTIME':>7}  "
            f"{'DEV':>5}  "
            f"{'DUP':>4}  "
            f"{'ERRORS':>6}"
        )

        print(
            f"{'-' * name_width}  "
            f"{'-' * 5}  "
            f"{'-' * 6}  "
            f"{'-' * 7}  "
            f"{'-' * 5}  "
            f"{'-' * 4}  "
            f"{'-' * 6}"
        )

        for report in reports:
            print(
                f"{report['project_name']:<{name_width}}  "
                f"{report['total']:>5}  "
                f"{report['unique_total']:>6}  "
                f"{report['runtime_total']:>7}  "
                f"{report['development_total']:>5}  "
                f"{report['duplicate_total']:>4}  "
                f"{report['error_total']:>6}"
            )

        return 0

    @staticmethod
    def _show(
        repository: DependencyRepository,
        project_name: str,
        as_json: bool,
    ) -> int:
        report = repository.get_project_report(
            project_name
        )

        if report is None:
            print(
                f"Dependency report not found: "
                f"{project_name}"
            )
            return 1

        if as_json:
            print(
                json.dumps(
                    report,
                    indent=2,
                    ensure_ascii=False,
                )
            )
            return 0

        print(
            f"Project: {report['project_name']}"
        )
        print(
            f"Path: {report['project_path']}"
        )
        print(f"Total: {report['total']}")
        print(
            f"Unique: {report['unique_total']}"
        )
        print(
            f"Runtime: {report['runtime_total']}"
        )
        print(
            "Development: "
            f"{report['development_total']}"
        )
        print(
            f"Optional: {report['optional_total']}"
        )
        print(
            f"Duplicates: "
            f"{report['duplicate_total']}"
        )
        print(
            f"Errors: {report['error_total']}"
        )

        dependencies = report[
            "dependencies"
        ]

        if dependencies:
            print("")
            print("Dependencies")

            for dependency in dependencies:
                version = (
                    dependency["version"]
                    or "*"
                )

                print(
                    f"- {dependency['name']} "
                    f"{version} "
                    f"[{dependency['dependency_group']}] "
                    f"({dependency['source']})"
                )

        return 0

    @staticmethod
    def _find(
        repository: DependencyRepository,
        dependency_name: str,
        as_json: bool,
    ) -> int:
        matches = repository.find_dependency(
            dependency_name
        )

        if as_json:
            print(
                json.dumps(
                    matches,
                    indent=2,
                    ensure_ascii=False,
                )
            )
            return 0

        if not matches:
            print(
                f"Dependency not found: "
                f"{dependency_name}"
            )
            return 1

        for match in matches:
            version = (
                match["version"]
                or "*"
            )

            print(
                f"{match['project_name']}: "
                f"{match['name']} {version} "
                f"[{match['dependency_group']}] "
                f"({match['source']})"
            )

        return 0
