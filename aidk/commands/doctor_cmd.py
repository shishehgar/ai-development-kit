"""
Doctor CLI Command
"""

from aidk.core.command import Command

from aidk.commands.doctor import Doctor


class DoctorCommand(Command):

    @property
    def name(self):
        return "doctor"

    @property
    def help(self):
        return "Check installation"

    def run(self, args):

        Doctor().run()

        return 0
