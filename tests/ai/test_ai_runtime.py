"""Tests for AI runtime composition."""

from __future__ import annotations

from aidk.ai.config import AISettings
from aidk.ai.engine import AssistantEngine
from aidk.ai.providers.local import LocalRuleProvider
from aidk.ai.providers.ollama import OllamaProvider
from aidk.ai.providers.transport import HTTPResponse
from aidk.ai.retrieval.models import RetrievedContext
from aidk.ai.runtime import build_ai_runtime


class FakeRetriever:
    """Deterministic context retriever for runtime tests."""

    def __init__(self) -> None:
        self.questions: list[str] = []

    def retrieve(
        self,
        question: str,
    ) -> RetrievedContext:
        self.questions.append(question)

        return RetrievedContext(
            question=question,
        )


class FakeTransport:
    """Network-free transport for Ollama runtime construction."""

    def post_json(
        self,
        *,
        url: str,
        payload: dict[str, object],
        timeout: float,
    ) -> HTTPResponse:
        return HTTPResponse(
            status_code=200,
            body=b'{"response": "ok", "done": true}',
        )


def test_runtime_builds_local_provider_by_default() -> None:
    retriever = FakeRetriever()

    runtime = build_ai_runtime(
        retriever=retriever,
        settings=AISettings(
            provider="local",
        ),
    )

    assert runtime.settings.provider == "local"
    assert isinstance(
        runtime.provider,
        LocalRuleProvider,
    )
    assert isinstance(
        runtime.engine,
        AssistantEngine,
    )


def test_runtime_builds_ollama_without_network_request() -> None:
    retriever = FakeRetriever()
    transport = FakeTransport()

    runtime = build_ai_runtime(
        retriever=retriever,
        settings=AISettings(
            provider="ollama",
            ollama_model="qwen3:8b",
            ollama_endpoint=(
                "http://ollama.internal:11434"
            ),
        ),
        transport=transport,
    )

    assert isinstance(
        runtime.provider,
        OllamaProvider,
    )
    assert runtime.provider.transport is transport
    assert runtime.provider.config.model == "qwen3:8b"
    assert isinstance(
        runtime.engine,
        AssistantEngine,
    )


def test_runtime_preserves_explicit_settings() -> None:
    retriever = FakeRetriever()

    settings = AISettings(
        provider="local",
        ollama_timeout=75.0,
    )

    runtime = build_ai_runtime(
        retriever=retriever,
        settings=settings,
    )

    assert runtime.settings is settings
