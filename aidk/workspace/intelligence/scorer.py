"""
Workspace Intelligence Scorer

Evaluates project engineering maturity.
"""


class IntelligenceScorer:


    def analyze(self, project):

        score = 0

        strengths = []

        weaknesses = []

        recommendations = []


        # Git

        if project.git:

            score += 15

            strengths.append(
                "Git repository available"
            )

        else:

            weaknesses.append(
                "Git repository missing"
            )

            recommendations.append(
                "Initialize Git repository"
            )


        # Docker

        if project.docker:

            score += 15

            strengths.append(
                "Docker configuration available"
            )

        else:

            weaknesses.append(
                "Docker configuration missing"
            )

            recommendations.append(
                "Add Dockerfile and docker-compose configuration"
            )


        # Tests

        if project.tests:

            score += 20

            strengths.append(
                "Automated tests detected"
            )

        else:

            weaknesses.append(
                "No automated tests detected"
            )

            recommendations.append(
                "Add unit and integration tests"
            )


        # Documentation

        if project.readme:

            score += 15

            strengths.append(
                "README documentation available"
            )

        else:

            weaknesses.append(
                "README documentation missing"
            )

            recommendations.append(
                "Create project documentation"
            )


        # License

        if project.license:

            score += 10

            strengths.append(
                "License file available"
            )

        else:

            weaknesses.append(
                "License file missing"
            )

            recommendations.append(
                "Add open-source license"
            )


        # AI readiness

        if project.continue_config:

            score += 15

            strengths.append(
                "AI coding configuration detected"
            )

        else:

            weaknesses.append(
                "AI development configuration missing"
            )

            recommendations.append(
                "Add Continue/Copilot AI configuration"
            )


        # Score

        project.intelligence_score = score


        if score >= 85:

            project.grade = "A"


        elif score >= 70:

            project.grade = "B"


        elif score >= 50:

            project.grade = "C"


        else:

            project.grade = "D"


        project.strengths = strengths

        project.weaknesses = weaknesses

        project.recommendations = recommendations


        return project
