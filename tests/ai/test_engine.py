"""Tests for the AIDK assistant engine."""

from __future__ import annotations

import pytest

from aidk.ai import (
    AssistantEngine,
    GraphContextRetriever,
    LocalRuleProvider,
)
from aidk.knowledge import (
    KnowledgeGraph,
    ModuleEntity,
)


def test_assistant_engine_returns_answer() -> None:
    graph = KnowledgeGraph()

    graph.add_entity(
        ModuleEntity(
            name="workspace",
            path="aidk/workspace.py",
        )
    )

    engine = AssistantEngine(
        retriever=GraphContextRetriever(
            graph
        ),
        provider=LocalRuleProvider(),
    )

    result = engine.ask(
        "workspace"
    )

    assert result.provider == "local-rule"
    assert result.answer
    assert len(
        result.context.matched_entities
    ) == 1


def test_assistant_engine_rejects_empty_question() -> None:
    engine = AssistantEngine(
        retriever=GraphContextRetriever(
            KnowledgeGraph()
        ),
        provider=LocalRuleProvider(),
    )

    with pytest.raises(
        ValueError,
        match="cannot be empty",
    ):
        engine.ask("   ")
