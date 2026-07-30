"""
Dependencies command.
"""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path

from aidk.core.command import Command
from aidk.dependency.engine import DependencyEngine
from aidk.dependency.printer import DependencyPrinter


class DependenciesCommand(Command):

    @property
    def name(self):
        return "deps"

    @property
    def help(self):
        return "Inspect project dependencies"

    def configure(
        self,
        parser: ArgumentParser,
    ):
        parser.add_argument(
            "path",
            nargs="?",
            default=".",
        )

        parser.add_argument(
            "--json",
            action="store_true",
        )

        parser.add_argument(
            "--duplicates-only",
            action="store_true",
        )

        return parser

    def run(
        self,
        args: Namespace,
    ):
        project_path = Path(
            args.path
        ).expanduser().resolve()

        if not project_path.exists():
            print(
                f"Path not found: {project_path}"
            )
            return 1

        if not project_path.is_dir():
            print(
                f"Not a directory: {project_path}"
            )
            return 1

        engine = DependencyEngine()
        printer = DependencyPrinter()

        report = engine.inspect(
            project_path
        )

        if args.duplicates_only:
            report.dependencies = [
                dependency
                for dependencies
                in report.duplicates.values()
                for dependency
                in dependencies
            ]

        printer.print_report(
            report,
            as_json=args.json,
        )

        return 0
