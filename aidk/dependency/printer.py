"""
Dependency report printer.
"""

from __future__ import annotations

import json
from dataclasses import asdict

from aidk.dependency.models import (
    DependencyReport,
)


class DependencyPrinter:

    def print_report(
        self,
        report: DependencyReport,
        as_json: bool = False,
    ) -> None:
        if as_json:
            self._print_json(report)
            return

        print(
            f"Project: {report.project_name}"
        )
        print(
            f"Path: {report.project_path}"
        )
        print(
            f"Dependency files: {len(report.files)}"
        )
        print(
            f"Dependencies: {report.total}"
        )
        print(
            f"Unique dependencies: "
            f"{report.unique_total}"
        )
        print(
            f"Runtime: {report.runtime_total}"
        )
        print(
            f"Development: "
            f"{report.development_total}"
        )
        print(
            f"Optional: {report.optional_total}"
        )
        print(
            f"Duplicates: "
            f"{len(report.duplicates)}"
        )

        if report.files:
            print("")
            print("Files")

            for file_path in report.files:
                print(
                    f"- {file_path.name}"
                )

        if report.dependencies:
            print("")
            print("Dependencies")

            name_width = max(
                len("NAME"),
                max(
                    len(dependency.name)
                    for dependency
                    in report.dependencies
                ),
            )

            group_width = max(
                len("GROUP"),
                max(
                    len(dependency.group)
                    for dependency
                    in report.dependencies
                ),
            )

            print(
                f"{'NAME':<{name_width}}  "
                f"{'GROUP':<{group_width}}  "
                f"{'VERSION':<24}  "
                f"SOURCE"
            )

            print(
                f"{'-' * name_width}  "
                f"{'-' * group_width}  "
                f"{'-' * 24}  "
                f"{'-' * 20}"
            )

            for dependency in report.dependencies:
                version = (
                    dependency.version[:24]
                )

                print(
                    f"{dependency.name:<{name_width}}  "
                    f"{dependency.group:<{group_width}}  "
                    f"{version:<24}  "
                    f"{dependency.source}"
                )

        if report.duplicates:
            print("")
            print("Duplicates")

            for name, dependencies in sorted(
                report.duplicates.items()
            ):
                versions = ", ".join(
                    dependency.version or "*"
                    for dependency
                    in dependencies
                )

                print(
                    f"- {name}: {versions}"
                )

        if report.errors:
            print("")
            print("Errors")

            for error in report.errors:
                print(
                    f"- {error}"
                )

    @staticmethod
    def _print_json(
        report: DependencyReport,
    ) -> None:
        data = asdict(report)

        data["project_path"] = str(
            report.project_path
        )

        data["files"] = [
            str(file_path)
            for file_path in report.files
        ]

        data["duplicates"] = {
            name: [
                asdict(dependency)
                for dependency
                in dependencies
            ]
            for name, dependencies
            in report.duplicates.items()
        }

        print(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
            )
        )
