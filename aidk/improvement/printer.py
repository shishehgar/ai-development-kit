"""
Improvement Printer
"""


class ImprovementPrinter:


    def show(self, plan):


        print()

        print("=" * 70)

        print(
            f"Improvement Plan: {plan.project}"
        )

        print("=" * 70)


        print()

        print(
            f"Current Maturity : {plan.current_score}/100"
        )


        print()

        print("Actions")

        print("-" * 30)



        if not plan.items:

            print(
                "✓ No improvement required"
            )

            return



        for item in plan.items:


            print()

            print(
                f"Priority {item.priority}"
            )


            print(
                f"⚠ {item.problem}"
            )


            print(
                f"→ {item.action}"
            )
