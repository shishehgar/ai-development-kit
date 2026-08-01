"""OpenAI-compatible language-model provider."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from aidk.ai.providers.base import (
    LLMRequest,
    LLMResponse,
)
from aidk.ai.providers.transport import (
    HTTPTransport,
    UrllibHTTPTransport,
)


@dataclass(slots=True, frozen=True)
class OpenAICompatibleConfig:
    """Configuration for an OpenAI-compatible API."""

    api_key: str
    base_url: str
    model: str
    timeout: float = 120.0

    def __post_init__(self) -> None:
        """Validate provider configuration."""

        if not self.base_url.strip():
            raise ValueError(
                "OpenAI-compatible base URL is required."
            )

        if not self.model.strip():
            raise ValueError(
                "OpenAI-compatible model is required."
            )

        if self.timeout <= 0:
            raise ValueError(
                "OpenAI-compatible timeout must be positive."
            )


class OpenAICompatibleProvider:
    """
    Provider for APIs implementing the OpenAI chat-completions protocol.

    Compatible backends can include Ollama, OpenAI, OpenRouter, vLLM,
    LM Studio, Groq and other OpenAI-compatible services.
    """

    def __init__(
        self,
        config: OpenAICompatibleConfig,
        *,
        transport: HTTPTransport | None = None,
    ) -> None:
        """Initialize the provider."""

        self.config = config
        self.transport = transport or UrllibHTTPTransport()

    @property
    def name(self) -> str:
        """Return the provider identifier."""

        return "openai-compatible"

    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """Generate a response using the chat-completions endpoint."""

        messages: list[dict[str, str]] = []

        if request.system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": request.system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": request.prompt,
            }
        )

        payload: dict[str, Any] = {
            "model": self.config.model,
            "messages": messages,
            "temperature": request.temperature,
            "stream": False,
        }

        headers = {
            "Content-Type": "application/json",
        }

        if self.config.api_key:
            headers["Authorization"] = (
                f"Bearer {self.config.api_key}"
            )

        response = self.transport.post_json(
            url=(
                self.config.base_url.rstrip("/")
                + "/chat/completions"
            ),
            payload=payload,
            timeout=self.config.timeout,
            headers=headers,
        )

        data = json.loads(
            response.body.decode("utf-8")
        )

        try:
            answer = data["choices"][0]["message"]["content"]
        except (
            KeyError,
            IndexError,
            TypeError,
        ) as exc:
            raise RuntimeError(
                "OpenAI-compatible backend returned an invalid "
                "chat-completions response."
            ) from exc

        if not isinstance(answer, str):
            raise RuntimeError(
                "OpenAI-compatible backend returned non-text content."
            )

        return LLMResponse(
            text=answer,
            provider=self.name,
            model=self.config.model,
            metadata=data,
        )
