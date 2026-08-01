"""Runtime composition for the AIDK assistant."""

from __future__ import annotations

from dataclasses import dataclass

from aidk.ai.config import (
    AISettings,
    load_ai_settings,
)
from aidk.ai.engine import AssistantEngine
from aidk.ai.factory import (
    build_llm_provider,
)
from aidk.ai.providers.base import (
    LLMProvider,
)
from aidk.ai.providers.transport import (
    HTTPTransport,
)
from aidk.ai.retrieval import (
    build_retrieval_pipeline,
)
from aidk.ai.retrieval.pipeline import (
    RetrievalPipeline,
)
from aidk.knowledge.graph import (
    KnowledgeGraph,
)


@dataclass(frozen=True, slots=True)
class AIRuntime:
    """Fully initialized AI runtime."""

    settings: AISettings
    provider: LLMProvider
    engine: AssistantEngine
    retriever: RetrievalPipeline | None = None


def build_ai_runtime(
    *,
    settings: AISettings | None = None,
    graph: KnowledgeGraph | None = None,
    project_path: str | None = None,
    retriever=None,
    transport: HTTPTransport | None = None,
) -> AIRuntime:
    """
    Build the complete AI execution runtime.

    Supports both:
    - explicit retriever injection (legacy compatibility)
    - automatic retrieval pipeline construction
    """

    resolved_settings = (
        settings
        if settings is not None
        else load_ai_settings()
    )

    provider = build_llm_provider(
        resolved_settings,
        transport=transport,
    )

    if retriever is not None:
        resolved_retriever = retriever

    else:
        resolved_retriever = build_retrieval_pipeline(
            graph=graph,
            project_path=project_path,
        )

    engine = AssistantEngine(
        retriever=resolved_retriever,
        provider=provider,
    )

    return AIRuntime(
        settings=resolved_settings,
        provider=provider,
        retriever=resolved_retriever,
        engine=engine,
    )
