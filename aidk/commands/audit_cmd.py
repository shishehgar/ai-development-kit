"""
Audit Command
"""

from aidk.core.command import Command

from aidk.audit.command import AuditCommand


class AuditCLICommand(Command):

    @property
    def name(self):

        return "audit"

    @property
    def help(self):

        return "Engineering audit"

    def run(self, args):

        return AuditCommand().run()
