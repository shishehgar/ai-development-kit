"""
Knowledge Printer
"""


class KnowledgePrinter:

    def show(self, knowledge):

        print()

        print("Knowledge")

        print("-" * 30)

        print(f"Score : {knowledge.score}")

        print()

        if knowledge.missing:

            print("Missing")

            for item in knowledge.missing:

                print(f"  - {item}")

        else:

            print("Complete")
