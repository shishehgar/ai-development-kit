"""Tests for retrieval pipeline construction."""

from __future__ import annotations

from aidk.ai.retrieval import (
    build_retrieval_pipeline,
    RetrievalPipeline,
)
from aidk.knowledge.graph import KnowledgeGraph


def test_empty_pipeline_is_created_without_dependencies() -> None:

    pipeline = build_retrieval_pipeline()

    assert isinstance(
        pipeline,
        RetrievalPipeline,
    )

    assert pipeline.retrievers == []


def test_graph_retriever_is_added() -> None:

    graph = KnowledgeGraph()

    pipeline = build_retrieval_pipeline(
        graph=graph,
    )

    assert len(
        pipeline.retrievers
    ) == 1


def test_extra_retrievers_are_supported() -> None:

    class DummyRetriever:

        def retrieve(
            self,
            question: str,
        ):
            raise NotImplementedError


    pipeline = build_retrieval_pipeline(
        extra_retrievers=[
            DummyRetriever()
        ]
    )

    assert len(
        pipeline.retrievers
    ) == 1
