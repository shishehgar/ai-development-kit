"""
Workspace Scanner.
"""

from __future__ import annotations

from pathlib import Path

from aidk.workspace.project import Project


class WorkspaceScanner:

    DEFAULT_ROOT = Path(
        "/home/ubuntu/my_services/projects"
    )

    SKIPPED_DIRECTORIES = {
        ".git",
        ".idea",
        ".vscode",
        ".venv",
        "venv",
        "env",
        "__pycache__",
        "node_modules",
    }

    def __init__(
        self,
        root: Path | str | None = None,
    ):
        self.root = Path(
            root or self.DEFAULT_ROOT
        ).expanduser().resolve()

    def scan(self):
        projects = []

        if not self.root.exists():
            return projects

        if not self.root.is_dir():
            return projects

        for item in sorted(
            self.root.iterdir(),
            key=lambda path: path.name.lower(),
        ):
            if not item.is_dir():
                continue

            if item.name in self.SKIPPED_DIRECTORIES:
                continue

            if item.name.startswith("."):
                continue

            projects.append(
                Project(
                    name=item.name,
                    path=item.resolve(),
                )
            )

        return projects
