"""Audit CLI adapter."""

from __future__ import annotations

from aidk.app import app
from aidk.audit.printer import AuditPrinter


class AuditCommand:
    """Run engineering audit."""

    def run(self) -> int:
        report = app.services.audit.run()

        AuditPrinter().show(
            report
        )

        return 0
