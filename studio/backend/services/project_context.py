"""Project context resolver."""

from __future__ import annotations


from aidk.knowledge.graph import (
    KnowledgeGraph,
)


from studio.backend.services.project_knowledge import (
    project_knowledge_store,
)


from studio.backend.services.knowledge_runtime import (
    knowledge_runtime,
)



class ProjectContextResolver:
    """
    Resolves knowledge context per project.
    """



    def resolve(
        self,
        project: str | None,
    ) -> KnowledgeGraph:


        if project:

            return (
                project_knowledge_store
                .get_or_create(project)
            )


        return (
            knowledge_runtime.graph
        )



project_context_resolver = (
    ProjectContextResolver()
)
