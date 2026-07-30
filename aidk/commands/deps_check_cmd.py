"""
Dependency health check command.
"""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path

from aidk.core.command import Command
from aidk.dependency.engine import DependencyEngine
from aidk.dependency.health import (
    DependencyHealthAnalyzer,
)
from aidk.dependency.health_printer import (
    DependencyHealthPrinter,
)


class DependenciesCheckCommand(Command):

    @property
    def name(self):
        return "deps-check"

    @property
    def help(self):
        return "Check dependency health and reproducibility"

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
            "--fail-score",
            type=int,
            default=70,
        )

        parser.add_argument(
            "--strict",
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

        dependency_report = (
            DependencyEngine().inspect(
                project_path
            )
        )

        health_report = (
            DependencyHealthAnalyzer().analyze(
                dependency_report
            )
        )

        DependencyHealthPrinter().print_report(
            health_report,
            as_json=args.json,
        )

        if args.strict and health_report.issues:
            return 1

        if health_report.score < args.fail_score:
            return 1

        if (
            health_report.critical_total > 0
            or health_report.high_total > 0
        ):
            return 1

        return 0
