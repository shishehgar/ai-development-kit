"""
Dependency health report printer.
"""

from __future__ import annotations

import json
from dataclasses import asdict

from aidk.dependency.health import (
    DependencyHealthReport,
)


class DependencyHealthPrinter:

    def print_report(
        self,
        report: DependencyHealthReport,
        as_json: bool = False,
    ) -> None:
        if as_json:
            self._print_json(report)
            return

        print(
            f"Project: {report.project_name}"
        )
        print(
            f"Dependencies: "
            f"{report.dependency_total}"
        )
        print(f"Health score: {report.score}/100")
        print(
            f"Critical: {report.critical_total}"
        )
        print(f"High: {report.high_total}")
        print(f"Medium: {report.medium_total}")
        print(f"Low: {report.low_total}")
        print(
            "Status: "
            f"{'PASS' if report.healthy else 'FAIL'}"
        )

        if not report.issues:
            print("")
            print("No dependency issues found.")
            return

        print("")
        print("Issues")

        for issue in report.issues:
            location = issue.source or "-"
            print(
                f"- [{issue.severity.value.upper()}] "
                f"{issue.dependency}: "
                f"{issue.message} "
                f"[{issue.issue_type}] "
                f"({location})"
            )

    @staticmethod
    def _print_json(
        report: DependencyHealthReport,
    ) -> None:
        data = asdict(report)

        data["healthy"] = report.healthy
        data["critical_total"] = (
            report.critical_total
        )
        data["high_total"] = report.high_total
        data["medium_total"] = (
            report.medium_total
        )
        data["low_total"] = report.low_total

        print(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
            )
        )
