"""
Git Report Command
"""

from aidk.core.command import Command

from aidk.commands.git_report import GitReport


class GitReportCommand(Command):

    @property
    def name(self):

        return "git-report"

    @property
    def help(self):

        return "Generate git report"

    def run(self, args):

        GitReport().run()

        return 0
