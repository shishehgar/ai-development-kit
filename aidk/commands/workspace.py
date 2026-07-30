"""Workspace CLI adapter."""

from __future__ import annotations

from aidk.application.container import services


class Workspace:
    """Render structured workspace results for the CLI."""

    @staticmethod
    def _show_project(
        project,
    ) -> None:
        print()
        print("-" * 70)
        print(f"Project       : {project.name}")
        print(f"Path          : {project.path}")
        print(f"Language      : {project.language}")
        print(f"Grade         : {project.grade}")
        print(
            f"Intelligence  : "
            f"{project.intelligence_score}"
        )
        print(
            f"Documentation : "
            f"{project.documentation_score}"
        )
        print(f"Git           : {project.git}")
        print(f"Docker        : {project.docker}")
        print(f"README        : {project.readme}")
        print(f"License       : {project.license}")
        print(f"Tests         : {project.tests}")

    def run(self) -> int:
        report = services.workspace.run()

        print()
        print("=" * 70)
        print("AI Development Kit Workspace")
        print("=" * 70)
        print(f"Root     : {report.root}")
        print(
            f"Projects : "
            f"{report.project_count}"
        )

        for project in report.projects:
            self._show_project(project)

        print()
        print("=" * 70)

        return 0
