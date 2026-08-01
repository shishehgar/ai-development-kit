"""Tests for AI provider construction."""

from __future__ import annotations

import pytest

from aidk.ai.config import AISettings
from aidk.ai.factory import (
    UnknownAIProviderError,
    build_llm_provider,
)
from aidk.ai.providers.local import LocalRuleProvider
from aidk.ai.providers.ollama import OllamaProvider
from aidk.ai.providers.transport import (
    HTTPResponse,
)


class FakeTransport:
    """Minimal transport used to verify dependency injection."""

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


def test_factory_builds_local_provider() -> None:
    provider = build_llm_provider(
        AISettings(
            provider="local",
        )
    )

    assert isinstance(
        provider,
        LocalRuleProvider,
    )
    assert provider.name == "local-rule"


def test_factory_builds_configured_ollama_provider() -> None:
    transport = FakeTransport()

    provider = build_llm_provider(
        AISettings(
            provider="ollama",
            ollama_model="qwen3:8b",
            ollama_endpoint=(
                "http://ollama.internal:11434/"
            ),
            ollama_timeout=90.0,
            ollama_retries=2,
            ollama_retry_delay=0.1,
        ),
        transport=transport,
    )

    assert isinstance(
        provider,
        OllamaProvider,
    )
    assert provider.transport is transport
    assert provider.config.model == "qwen3:8b"
    assert provider.config.endpoint == (
        "http://ollama.internal:11434"
    )
    assert provider.config.timeout == 90.0
    assert provider.config.retries == 2


def test_factory_rejects_unknown_provider() -> None:
    with pytest.raises(
        UnknownAIProviderError,
        match="Unsupported AI provider",
    ):
        build_llm_provider(
            AISettings(
                provider="unknown",
            )
        )
