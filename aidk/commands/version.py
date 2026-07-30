"""
Version command.
"""

from aidk.core.command import Command

from aidk.version import get_version


class VersionCommand(Command):

    @property
    def name(self):

        return "version"

    @property
    def help(self):

        return "Show version"

    def run(self, args):

        print(
            get_version()
        )

        return 0
