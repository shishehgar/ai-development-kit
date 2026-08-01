"""Tests for the assistant application service."""

from __future__ import annotations

from aidk.ai.engine import AssistantAnswer
from aidk.ai.retrieval.models import RetrievedContext
from aidk.application.assistant_service import AssistantService


class FakeAssistantEngine:
    """Deterministic assistant engine used by service tests."""

    def __init__(self) -> None:
        self.questions: list[str] = []

    def ask(
        self,
        question: str,
    ) -> AssistantAnswer:
        self.questions.append(question)

        return AssistantAnswer(
            answer=f"answer:{question}",
            provider="fake",
            context=RetrievedContext(
                question=question,
            ),
        )


def test_assistant_service_delegates_to_engine() -> None:
    engine = FakeAssistantEngine()
    service = AssistantService(
        engine=engine,
    )

    result = service.ask(
        "  Explain the architecture  "
    )

    assert engine.questions == [
        "Explain the architecture",
    ]
    assert result.answer == (
        "answer:Explain the architecture"
    )
    assert result.provider == "fake"


def test_assistant_service_rejects_empty_question() -> None:
    engine = FakeAssistantEngine()
    service = AssistantService(
        engine=engine,
    )

    try:
        service.ask("   ")
    except ValueError as exc:
        assert str(exc) == (
            "Assistant question cannot be empty."
        )
    else:
        raise AssertionError(
            "Expected ValueError for an empty question."
        )

    assert engine.questions == []
