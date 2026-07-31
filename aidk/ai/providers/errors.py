"""Exceptions raised by language-model providers."""

from __future__ import annotations


class LLMProviderError(RuntimeError):
    """Base exception for language-model provider failures."""


class LLMConnectionError(LLMProviderError):
    """Raised when the provider endpoint cannot be reached."""


class LLMTimeoutError(LLMProviderError):
    """Raised when a provider request exceeds its timeout."""


class LLMResponseError(LLMProviderError):
    """Raised when a provider returns an invalid response."""
