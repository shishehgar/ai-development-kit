"""
Workspace Dashboard Printer
"""


class DashboardPrinter:


    def show(self, report):


        print()

        print("=" * 70)

        print(
            "AIDK Workspace Maturity"
        )

        print("=" * 70)


        print()

        print(
            f"Projects : {report.projects}"
        )


        print()

        print(
            f"Average Maturity : {report.average_score}/100"
        )


        print()

        print("Level Distribution")

        print("-" * 30)


        for level, count in report.levels.items():

            print(
                f"{level:<15}: {count}"
            )


        print()

        print("Top Projects")

        print("-" * 30)


        for index, item in enumerate(
            report.ranking[:5],
            start=1
        ):

            print(
                f"{index}. {item[0]:30} {item[1]}"
            )


        print()

        print("Critical Projects")

        print("-" * 30)


        for project in report.critical_projects:

            print(
                f"⚠ {project}"
            )


        print()
