"""
Auto Fix Command
"""

from aidk.core.command import Command

from aidk.workspace.scanner import WorkspaceScanner
from aidk.workspace.analyzer import WorkspaceAnalyzer

from aidk.autofix.engine import AutoFixEngine
from aidk.autofix.printer import AutoFixPrinter


class FixCommand(Command):

    @property
    def name(self):
        return "fix"

    @property
    def help(self):
        return "Generate project fixes"

    def configure(self, parser):

        parser.add_argument(
            "project"
        )

        return parser

    def run(self, args):

        projects = WorkspaceScanner().scan()

        projects = WorkspaceAnalyzer().analyze(projects)

        target = None

        for project in projects:

            if project.name == args.project:

                target = project

                break

        if target is None:

            print("Project not found")

            return 1

        engine = AutoFixEngine()

        plan = engine.generate(target)

        AutoFixPrinter().show(plan)

        engine.apply(target, plan)

        return 0
