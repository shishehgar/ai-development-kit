"""
Git Report Printer
"""


class GitReportPrinter:


    def show(self, report):

        print()

        print("=" * 70)

        print("Git Report")

        print("=" * 70)

        print()


        print(
            f"Projects analyzed : {report.total_projects}"
        )

        print()


        print("Repository Status")

        print("-" * 30)

        print(
            f"Clean repositories : {report.clean_repositories}"
        )

        print(
            f"Dirty repositories : {report.dirty_repositories}"
        )

        print()


        if report.risks:

            print("Risk Analysis")

            print("-" * 30)

            print()


            high = [
                item
                for item in report.risks
                if item.level == "HIGH"
            ]


            medium = [
                item
                for item in report.risks
                if item.level == "MEDIUM"
            ]


            if high:

                print("HIGH")

                print("----")

                for item in high:

                    print(
                        f"⚠ {item.project}"
                    )

                    for reason in item.reasons:

                        print(
                            f"   - {reason}"
                        )

                    print()


            if medium:

                print("MEDIUM")

                print("------")

                for item in medium:

                    print(
                        f"⚠ {item.project}"
                    )

                    for reason in item.reasons:

                        print(
                            f"   - {reason}"
                        )

                    print()


        print("Branches")

        print("-" * 30)

        for name, count in report.branches.items():

            print(
                f"{name:<10}: {count}"
            )


        print()


        print("Remote")

        print("-" * 30)

        print(
            f"With remote : {report.remote_count}"
        )

        print(
            f"No remote   : {report.no_remote_count}"
        )

        print()
