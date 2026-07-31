"""Core AI assistant engine."""

from __future__ import annotations

from dataclasses import dataclass

from aidk.ai.prompts.engineering import (
    SYSTEM_PROMPT,
    build_engineering_prompt,
)
from aidk.ai.providers.base import (
    LLMProvider,
    LLMRequest,
)
from aidk.ai.retrieval.base import ContextRetriever
from aidk.ai.retrieval.models import RetrievedContext


@dataclass(slots=True)
class AssistantAnswer:
    """Result returned by the assistant engine."""

    answer: str
    provider: str
    context: RetrievedContext


class AssistantEngine:
    """Coordinate retrieval, prompt construction, and generation."""

    def __init__(
        self,
        *,
        retriever: ContextRetriever,
        provider: LLMProvider,
    ) -> None:
        self.retriever = retriever
        self.provider = provider

    def ask(
        self,
        question: str,
    ) -> AssistantAnswer:
        normalized = question.strip()

        if not normalized:
            raise ValueError(
                "Assistant question cannot be empty."
            )

        context = self.retriever.retrieve(
            normalized
        )

        prompt = build_engineering_prompt(
            context
        )

        response = self.provider.generate(
            LLMRequest(
                prompt=prompt,
                system_prompt=SYSTEM_PROMPT,
                metadata={
                    "question": normalized,
                },
            )
        )

        return AssistantAnswer(
            answer=response.text,
            provider=response.provider,
            context=context,
        )
