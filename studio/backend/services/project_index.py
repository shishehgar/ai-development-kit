"""Project indexing service."""

from __future__ import annotations


from pathlib import Path


from aidk.knowledge.scanner import (
    KnowledgeScanner,
)


from studio.backend.services.project_knowledge import (
    project_knowledge_store,
)



class ProjectIndexService:
    """
    Build project knowledge graph.
    """


    def __init__(self):

        self.scanner = (
            KnowledgeScanner()
        )


    def index_project(
        self,
        project_id: str,
        path: str | Path,
    ):


        graph = (
            self.scanner.scan(
                path
            )
        )


        project_knowledge_store.save(
            project_id,
            graph,
        )


        return {

            "project": project_id,

            "entities":
                len(
                    graph.entities()
                ),

            "relations":
                len(
                    graph.relations()
                ),

        }



project_index_service = (
    ProjectIndexService()
)
