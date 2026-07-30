"""AI engineering assistant service."""

from __future__ import annotations


from studio.backend.services.knowledge_runtime import (
    knowledge_runtime,
)



class AssistantService:
    """
    Knowledge aware engineering assistant.

    Current version:
        Graph based reasoning

    Future:
        RAG + LLM
    """



    def ask(
        self,
        question: str,
    ) -> dict:


        question_lower = (
            question.lower()
        )


        graph = (
            knowledge_runtime.graph
        )


        if "statistics" in question_lower:

            return {

                "answer":
                    "Knowledge statistics returned.",

                "data":
                    graph.statistics(),

            }



        return {

            "answer":
                "Question analyzed using project knowledge graph.",

            "data":
                {

                    "entities":
                        len(
                            graph.entities()
                        ),

                    "relations":
                        len(
                            graph.relations()
                        ),

                },

        }



assistant_service = AssistantService()
