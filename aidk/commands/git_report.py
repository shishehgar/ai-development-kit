"""
Git Report Command
"""

from aidk.git.report.engine import GitReportEngine
from aidk.git.report.printer import GitReportPrinter
from aidk.workspace.scanner import WorkspaceScanner


class GitReport:

    def run(self):

        scanner = WorkspaceScanner()

        projects = scanner.scan()

        engine = GitReportEngine()

        report = engine.generate(
            projects
        )

        printer = GitReportPrinter()

        printer.show(
            report
        )
