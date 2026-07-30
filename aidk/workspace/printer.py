"""
Workspace Printer
"""


class WorkspacePrinter:


    @staticmethod
    def yes(value):

        return "Yes" if value else "No"



    def show_knowledge(self, project):

        print()

        print("    Knowledge Intelligence")

        print("    ------------------------------")


        score = getattr(
            project,
            "documentation_score",
            0
        )


        print(
            f"    Documentation Score : {score}/100"
        )


        knowledge = getattr(
            project,
            "knowledge",
            None
        )


        if knowledge:

            missing = getattr(
                knowledge,
                "missing",
                []
            )


            if missing:

                print()

                print("    Missing")

                for item in missing:

                    print(
                        f"    ⚠ {item}"
                    )


            else:

                print()

                print(
                    "    ✓ Documentation complete"
                )

    def show_deployment(self, project):

        print()

        print("    Deployment Intelligence")

        print("    ------------------------------")


        deployment = getattr(
            project,
            "deployment",
            None
        )


        if not deployment:

            print(
                "    Deployment data unavailable"
            )

            return


        print(
            f"    Deployment Score : {deployment.score}/100"
        )


        if deployment.strengths:

            print()

            print("    Strengths")

            for item in deployment.strengths:

                print(
                    f"    ✓ {item}"
                )


        if deployment.warnings:

            print()

            print("    Warnings")

            for item in deployment.warnings:

                print(
                    f"    ⚠ {item}"
                )


    def show_security(self, project):

        print()

        print("    Security Intelligence")

        print("    ------------------------------")


        security = getattr(
            project,
            "security",
            None
        )


        if not security:

            print(
                "    Security data unavailable"
            )

            return


        print(
            f"    Security Score : {security.score}/100"
        )


        if security.strengths:

            print()

            print("    Strengths")

            for item in security.strengths:

                print(
                    f"    ✓ {item}"
                )


        if security.warnings:

            print()

            print("    Warnings")

            for item in security.warnings:

                print(
                    f"    ⚠ {item}"
                )

    def show_intelligence(self, project):

        print()

        print("    Engineering Intelligence")

        print("    ------------------------------")

        print(
            f"    Score     : {project.intelligence_score}/100"
        )

        print(
            f"    Grade     : {project.grade}"
        )


        if project.strengths:

            print()

            print("    Strengths")

            for item in project.strengths:

                print(
                    f"    ✓ {item}"
                )


        if project.weaknesses:

            print()

            print("    Weaknesses")

            for item in project.weaknesses:

                print(
                    f"    ⚠ {item}"
                )


        if project.recommendations:

            print()

            print("    Recommendations")

            for item in project.recommendations:

                print(
                    f"    → {item}"
                )



    def show(self, projects):

        print()

        print("=" * 70)

        print("Workspace")

        print("=" * 70)

        print()

        print(
            f"Projects : {len(projects)}"
        )

        print()



        for project in projects:

            print(
                f"✓ {project.name}"
            )

            print()


            print(
                f"    Language  : {project.language}"
            )


            print(
                f"    Git       : {self.yes(project.git)}"
            )



            if project.git_info.exists:

                print()

                print("    Git Details")

                print("    ------------------------------")


                print(
                    f"    Branch    : {project.git_info.branch}"
                )


                print(
                    f"    Clean     : {project.git_info.clean}"
                )


                if project.git_info.remote:

                    print(
                        f"    Remote    : {project.git_info.remote_name}"
                    )

                    print(
                        f"    URL       : {project.git_info.remote_url}"
                    )


                print(
                    f"    Commit    : {project.git_info.last_commit_hash}"
                )


                print(
                    f"    Author    : {project.git_info.last_commit_author}"
                )


                print(
                    f"    Date      : {project.git_info.last_commit_date}"
                )



            print(
                f"    Docker    : {self.yes(project.docker)}"
            )


            print(
                f"    Continue  : {self.yes(project.continue_config)}"
            )


            print(
                f"    Readme    : {self.yes(project.readme)}"
            )


            print(
                f"    License   : {self.yes(project.license)}"
            )


            print(
                f"    Tests     : {self.yes(project.tests)}"
            )


            print(
                f"    Engineering Score  : {project.intelligence_score}/100"
            )


            self.show_knowledge(project)

            self.show_security(project)

            self.show_deployment(project)

            self.show_intelligence(project)



            print()

            print("-" * 60)

            print()
