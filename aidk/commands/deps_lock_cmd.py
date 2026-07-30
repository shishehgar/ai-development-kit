"""
Dependency lockfile command.
"""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path

from aidk.core.command import Command
from aidk.dependency.lockfile_printer import (
    LockfilePrinter,
)
from aidk.dependency.lockfiles import (
    LockfileAnalyzer,
)


class DependenciesLockCommand(Command):

    @property
    def name(self):
        return "deps-lock"

    @property
    def help(self):
        return "Check dependency lockfiles"

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

        report = LockfileAnalyzer().analyze(
            project_path
        )

        LockfilePrinter().print_report(
            report,
            as_json=args.json,
        )

        if (
            args.strict
            and report.issues
        ):
            return 1

        if report.score < args.fail_score:
            return 1

        if not report.healthy:
            return 1

        return 0
