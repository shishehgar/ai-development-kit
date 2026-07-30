"""
Dependency license command.
"""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path

from aidk.core.command import Command
from aidk.dependency.license_printer import (
    LicensePrinter,
)
from aidk.dependency.licenses import (
    LicenseAnalyzer,
    LicensePolicy,
)


class DependenciesLicensesCommand(Command):

    @property
    def name(self):
        return "deps-licenses"

    @property
    def help(self):
        return "Check dependency licenses"

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
            "--allow-unknown",
            action="store_true",
        )

        parser.add_argument(
            "--deny-category",
            action="append",
            default=None,
        )

        parser.add_argument(
            "--deny-license",
            action="append",
            default=None,
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

        denied_categories = (
            set(args.deny_category)
            if args.deny_category
            else None
        )

        denied_licenses = set(
            args.deny_license or []
        )

        policy = LicensePolicy(
            denied_categories=denied_categories,
            denied_licenses=denied_licenses,
            allow_unknown=args.allow_unknown,
        )

        report = LicenseAnalyzer(
            policy
        ).analyze(
            project_path
        )

        LicensePrinter().print_report(
            report,
            as_json=args.json,
        )

        return 0 if report.compliant else 1
