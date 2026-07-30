"""
Workspace scan command.
"""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path

from aidk.core.command import Command
from aidk.db.dependency_repository import DependencyRepository
from aidk.db.engine import DatabaseEngine
from aidk.db.repository import WorkspaceRepository
from aidk.dependency.engine import DependencyEngine
from aidk.workspace.analyzer import WorkspaceAnalyzer
from aidk.workspace.scanner import WorkspaceScanner


class ScanCommand(Command):

    @property
    def name(self):
        return "scan"

    @property
    def help(self):
        return "Scan workspace and persist project data"

    def configure(
        self,
        parser: ArgumentParser,
    ):
        parser.add_argument(
            "path",
            nargs="?",
            default="/home/ubuntu/my_services/projects",
        )

        parser.add_argument(
            "--database",
            type=Path,
            default=None,
        )

        parser.add_argument(
            "--clear",
            action="store_true",
        )

        parser.add_argument(
            "--skip-dependencies",
            action="store_true",
        )

        return parser

    def run(
        self,
        args: Namespace,
    ):
        root = Path(
            args.path
        ).expanduser().resolve()

        if not root.exists():
            print(f"Path not found: {root}")
            return 1

        if not root.is_dir():
            print(f"Not a directory: {root}")
            return 1

        engine = DatabaseEngine(
            args.database
        )

        workspace_repository = WorkspaceRepository(
            engine
        )

        dependency_repository = DependencyRepository(
            engine
        )

        if args.clear:
            workspace_repository.clear()

        scanner = WorkspaceScanner(
            root=root
        )

        analyzer = WorkspaceAnalyzer()
        dependency_engine = DependencyEngine()

        projects = scanner.scan()
        projects = analyzer.analyze(projects)

        dependency_scans = 0

        for project in projects:
            project_id = workspace_repository.save_project(
                project
            )

            if args.skip_dependencies:
                continue

            dependency_report = dependency_engine.inspect(
                project.path
            )

            dependency_repository.save_report(
                project_id,
                dependency_report,
            )

            dependency_scans += 1

        print(f"Scanned projects: {len(projects)}")
        print(f"Saved projects: {len(projects)}")
        print(
            f"Dependency scans: {dependency_scans}"
        )
        print(f"Database: {engine.database_path}")

        return 0
