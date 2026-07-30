"""
Improve Command
"""

from aidk.core.command import Command

from aidk.workspace.scanner import WorkspaceScanner
from aidk.workspace.analyzer import WorkspaceAnalyzer

from aidk.improvement.engine import ImprovementEngine
from aidk.improvement.printer import ImprovementPrinter


class ImproveCommand(Command):

    @property
    def name(self):
        return "improve"

    @property
    def help(self):
        return "Generate improvement plan"

    def run(self, args):

        projects = WorkspaceScanner().scan()
        projects = WorkspaceAnalyzer().analyze(projects)

        engine = ImprovementEngine()

        for project in projects:

            plan = engine.generate(project)

            ImprovementPrinter().show(plan)

        return 0
