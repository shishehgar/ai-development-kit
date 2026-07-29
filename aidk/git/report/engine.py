"""
Git Report Engine
"""

from aidk.git.engine import GitEngine

from aidk.git.report.model import (
    GitReport,
    GitRiskItem,
)


class GitReportEngine:


    def __init__(self):

        self.git = GitEngine()


    def generate(self, projects):

        report = GitReport()

        report.total_projects = len(projects)


        for project in projects:

            info = self.git.inspect(
                project.path
            )


            if info.clean:

                report.clean_repositories += 1

            else:

                report.dirty_repositories += 1

                reasons = [
                    "Uncommitted changes"
                ]

                level = "MEDIUM"


                if not info.remote:

                    reasons.append(
                        "No remote repository"
                    )

                    level = "HIGH"


                report.risks.append(

                    GitRiskItem(

                        project=project.name,

                        level=level,

                        reasons=reasons,

                    )

                )


            branch = info.branch or "unknown"


            if branch not in report.branches:

                report.branches[branch] = 0


            report.branches[branch] += 1


            if info.remote:

                report.remote_count += 1

            else:

                report.no_remote_count += 1


        return report
