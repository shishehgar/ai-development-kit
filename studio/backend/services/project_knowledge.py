"""Project scoped persistent knowledge storage."""

from __future__ import annotations


from pathlib import Path


from aidk.knowledge.graph import (
    KnowledgeGraph,
)


from aidk.knowledge.store import (
    KnowledgeGraphStore,
)



class ProjectKnowledgeStore:
    """
    Project knowledge cache with persistence.
    """


    def __init__(
        self,
        root: str | Path = ".aidk/knowledge",
    ):

        self._graphs = {}

        self.store = KnowledgeGraphStore(
            root
        )



    def save(
        self,
        project_id: str,
        graph: KnowledgeGraph,
    ):

        self._graphs[
            project_id
        ] = graph


        self.store.save(
            project_id,
            graph,
        )



    def get_or_create(
        self,
        project_id: str,
    ) -> KnowledgeGraph:


        if project_id in self._graphs:

            return self._graphs[
                project_id
            ]


        if self.store.exists(
            project_id
        ):

            graph = self.store.load(
                project_id
            )

        else:

            graph = KnowledgeGraph()


        self._graphs[
            project_id
        ] = graph


        return graph



    def exists(
        self,
        project_id: str,
    ) -> bool:

        return (
            project_id in self._graphs
            or
            self.store.exists(project_id)
        )



project_knowledge_store = (
    ProjectKnowledgeStore()
)
