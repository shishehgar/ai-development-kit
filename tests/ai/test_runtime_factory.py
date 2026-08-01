"""Tests for unified AI runtime construction."""

from __future__ import annotations

from aidk.ai import (
    AISettings,
    AIRuntime,
    build_ai_runtime,
)
from aidk.ai.providers.local import (
    LocalRuleProvider,
)
from aidk.ai.retrieval.pipeline import (
    RetrievalPipeline,
)
from aidk.knowledge.graph import (
    KnowledgeGraph,
)


def test_runtime_builds_all_components():

    runtime = build_ai_runtime(
        settings=AISettings(
            provider="local",
        ),
        graph=KnowledgeGraph(),
    )

    assert isinstance(
        runtime,
        AIRuntime,
    )

    assert isinstance(
        runtime.provider,
        LocalRuleProvider,
    )

    assert isinstance(
        runtime.retriever,
        RetrievalPipeline,
    )

    assert runtime.engine is not None


def test_runtime_accepts_project_without_network():

    runtime = build_ai_runtime(
        settings=AISettings(
            provider="local",
        ),
        project_path=".",
    )

    assert runtime.retriever is not None
