"""
Auto Improvement Engine
"""

from aidk.improvement.model import (
    ImprovementPlan,
    ImprovementItem,
)



class ImprovementEngine:


    def generate(self, project):


        plan = ImprovementPlan()


        plan.project = project.name


        plan.current_score = (
            project.maturity.score
        )



        priority = 1



        if not project.continue_config:

            plan.items.append(

                ImprovementItem(

                    priority=priority,

                    problem="AI development configuration missing",

                    action=(
                        "Create Continue/Copilot AI configuration"
                    )

                )

            )

            priority += 1



        if not project.license:

            plan.items.append(

                ImprovementItem(

                    priority=priority,

                    problem="License missing",

                    action=(
                        "Create LICENSE file"
                    )

                )

            )

            priority += 1



        if not project.readme:

            plan.items.append(

                ImprovementItem(

                    priority=priority,

                    problem="Documentation missing",

                    action=(
                        "Create README documentation"
                    )

                )

            )

            priority += 1



        if not project.tests:

            plan.items.append(

                ImprovementItem(

                    priority=priority,

                    problem="Automated tests missing",

                    action=(
                        "Add unit and integration tests"
                    )

                )

            )

            priority += 1



        if not project.docker:

            plan.items.append(

                ImprovementItem(

                    priority=priority,

                    problem="Containerization missing",

                    action=(
                        "Add Dockerfile and compose configuration"
                    )

                )

            )



        return plan
