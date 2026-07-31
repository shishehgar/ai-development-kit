"""Ollama language-model provider."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field

from aidk.ai.providers.base import (
    LLMRequest,
    LLMResponse,
)
from aidk.ai.providers.errors import (
    LLMConnectionError,
    LLMProviderError,
    LLMResponseError,
    LLMTimeoutError,
)
from aidk.ai.providers.transport import (
    HTTPTransport,
    UrllibHTTPTransport,
)


@dataclass(slots=True)
class OllamaConfig:
    """Configuration for an Ollama provider."""

    model: str = "qwen2.5-coder:7b"
    endpoint: str = "http://127.0.0.1:11434"
    timeout: float = 60.0
    retries: int = 1
    retry_delay: float = 0.25
    options: dict[str, object] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        self.endpoint = self.endpoint.rstrip("/")

        if not self.model.strip():
            raise ValueError(
                "Ollama model cannot be empty."
            )

        if self.timeout <= 0:
            raise ValueError(
                "Ollama timeout must be greater than zero."
            )

        if self.retries < 0:
            raise ValueError(
                "Ollama retries cannot be negative."
            )

        if self.retry_delay < 0:
            raise ValueError(
                "Ollama retry delay cannot be negative."
            )


class OllamaProvider:
    """Generate assistant responses through Ollama."""

    def __init__(
        self,
        config: OllamaConfig | None = None,
        *,
        transport: HTTPTransport | None = None,
    ) -> None:
        self.config = config or OllamaConfig()
        self.transport = transport or UrllibHTTPTransport()

    @property
    def name(self) -> str:
        return "ollama"

    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        payload = self._build_payload(request)
        response_data = self._execute(payload)

        text = response_data.get("response")

        if not isinstance(text, str):
            raise LLMResponseError(
                "Ollama response does not contain a valid "
                "'response' field."
            )

        model = response_data.get("model")

        return LLMResponse(
            text=text,
            provider=self.name,
            model=(
                model
                if isinstance(model, str)
                else self.config.model
            ),
            metadata={
                "done": bool(
                    response_data.get("done", False)
                ),
                "done_reason": response_data.get(
                    "done_reason"
                ),
                "total_duration": response_data.get(
                    "total_duration"
                ),
                "load_duration": response_data.get(
                    "load_duration"
                ),
                "prompt_eval_count": response_data.get(
                    "prompt_eval_count"
                ),
                "eval_count": response_data.get(
                    "eval_count"
                ),
            },
        )

    def _build_payload(
        self,
        request: LLMRequest,
    ) -> dict[str, object]:
        options = dict(self.config.options)

        options.setdefault(
            "temperature",
            request.temperature,
        )

        payload: dict[str, object] = {
            "model": self.config.model,
            "prompt": request.prompt,
            "stream": False,
            "options": options,
        }

        if request.system_prompt:
            payload["system"] = request.system_prompt

        return payload

    def _execute(
        self,
        payload: dict[str, object],
    ) -> dict[str, object]:
        attempts = self.config.retries + 1
        last_error: LLMProviderError | None = None

        for attempt in range(attempts):
            try:
                response = self.transport.post_json(
                    url=(
                        f"{self.config.endpoint}"
                        "/api/generate"
                    ),
                    payload=payload,
                    timeout=self.config.timeout,
                )

                return self._decode_response(
                    response.status_code,
                    response.body,
                )

            except (
                LLMConnectionError,
                LLMTimeoutError,
            ) as exc:
                last_error = exc

                if attempt >= attempts - 1:
                    raise

                if self.config.retry_delay:
                    time.sleep(
                        self.config.retry_delay
                    )

        if last_error is not None:
            raise last_error

        raise LLMProviderError(
            "Ollama request failed without a reported error."
        )

    @staticmethod
    def _decode_response(
        status_code: int,
        body: bytes,
    ) -> dict[str, object]:
        try:
            decoded = json.loads(
                body.decode("utf-8")
            )
        except (
            UnicodeDecodeError,
            json.JSONDecodeError,
        ) as exc:
            raise LLMResponseError(
                "Ollama returned invalid JSON."
            ) from exc

        if not isinstance(decoded, dict):
            raise LLMResponseError(
                "Ollama returned an unexpected response type."
            )

        if status_code < 200 or status_code >= 300:
            error_message = decoded.get("error")

            if not isinstance(error_message, str):
                error_message = (
                    f"HTTP status {status_code}"
                )

            raise LLMResponseError(
                f"Ollama request failed: {error_message}"
            )

        return decoded
