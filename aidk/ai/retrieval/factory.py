"""Factory functions for retrieval runtime composition."""

from __future__ import annotations

from collections.abc import Iterable

from aidk.ai.retrieval.base import ContextRetriever
from aidk.ai.retrieval.pipeline import RetrievalPipeline
from aidk.ai.retrieval.code import CodeContextRetriever
from aidk.ai.retrieval.metadata import ProjectMetadataRetriever
from aidk.ai.retrieval.context import GraphContextRetriever
from aidk.knowledge.graph import KnowledgeGraph


def build_retrieval_pipeline(
    *,
    graph: KnowledgeGraph | None = None,
    project_path: str | None = None,
    extra_retrievers: Iterable[ContextRetriever] = (),
) -> RetrievalPipeline:
    """
    Build the retrieval pipeline.

    Components are added only when their required
    dependencies are provided.
    """

    retrievers: list[ContextRetriever] = []

    if graph is not None:
        retrievers.append(
            GraphContextRetriever(
                graph
            )
        )

    if project_path is not None:
        retrievers.append(
            CodeContextRetriever(
                project_path
            )
        )

        retrievers.append(
            ProjectMetadataRetriever(
                project_path
            )
        )

    retrievers.extend(
        extra_retrievers
    )

    return RetrievalPipeline(
        retrievers
    )
