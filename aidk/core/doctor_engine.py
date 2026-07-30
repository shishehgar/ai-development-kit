"""CLI renderer for the structured AIDK Doctor service."""

from __future__ import annotations

from aidk.application.container import services
from aidk.application.doctor_service import (
    DoctorCheck,
    DoctorReport,
)


class DoctorEngine:
    """Preserve the legacy CLI output using DoctorService."""

    @staticmethod
    def _render_check(
        check: DoctorCheck,
    ) -> None:
        if check.status == "passed":
            marker = "[ OK ]"
        elif check.status == "warning":
            marker = "[WARN]"
        else:
            marker = "[FAIL]"

        detail = (
            check.version
            or check.path
            or check.message
            or ""
        )

        print(
            f"{marker} "
            f"{check.title:<20} "
            f"{detail}"
        )

    @staticmethod
    def _render_header() -> None:
        print()
        print("=" * 70)
        print("AI Development Kit Doctor")
        print("=" * 70)

    @staticmethod
    def _render_python(
        report: DoctorReport,
    ) -> None:
        print()
        print("Python")
        print("-" * 70)
        print(report.python_version)

    @staticmethod
    def _render_footer(
        report: DoctorReport,
    ) -> None:
        print()
        print("-" * 70)
        print(
            f"Health Score : "
            f"{report.health_score}%"
        )
        print(f"Passed       : {report.passed}")
        print(f"Failed       : {report.failed}")
        print(f"Warnings     : {report.warnings}")
        print(f"Status       : {report.status}")
        print("-" * 70)

    def run(self) -> DoctorReport:
        report = services.doctor.run()

        self._render_header()
        self._render_python(report)

        print()
        print("Environment Checks")
        print("-" * 70)

        for check in report.checks:
            self._render_check(check)

        self._render_footer(report)

        return report
