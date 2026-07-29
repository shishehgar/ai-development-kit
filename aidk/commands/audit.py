"""
Audit Command
"""

from aidk.workspace.scanner import WorkspaceScanner
from aidk.workspace.analyzer import WorkspaceAnalyzer

from aidk.audit.engine import AuditEngine
from aidk.audit.printer import AuditPrinter


class Audit:


    def run(self):

        scanner = WorkspaceScanner()

        projects = scanner.scan()

        analyzer = WorkspaceAnalyzer()

        projects = analyzer.analyze(
            projects
        )


        for project in projects:

            print(
                project.name,
                project.intelligence_score
            )


        report = AuditEngine().generate(
            projects
        )


        AuditPrinter().show(
            report
        )

        return 0
