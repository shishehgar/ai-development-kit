"""
Dependency license report printer.
"""

from __future__ import annotations

import json
from dataclasses import asdict

from aidk.dependency.licenses import (
    LicenseReport,
)


class LicensePrinter:

    def print_report(
        self,
        report: LicenseReport,
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
        print(f"Dependencies: {report.total}")
        print(f"Allowed: {report.allowed_total}")
        print(f"Denied: {report.denied_total}")
        print(f"Unknown: {report.unknown_total}")
        print(
            "Status: "
            f"{'PASS' if report.compliant else 'FAIL'}"
        )

        if report.records:
            print("")
            print("Licenses")

            name_width = max(
                len("NAME"),
                max(
                    len(record.name)
                    for record in report.records
                ),
            )

            print(
                f"{'NAME':<{name_width}}  "
                f"{'VERSION':<14}  "
                f"{'LICENSE':<24}  "
                f"{'CATEGORY':<18}  "
                f"STATUS"
            )

            print(
                f"{'-' * name_width}  "
                f"{'-' * 14}  "
                f"{'-' * 24}  "
                f"{'-' * 18}  "
                f"{'-' * 8}"
            )

            for record in report.records:
                version = (
                    record.version[:14]
                    or "-"
                )

                license_name = (
                    record.license[:24]
                    or "UNKNOWN"
                )

                status = (
                    "ALLOW"
                    if record.allowed
                    else "DENY"
                )

                print(
                    f"{record.name:<{name_width}}  "
                    f"{version:<14}  "
                    f"{license_name:<24}  "
                    f"{record.category:<18}  "
                    f"{status}"
                )

        denied = [
            record
            for record in report.records
            if not record.allowed
        ]

        if denied:
            print("")
            print("Policy violations")

            for record in denied:
                print(
                    f"- {record.name}: "
                    f"{record.license} — "
                    f"{record.reason}"
                )

        if report.errors:
            print("")
            print("Errors")

            for error in report.errors:
                print(f"- {error}")

    @staticmethod
    def _print_json(
        report: LicenseReport,
    ) -> None:
        data = asdict(report)

        data["project_path"] = str(
            report.project_path
        )

        data["total"] = report.total
        data["allowed_total"] = (
            report.allowed_total
        )
        data["denied_total"] = (
            report.denied_total
        )
        data["unknown_total"] = (
            report.unknown_total
        )
        data["compliant"] = report.compliant

        print(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
            )
        )
