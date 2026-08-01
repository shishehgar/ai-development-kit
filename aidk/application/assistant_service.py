"""Application service for the AIDK engineering assistant."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from aidk.ai.engine import AssistantAnswer


class AssistantRunner(Protocol):
    """Contract required by the assistant application service."""

    def ask(
        self,
        question: str,
    ) -> AssistantAnswer:
        """Answer an engineering question."""


@dataclass(slots=True)
class AssistantService:
    """Expose the AI assistant through the application layer."""

    engine: AssistantRunner

    def ask(
        self,
        question: str,
    ) -> AssistantAnswer:
        """Delegate a normalized question to the assistant engine."""

        normalized = question.strip()

        if not normalized:
            raise ValueError(
                "Assistant question cannot be empty."
            )

        return self.engine.ask(normalized)
