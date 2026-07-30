"""
Auto Fix Engine
"""

from pathlib import Path

from aidk.autofix.model import (
    FixPlan,
    FixTask,
)


class AutoFixEngine:


    def generate(self, project):

        plan = FixPlan(
            project=project.name
        )


        if not project.license:

            plan.tasks.append(

                FixTask(

                    title="LICENSE",

                    path="LICENSE",

                    content="MIT License\n"

                )

            )


        if not project.readme:

            plan.tasks.append(

                FixTask(

                    title="README",

                    path="README.md",

                    content="# " + project.name + "\n"

                )

            )


        if not project.continue_config:

            plan.tasks.append(

                FixTask(

                    title="Continue",

                    path=".continue/config.yaml",

                    content="# Continue Configuration\n"

                )

            )


        if not project.tests:

            plan.tasks.append(

                FixTask(

                    title="Tests",

                    path="tests/test_basic.py",

                    content=(
                        "def test_placeholder():\n"
                        "    assert True\n"
                    )

                )

            )


        if not project.docker:

            plan.tasks.append(

                FixTask(

                    title="Docker",

                    path="Dockerfile",

                    content=(
                        "FROM python:3.12-slim\n"
                    )

                )

            )


        return plan


    def apply(self, project, plan):

        root = Path(project.path)


        for task in plan.tasks:

            file = root / task.path

            file.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            if file.exists():

                continue

            file.write_text(
                task.content,
                encoding="utf-8"
            )

