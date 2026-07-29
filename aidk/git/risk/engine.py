"""
Git Risk Engine
"""

from aidk.git.engine import GitEngine


class GitRiskEngine:


    def __init__(self):

        self.git = GitEngine()


    def analyze(self, projects):

        risks = []


        for project in projects:

            info = self.git.inspect(
                project.path
            )


            reasons = []


            if not info.clean:

                reasons.append(
                    "Uncommitted changes"
                )


            if not info.remote:

                reasons.append(
                    "No remote repository"
                )


            if not info.branch:

                reasons.append(
                    "Unknown branch"
                )


            if reasons:

                level = "MEDIUM"


                if (
                    "No remote repository"
                    in reasons
                    and
                    "Uncommitted changes"
                    in reasons
                ):
                    level = "HIGH"


                risks.append(

                    {
                        "project": project.name,
                        "level": level,
                        "reasons": reasons,
                    }

                )


        return risks
