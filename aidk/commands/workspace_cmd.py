"""
Workspace Command
"""

from aidk.core.command import Command

from aidk.commands.workspace import Workspace


class WorkspaceCommand(Command):

    @property
    def name(self):

        return "workspace"

    @property
    def help(self):

        return "Analyze workspace"

    def run(self, args):

        Workspace().run()

        return 0
