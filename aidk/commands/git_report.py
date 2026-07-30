"""Git report CLI adapter."""

from __future__ import annotations

from aidk.app import app
from aidk.git.report.model import (
    GitReport as LegacyGitReport,
    GitRiskItem,
)
from aidk.git.report.printer import GitReportPrinter


class GitReport:
    """Render the structured workspace Git report."""

    @staticmethod
    def _to_legacy_report(
        report,
    ) -> LegacyGitReport:
        return LegacyGitReport(
            total_projects=report.total_projects,
            clean_repositories=(
                report.clean_repositories
            ),
            dirty_repositories=(
                report.dirty_repositories
            ),
            branches=dict(report.branches),
            remote_count=report.remote_count,
            no_remote_count=report.no_remote_count,
            risks=[
                GitRiskItem(
                    project=item.project,
                    level=item.level,
                    reasons=list(item.reasons),
                )
                for item in report.risks
            ],
        )

    def run(self) -> int:
        report = app.services.git_report.run()

        GitReportPrinter().show(
            self._to_legacy_report(report)
        )

        return 0
