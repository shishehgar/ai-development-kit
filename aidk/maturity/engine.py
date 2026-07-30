"""
Maturity Engine
"""

from aidk.maturity.model import MaturityReport



class MaturityEngine:


    def calculate(self, project):


        engineering = getattr(
            project,
            "intelligence_score",
            0
        )


        knowledge_score = 0


        security_score = 0


        deployment_score = 0



        knowledge = getattr(
            project,
            "knowledge",
            None
        )


        if knowledge:

            knowledge_score = getattr(
                knowledge,
                "score",
                0
            )



        security = getattr(
            project,
            "security",
            None
        )


        if security:

            security_score = getattr(
                security,
                "score",
                0
            )



        deployment = getattr(
            project,
            "deployment",
            None
        )


        if deployment:

            deployment_score = getattr(
                deployment,
                "score",
                0
            )



        score = (

            engineering * 0.4

            +

            knowledge_score * 0.2

            +

            security_score * 0.2

            +

            deployment_score * 0.2

        )



        report = MaturityReport()


        report.score = round(score)



        if report.score >= 85:

            report.level = "Excellent"


        elif report.score >= 70:

            report.level = "Advanced"


        elif report.score >= 50:

            report.level = "Intermediate"


        else:

            report.level = "Initial"



        return report
