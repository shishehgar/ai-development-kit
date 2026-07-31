"""Tests for the Ollama language-model provider."""

from __future__ import annotations

import json

import pytest

from aidk.ai.providers import (
    HTTPResponse,
    LLMConnectionError,
    LLMRequest,
    LLMResponseError,
    OllamaConfig,
    OllamaProvider,
)


class SuccessfulTransport:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def post_json(
        self,
        *,
        url: str,
        payload: dict[str, object],
        headers: dict[str, str] | None = None,
        timeout: float = 30.0,
    ) -> HTTPResponse:
        self.calls.append(
            {
                "url": url,
                "payload": payload,
                "headers": headers,
                "timeout": timeout,
            }
        )

        return HTTPResponse(
            status_code=200,
            body=json.dumps(
                {
                    "model": "qwen2.5-coder:7b",
                    "response": "WorkspaceService manages workspaces.",
                    "done": True,
                    "eval_count": 12,
                }
            ).encode("utf-8"),
            headers={},
        )


class FailingTransport:
    def __init__(self) -> None:
        self.call_count = 0

    def post_json(
        self,
        *,
        url: str,
        payload: dict[str, object],
        headers: dict[str, str] | None = None,
        timeout: float = 30.0,
    ) -> HTTPResponse:
        self.call_count += 1

        raise LLMConnectionError(
            "Ollama is unavailable."
        )


class InvalidJSONTransport:
    def post_json(
        self,
        *,
        url: str,
        payload: dict[str, object],
        headers: dict[str, str] | None = None,
        timeout: float = 30.0,
    ) -> HTTPResponse:
        return HTTPResponse(
            status_code=200,
            body=b"not-json",
            headers={},
        )


class ErrorResponseTransport:
    def post_json(
        self,
        *,
        url: str,
        payload: dict[str, object],
        headers: dict[str, str] | None = None,
        timeout: float = 30.0,
    ) -> HTTPResponse:
        return HTTPResponse(
            status_code=404,
            body=json.dumps(
                {
                    "error": "model not found",
                }
            ).encode("utf-8"),
            headers={},
        )


def test_ollama_provider_generates_response() -> None:
    transport = SuccessfulTransport()

    provider = OllamaProvider(
        OllamaConfig(
            model="qwen2.5-coder:7b",
            endpoint="http://localhost:11434/",
            timeout=15.0,
            retries=0,
        ),
        transport=transport,
    )

    response = provider.generate(
        LLMRequest(
            prompt="Explain WorkspaceService.",
            system_prompt="Use repository context.",
            temperature=0.1,
        )
    )

    assert response.provider == "ollama"
    assert response.model == "qwen2.5-coder:7b"
    assert response.text == (
        "WorkspaceService manages workspaces."
    )

    assert transport.calls[0]["url"] == (
        "http://localhost:11434/api/generate"
    )
    assert transport.calls[0]["timeout"] == 15.0

    payload = transport.calls[0]["payload"]

    assert isinstance(payload, dict)
    assert payload["stream"] is False
    assert payload["system"] == (
        "Use repository context."
    )
    assert payload["options"] == {
        "temperature": 0.1,
    }


def test_ollama_provider_retries_connection_errors() -> None:
    transport = FailingTransport()

    provider = OllamaProvider(
        OllamaConfig(
            retries=2,
            retry_delay=0,
        ),
        transport=transport,
    )

    with pytest.raises(
        LLMConnectionError,
        match="unavailable",
    ):
        provider.generate(
            LLMRequest(
                prompt="Analyze the project."
            )
        )

    assert transport.call_count == 3


def test_ollama_provider_rejects_invalid_json() -> None:
    provider = OllamaProvider(
        OllamaConfig(
            retries=0,
        ),
        transport=InvalidJSONTransport(),
    )

    with pytest.raises(
        LLMResponseError,
        match="invalid JSON",
    ):
        provider.generate(
            LLMRequest(
                prompt="Analyze."
            )
        )


def test_ollama_provider_reports_api_error() -> None:
    provider = OllamaProvider(
        OllamaConfig(
            retries=0,
        ),
        transport=ErrorResponseTransport(),
    )

    with pytest.raises(
        LLMResponseError,
        match="model not found",
    ):
        provider.generate(
            LLMRequest(
                prompt="Analyze."
            )
        )


def test_ollama_config_rejects_invalid_values() -> None:
    with pytest.raises(
        ValueError,
        match="model cannot be empty",
    ):
        OllamaConfig(
            model=" "
        )

    with pytest.raises(
        ValueError,
        match="timeout",
    ):
        OllamaConfig(
            timeout=0
        )

    with pytest.raises(
        ValueError,
        match="retries",
    ):
        OllamaConfig(
            retries=-1
        )
