"""Environment-based configuration for the AIDK AI runtime."""

from __future__ import annotations

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Mapping

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]


load_dotenv(
    PROJECT_ROOT / ".env"
)

class AIConfigurationError(ValueError):
    """Raised when AI runtime configuration is invalid."""


@dataclass(frozen=True, slots=True)
class AISettings:
    """Normalized AI runtime settings."""
    # OpenAI Compatible
    openai_api_key: str = ""
    openai_base_url: str = ""
    openai_model: str = ""

    provider: str = "local"
    ollama_model: str = "qwen2.5-coder:7b"
    ollama_endpoint: str = "http://127.0.0.1:11434"
    ollama_timeout: float = 60.0
    ollama_retries: int = 1
    ollama_retry_delay: float = 0.25
    ollama_options: dict[str, object] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        provider = self.provider.strip().lower()

        if not provider:
            raise AIConfigurationError(
                "AI provider cannot be empty."
            )

        if self.ollama_timeout <= 0:
            raise AIConfigurationError(
                "Ollama timeout must be greater than zero."
            )

        if self.ollama_retries < 0:
            raise AIConfigurationError(
                "Ollama retries cannot be negative."
            )

        if self.ollama_retry_delay < 0:
            raise AIConfigurationError(
                "Ollama retry delay cannot be negative."
            )

        object.__setattr__(
            self,
            "provider",
            provider,
        )

        object.__setattr__(
            self,
            "ollama_endpoint",
            self.ollama_endpoint.rstrip("/"),
        )


def load_ai_settings(
    environment: Mapping[str, str] | None = None,
) -> AISettings:
    """Load AI settings from an environment mapping."""

    env = environment if environment is not None else os.environ

    return AISettings(
        provider=env.get(
            "AIDK_AI_PROVIDER",
            "local",
        ),
        ollama_model=env.get(
            "AIDK_OLLAMA_MODEL",
            "qwen2.5-coder:7b",
        ),
        ollama_endpoint=env.get(
            "AIDK_OLLAMA_ENDPOINT",
            "http://127.0.0.1:11434",
        ),
        ollama_timeout=_read_float(
            env,
            "AIDK_OLLAMA_TIMEOUT",
            default=60.0,
        ),
        ollama_retries=_read_int(
            env,
            "AIDK_OLLAMA_RETRIES",
            default=1,
        ),
        ollama_retry_delay=_read_float(
            env,
            "AIDK_OLLAMA_RETRY_DELAY",
            default=0.25,
        ),
        openai_api_key=env.get(
            "AIDK_OPENAI_API_KEY",
            "",
        ),
        openai_base_url=env.get(
            "AIDK_OPENAI_BASE_URL",
            "",
        ),
        openai_model=env.get(
            "AIDK_OPENAI_MODEL",
            "",
        ),
    )


def _read_float(
    environment: Mapping[str, str],
    name: str,
    *,
    default: float,
) -> float:
    raw_value = environment.get(name)

    if raw_value is None or not raw_value.strip():
        return default

    try:
        return float(raw_value)
    except ValueError as exc:
        raise AIConfigurationError(
            f"{name} must be a valid number."
        ) from exc


def _read_int(
    environment: Mapping[str, str],
    name: str,
    *,
    default: int,
) -> int:
    raw_value = environment.get(name)

    if raw_value is None or not raw_value.strip():
        return default

    try:
        return int(raw_value)
    except ValueError as exc:
        raise AIConfigurationError(
            f"{name} must be a valid integer."
        ) from exc
