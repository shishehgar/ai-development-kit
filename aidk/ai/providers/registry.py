"""AI provider registry."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from aidk.ai.config import AISettings
from aidk.ai.providers.base import LLMProvider
from aidk.ai.providers.local import LocalRuleProvider
from aidk.ai.providers.ollama import (
    OllamaConfig,
    OllamaProvider,
)


ProviderFactory = Callable[
    ...,
    LLMProvider,
]


_PROVIDER_REGISTRY: dict[
    str,
    ProviderFactory,
] = {}


def register_provider(
    name: str,
    factory: ProviderFactory,
) -> None:
    """Register or replace an AI provider factory."""

    normalized = name.strip().lower()

    if not normalized:
        raise ValueError(
            "Provider name cannot be empty."
        )

    _PROVIDER_REGISTRY[
        normalized
    ] = factory


def get_provider_factory(
    name: str,
) -> ProviderFactory:
    """Return a registered provider factory."""

    normalized = name.strip().lower()

    try:
        return _PROVIDER_REGISTRY[
            normalized
        ]
    except KeyError as exc:
        raise ValueError(
            f"Unknown AI provider: {name}"
        ) from exc


def list_providers() -> list[str]:
    """Return registered provider names."""

    return sorted(
        _PROVIDER_REGISTRY.keys()
    )


def build_local_provider(
    *,
    settings: AISettings,
    transport: Any | None = None,
) -> LLMProvider:
    """Build the deterministic local provider."""

    del settings
    del transport

    return LocalRuleProvider()


def build_ollama_provider(
    *,
    settings: AISettings,
    transport: Any | None = None,
) -> LLMProvider:
    """Build an Ollama provider from normalized AI settings."""

    config = OllamaConfig(
        model=settings.ollama_model,
        endpoint=settings.ollama_endpoint,
        timeout=settings.ollama_timeout,
        retries=settings.ollama_retries,
        retry_delay=settings.ollama_retry_delay,
        options=dict(
            settings.ollama_options
        ),
    )

    return OllamaProvider(
        config=config,
        transport=transport,
    )


register_provider(
    "local",
    build_local_provider,
)

register_provider(
    "ollama",
    build_ollama_provider,
)
