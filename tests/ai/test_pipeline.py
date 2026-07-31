"""Tests for the composed retrieval pipeline."""

from __future__ import annotations

from aidk.ai.retrieval import (
    RetrievedContext,
    RetrievalPipeline,
)


class FirstRetriever:
    def retrieve(
        self,
        question: str,
    ) -> RetrievedContext:
        return RetrievedContext(
            question=question,
            statistics={
                "entities": 2,
            },
            matched_entities=[
                {
                    "id": "module:workspace",
                    "name": "workspace",
                }
            ],
        )


class SecondRetriever:
    def retrieve(
        self,
        question: str,
    ) -> RetrievedContext:
        return RetrievedContext(
            question=question,
            code_matches=[
                {
                    "path": "aidk/workspace.py",
                    "score": 10,
                    "snippets": [],
                }
            ],
            metadata={
                "git_branch": "studio",
            },
        )


def test_pipeline_merges_retrieval_results() -> None:
    pipeline = RetrievalPipeline(
        [
            FirstRetriever(),
            SecondRetriever(),
        ]
    )

    context = pipeline.retrieve(
        "workspace"
    )

    assert context.question == "workspace"
    assert context.statistics["entities"] == 2
    assert len(context.matched_entities) == 1
    assert len(context.code_matches) == 1
    assert context.metadata["git_branch"] == "studio"


def test_pipeline_supports_no_retrievers() -> None:
    pipeline = RetrievalPipeline([])

    context = pipeline.retrieve(
        "workspace"
    )

    assert context.question == "workspace"
    assert context.matched_entities == []
    assert context.code_matches == []
