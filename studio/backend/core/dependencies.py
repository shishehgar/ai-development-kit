"""FastAPI dependency providers."""

from __future__ import annotations



from aidk.ai import (
    build_ai_runtime,
    load_ai_settings,
)


from aidk.ai.retrieval.context import (
    GraphContextRetriever,
)


from aidk.application.assistant_service import (
    AssistantService,
)


from studio.backend.services.project_context import (
    project_context_resolver,
)



def get_ai_assistant_service(
    project: str | None = None,
):


    graph = (
        project_context_resolver.resolve(
            project
        )
    )


    retriever = GraphContextRetriever(
        graph
    )


    runtime = build_ai_runtime(
        settings=load_ai_settings(),
        retriever=retriever,
    )


    return AssistantService(
        engine=runtime.engine,
    )
