"""Factories for AIDK language-model providers."""

from __future__ import annotations

from typing import Any

from aidk.ai.config import AISettings
from aidk.ai.providers.base import LLMProvider
from aidk.ai.providers.registry import (
    get_provider_factory,
)


class UnknownAIProviderError(ValueError):
    """Raised when the configured AI provider is unsupported."""


def build_llm_provider(
    settings: AISettings,
    *,
    transport: Any | None = None,
) -> LLMProvider:
    """Construct the configured language-model provider."""

    provider_name = (
        settings.provider
        .strip()
        .lower()
    )

    if provider_name == "openai-compatible":
        from aidk.ai.providers.openai_compatible import (
            OpenAICompatibleConfig,
            OpenAICompatibleProvider,
        )

        config = OpenAICompatibleConfig(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
            model=settings.openai_model,
            timeout=settings.ollama_timeout,
        )

        return OpenAICompatibleProvider(
            config=config,
            transport=transport,
        )

    try:
        provider_factory = get_provider_factory(
            provider_name
        )
    except ValueError as exc:
        raise UnknownAIProviderError(
            f"Unsupported AI provider: "
            f"{provider_name!r}"
        ) from exc

    try:
        return provider_factory(
            settings=settings,
            transport=transport,
        )
    except Exception as exc:
        raise UnknownAIProviderError(
            "Provider factory could not be "
            "initialized for "
            f"{provider_name!r}."
        ) from exc
