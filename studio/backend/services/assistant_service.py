"""Backend adapter for the application assistant."""

from __future__ import annotations

from aidk.application.assistant_service import (
    AssistantService,
)


class AssistantAPIService:
    """Translate application assistant into API responses."""

    def __init__(
        self,
        service: AssistantService,
    ) -> None:
        self.service = service


    def ask(
        self,
        question: str,
    ) -> dict[str, str]:

        result = self.service.ask(
            question
        )

        return {
            "answer": result.answer,
            "provider": result.provider,
            "question": question,
        }
