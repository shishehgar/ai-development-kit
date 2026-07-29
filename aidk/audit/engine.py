"""
Audit Engine
"""

from aidk.audit.model import AuditReport


class AuditEngine:


    def generate(self, projects):

        report = AuditReport()

        report.total_projects = len(projects)


        total_score = 0


        for project in projects:


            score = getattr(
                project,
                "intelligence_score",
                0
            )

            total_score += score


            grade = getattr(
                project,
                "grade",
                "N/A"
            )


            if grade not in report.grade_distribution:

                report.grade_distribution[grade] = 0


            report.grade_distribution[grade] += 1



            if not project.readme:

                report.missing_readme += 1


            if not project.tests:

                report.missing_tests += 1


            if not project.continue_config:

                report.missing_ai_config += 1


            if not project.license:

                report.missing_license += 1


            if not project.docker:

                report.missing_docker += 1



            if score < 40:

                report.critical_projects.append(
                    project.name
                )


        if report.total_projects:

            report.average_score = round(
                total_score / report.total_projects,
                1
            )


        self.generate_recommendations(
            report
        )


        return report



    def generate_recommendations(self, report):


        if report.missing_readme:

            report.recommendations.append(
                "Create README documentation"
            )


        if report.missing_tests:

            report.recommendations.append(
                "Add automated tests"
            )


        if report.missing_ai_config:

            report.recommendations.append(
                "Add AI coding configuration"
            )


        if report.missing_license:

            report.recommendations.append(
                "Add project license"
            )


        if report.missing_docker:

            report.recommendations.append(
                "Add containerization support"
            )
