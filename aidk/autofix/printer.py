"""
Auto Fix Printer
"""


class AutoFixPrinter:


    def show(self, plan):

        print()

        print("=" * 70)

        print(
            f"Auto Fix : {plan.project}"
        )

        print("=" * 70)

        print()


        if not plan.tasks:

            print(
                "Nothing to generate."
            )

            return


        for task in plan.tasks:

            print(
                f"✓ {task.path}"
            )

        print()
