"""Tests for assistant integration with the application container."""

from __future__ import annotations

from aidk.ai.engine import AssistantAnswer
from aidk.ai.retrieval.models import RetrievedContext
from aidk.application.container import build_services


class FakeAssistantEngine:
    """Minimal engine used to test container wiring."""

    def ask(
        self,
        question: str,
    ) -> AssistantAnswer:
        return AssistantAnswer(
            answer="container-answer",
            provider="fake",
            context=RetrievedContext(
                question=question,
            ),
        )


def test_container_does_not_enable_assistant_by_default() -> None:
    services = build_services()

    assert services.assistant is None


def test_container_wraps_injected_assistant_engine() -> None:
    engine = FakeAssistantEngine()

    services = build_services(
        assistant_engine=engine,
    )

    assert services.assistant is not None

    result = services.assistant.ask(
        "How does the container work?"
    )

    assert result.answer == "container-answer"
    assert result.provider == "fake"


def test_container_accepts_ai_runtime() -> None:
    from aidk.ai.config import AISettings
    from aidk.ai.runtime import AIRuntime
    from aidk.ai.providers.local import LocalRuleProvider

    engine = FakeAssistantEngine()
    provider = LocalRuleProvider()

    runtime = AIRuntime(
        settings=AISettings(
            provider="local",
        ),
        provider=provider,
        engine=engine,
    )

    services = build_services(
        ai_runtime=runtime,
    )

    assert services.assistant is not None

    result = services.assistant.ask(
        "Runtime integration"
    )

    assert result.answer == "container-answer"


def test_container_rejects_two_assistant_sources() -> None:
    import pytest

    from aidk.ai.config import AISettings
    from aidk.ai.runtime import AIRuntime
    from aidk.ai.providers.local import LocalRuleProvider

    engine = FakeAssistantEngine()

    runtime = AIRuntime(
        settings=AISettings(
            provider="local",
        ),
        provider=LocalRuleProvider(),
        engine=engine,
    )

    with pytest.raises(
        ValueError,
        match="either assistant_engine or ai_runtime",
    ):
        build_services(
            assistant_engine=engine,
            ai_runtime=runtime,
        )
