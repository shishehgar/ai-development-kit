"""
Lockfile report printer.
"""

from __future__ import annotations

import json
from dataclasses import asdict

from aidk.dependency.lockfiles import (
    LockfileReport,
)


class LockfilePrinter:

    def print_report(
        self,
        report: LockfileReport,
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
            f"Managers: "
            f"{', '.join(report.package_managers) or '-'}"
        )
        print(
            f"Manifests: "
            f"{len(report.manifests)}"
        )
        print(
            f"Lockfiles: "
            f"{len(report.lockfiles)}"
        )
        print(
            f"Lock score: {report.score}/100"
        )
        print(
            "Status: "
            f"{'PASS' if report.healthy else 'FAIL'}"
        )

        if report.manifests:
            print("")
            print("Manifests")

            for filename in report.manifests:
                print(f"- {filename}")

        if report.lockfiles:
            print("")
            print("Lockfiles")

            for filename in report.lockfiles:
                print(f"- {filename}")

        if report.issues:
            print("")
            print("Issues")

            for issue in report.issues:
                location = issue.file or "-"

                print(
                    f"- [{issue.severity.upper()}] "
                    f"{issue.message} "
                    f"[{issue.issue_type}] "
                    f"({location})"
                )
        else:
            print("")
            print("No lockfile issues found.")

    @staticmethod
    def _print_json(
        report: LockfileReport,
    ) -> None:
        data = asdict(report)

        data["project_path"] = str(
            report.project_path
        )

        data["score"] = report.score
        data["healthy"] = report.healthy

        print(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
            )
        )
