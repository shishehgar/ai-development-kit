"""
Git Command
"""

from aidk.core.command import Command

from aidk.git.command import GitCommand


class GitCLICommand(Command):

    @property
    def name(self):

        return "git"

    @property
    def help(self):

        return "Inspect git repository"

    def run(self, args):

        return GitCommand().run()
