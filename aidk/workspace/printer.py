"""
Workspace Printer
"""


class WorkspacePrinter:


    @staticmethod
    def yes(value):

        return "Yes" if value else "No"


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


            self.show_intelligence(project)


            print()

            print("-" * 60)

            print()
