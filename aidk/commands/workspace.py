"""
Workspace Command
"""

from aidk.workspace.scanner import WorkspaceScanner
from aidk.workspace.analyzer import WorkspaceAnalyzer
from aidk.workspace.printer import WorkspacePrinter


class Workspace:

    def run(self):

        projects = WorkspaceScanner().scan()

        projects = WorkspaceAnalyzer().analyze(projects)

        WorkspacePrinter().show(projects)

        return 0
