"""Tests for environment-based AI configuration."""

from __future__ import annotations

import pytest

from aidk.ai.config import (
    AIConfigurationError,
    AISettings,
    load_ai_settings,
)


def test_default_settings_use_local_provider() -> None:
    settings = load_ai_settings({})

    assert settings.provider == "local"
    assert settings.ollama_model == "qwen2.5-coder:7b"
    assert settings.ollama_endpoint == (
        "http://127.0.0.1:11434"
    )
    assert settings.ollama_timeout == 60.0
    assert settings.ollama_retries == 1


def test_settings_are_loaded_from_environment() -> None:
    settings = load_ai_settings(
        {
            "AIDK_AI_PROVIDER": "OLLAMA",
            "AIDK_OLLAMA_MODEL": "qwen3:8b",
            "AIDK_OLLAMA_ENDPOINT": (
                "http://ollama.internal:11434/"
            ),
            "AIDK_OLLAMA_TIMEOUT": "120",
            "AIDK_OLLAMA_RETRIES": "3",
            "AIDK_OLLAMA_RETRY_DELAY": "0.5",
        }
    )

    assert settings.provider == "ollama"
    assert settings.ollama_model == "qwen3:8b"
    assert settings.ollama_endpoint == (
        "http://ollama.internal:11434"
    )
    assert settings.ollama_timeout == 120.0
    assert settings.ollama_retries == 3
    assert settings.ollama_retry_delay == 0.5


def test_invalid_float_setting_is_rejected() -> None:
    with pytest.raises(
        AIConfigurationError,
        match="AIDK_OLLAMA_TIMEOUT",
    ):
        load_ai_settings(
            {
                "AIDK_OLLAMA_TIMEOUT": "invalid",
            }
        )


def test_invalid_integer_setting_is_rejected() -> None:
    with pytest.raises(
        AIConfigurationError,
        match="AIDK_OLLAMA_RETRIES",
    ):
        load_ai_settings(
            {
                "AIDK_OLLAMA_RETRIES": "1.5",
            }
        )


def test_negative_retry_count_is_rejected() -> None:
    with pytest.raises(
        AIConfigurationError,
        match="cannot be negative",
    ):
        AISettings(
            ollama_retries=-1,
        )
