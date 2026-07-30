"""
Register all commands
"""

from aidk.core.registry import CommandRegistry

from aidk.commands.version import VersionCommand
from aidk.commands.doctor_cmd import DoctorCommand
from aidk.commands.workspace_cmd import WorkspaceCommand
from aidk.commands.git_cmd import GitCLICommand
from aidk.commands.git_report_cmd import GitReportCommand
from aidk.commands.audit_cmd import AuditCLICommand
from aidk.commands.dashboard_cmd import DashboardCommand
from aidk.commands.improve_cmd import ImproveCommand
from aidk.commands.fix_cmd import FixCommand


def build_registry():

    registry = CommandRegistry()

    registry.register(VersionCommand())
    registry.register(DoctorCommand())
    registry.register(WorkspaceCommand())
    registry.register(GitCLICommand())
    registry.register(GitReportCommand())
    registry.register(AuditCLICommand())
    registry.register(DashboardCommand())
    registry.register(ImproveCommand())
    registry.register(FixCommand())

    return registry

