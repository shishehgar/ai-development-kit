"""Deterministic local provider used before external LLM integration."""

from __future__ import annotations

from aidk.ai.providers.base import (
    LLMRequest,
    LLMResponse,
)


class LocalRuleProvider:
    """Minimal provider for deterministic development and tests."""

    @property
    def name(self) -> str:
        return "local-rule"

    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        prompt = request.prompt.strip()

        if not prompt:
            text = "No prompt was provided."
        else:
            text = (
                "The request was analyzed using the available "
                "project knowledge context."
            )

        return LLMResponse(
            text=text,
            provider=self.name,
            model="deterministic",
            metadata={
                "prompt_length": len(prompt),
            },
        )
