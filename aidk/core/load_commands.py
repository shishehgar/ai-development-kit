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
from aidk.commands.scan_cmd import ScanCommand
from aidk.commands.db_cmd import DatabaseCommand
from aidk.commands.deps_cmd import DependenciesCommand
from aidk.commands.deps_db_cmd import DependenciesDatabaseCommand
from aidk.commands.deps_check_cmd import DependenciesCheckCommand
from aidk.commands.deps_lock_cmd import DependenciesLockCommand
from aidk.commands.deps_licenses_cmd import DependenciesLicensesCommand


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
    registry.register(ScanCommand())
    registry.register(DatabaseCommand())
    registry.register(DependenciesCommand())
    registry.register(DependenciesDatabaseCommand())
    registry.register(DependenciesCheckCommand())
    registry.register(DependenciesLockCommand())
    registry.register(DependenciesLicensesCommand())

    return registry

