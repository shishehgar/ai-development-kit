"""
Audit Printer
"""


class AuditPrinter:


    def show(self, report):

        print()

        print("=" * 70)

        print("AIDK Engineering Audit")

        print("=" * 70)


        print()

        print(
            f"Projects : {report.total_projects}"
        )

        print(
            f"Average Score : {report.average_score}"
        )


        print()

        print("Grade Distribution")

        print("-" * 30)


        for grade, count in report.grade_distribution.items():

            print(
                f"{grade:<5}: {count}"
            )


        print()

        print("Missing Components")

        print("-" * 30)

        print(
            f"README       : {report.missing_readme}"
        )

        print(
            f"Tests        : {report.missing_tests}"
        )

        print(
            f"AI Config    : {report.missing_ai_config}"
        )

        print(
            f"License      : {report.missing_license}"
        )

        print(
            f"Docker       : {report.missing_docker}"
        )


        print()

        print("Critical Projects")

        print("-" * 30)


        for item in report.critical_projects:

            print(
                f"⚠ {item}"
            )


        print()

        print("Recommendations")

        print("-" * 30)


        for item in report.recommendations:

            print(
                f"→ {item}"
            )

        print()
