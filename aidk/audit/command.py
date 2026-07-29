"""
Audit Command
"""

from aidk.audit.engine import AuditEngine
from aidk.audit.printer import AuditPrinter
from aidk.workspace.analyzer import WorkspaceAnalyzer
from aidk.workspace.scanner import WorkspaceScanner


class AuditCommand:
    """Run engineering audit."""

    def run(self) -> int:

        scanner = WorkspaceScanner()

        analyzer = WorkspaceAnalyzer()

        projects = scanner.scan()

        projects = analyzer.analyze(projects)

        report = AuditEngine().generate(projects)

        AuditPrinter().show(report)

        return 0
