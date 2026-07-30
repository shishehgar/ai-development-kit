"""
Deployment Intelligence Engine
"""

from pathlib import Path

from aidk.deployment.models import DeploymentReport



class DeploymentEngine:


    def inspect(self, project: Path):

        report = DeploymentReport()


        score = 0



        # Dockerfile

        if (project / "Dockerfile").exists():

            report.docker = True

            score += 25

            report.strengths.append(
                "Dockerfile available"
            )

        else:

            report.warnings.append(
                "Dockerfile missing"
            )



        # Docker compose

        compose_files = [

            "docker-compose.yml",

            "docker-compose.yaml",

            "compose.yml",

            "compose.yaml",

        ]


        if any(
            (project / x).exists()
            for x in compose_files
        ):

            report.compose = True

            score += 25

            report.strengths.append(
                "Docker Compose available"
            )

        else:

            report.warnings.append(
                "Docker Compose missing"
            )



        # CI/CD

        github_actions = (
            project
            /
            ".github"
            /
            "workflows"
        )


        if github_actions.exists():

            report.ci_cd = True

            score += 25

            report.strengths.append(
                "CI/CD workflow detected"
            )

        else:

            report.warnings.append(
                "CI/CD configuration missing"
            )



        # Kubernetes

        k8s = [

            "k8s",

            "kubernetes",

            "helm",

        ]


        if any(
            (project / x).exists()
            for x in k8s
        ):

            report.kubernetes = True

            score += 15

            report.strengths.append(
                "Kubernetes configuration available"
            )

        else:

            report.warnings.append(
                "Kubernetes configuration missing"
            )



        # Cloud

        cloud_files = [

            "terraform",

            "serverless.yml",

            "cloudformation.yml",

        ]


        if any(
            (project / x).exists()
            for x in cloud_files
        ):

            report.cloud_ready = True

            score += 10

            report.strengths.append(
                "Cloud deployment configuration detected"
            )

        else:

            report.warnings.append(
                "Cloud deployment configuration missing"
            )



        report.score = score


        return report
