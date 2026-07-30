"""
Dashboard Command
"""

from aidk.core.command import Command

from aidk.workspace.scanner import WorkspaceScanner
from aidk.workspace.analyzer import WorkspaceAnalyzer

from aidk.dashboard.engine import DashboardEngine
from aidk.dashboard.printer import DashboardPrinter


class DashboardCommand(Command):

    @property
    def name(self):
        return "dashboard"

    @property
    def help(self):
        return "Show workspace dashboard"

    def run(self, args):

        projects = WorkspaceScanner().scan()
        projects = WorkspaceAnalyzer().analyze(projects)

        report = DashboardEngine().generate(projects)

        DashboardPrinter().show(report)

        return 0
