"""
Workspace Scanner
"""

from pathlib import Path

from aidk.workspace.project import Project


class WorkspaceScanner:

    ROOT = Path("/home/ubuntu/my_services/projects")

    def scan(self):

        projects = []

        if not self.ROOT.exists():

            return projects

        for item in sorted(self.ROOT.iterdir()):

            if not item.is_dir():

                continue

            projects.append(

                Project(

                    name=item.name,

                    path=item,

                )

            )

        return projects
