"""Base interfaces for AIDK language-model providers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(slots=True)
class LLMRequest:
    """Normalized request sent to a language-model provider."""

    prompt: str
    system_prompt: str | None = None
    temperature: float = 0.2
    metadata: dict[str, object] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class LLMResponse:
    """Normalized response returned by a language-model provider."""

    text: str
    provider: str
    model: str | None = None
    metadata: dict[str, object] = field(
        default_factory=dict
    )


class LLMProvider(Protocol):
    """Contract implemented by all LLM providers."""

    @property
    def name(self) -> str:
        """Return the provider identifier."""

    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """Generate a response for the supplied request."""
