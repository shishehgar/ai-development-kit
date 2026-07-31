"""Tests for retrieval context models."""

from __future__ import annotations

from aidk.ai.retrieval import RetrievedContext


def test_retrieved_context_serializes() -> None:
    context = RetrievedContext(
        question="workspace",
        statistics={
            "entities": 1,
        },
        metadata={
            "git_branch": "studio",
        },
    )

    payload = context.to_dict()

    assert payload["question"] == "workspace"
    assert payload["statistics"] == {
        "entities": 1,
    }
    assert payload["metadata"] == {
        "git_branch": "studio",
    }
