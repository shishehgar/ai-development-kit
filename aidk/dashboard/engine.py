"""
Workspace Dashboard Engine
"""


from aidk.dashboard.model import WorkspaceDashboard



class DashboardEngine:


    def generate(self, projects):


        report = WorkspaceDashboard()


        report.projects = len(projects)


        total = 0


        for project in projects:


            score = getattr(
                project.maturity,
                "score",
                0
            )


            total += score


            level = getattr(
                project.maturity,
                "level",
                "Unknown"
            )


            if level not in report.levels:

                report.levels[level] = 0


            report.levels[level] += 1



            report.ranking.append(

                (
                    project.name,
                    score
                )

            )



            if score < 50:

                report.critical_projects.append(
                    project.name
                )



        if report.projects:

            report.average_score = round(
                total / report.projects
            )



        report.ranking.sort(
            key=lambda x: x[1],
            reverse=True
        )


        return report
