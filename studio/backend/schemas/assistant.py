"""Assistant API schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class AssistantAskRequest(BaseModel):
    """User question payload."""

    question: str = Field(
        min_length=1,
        description="Engineering question.",
    )

    project: str | None = Field(
        default=None,
        description="Selected project context.",
    )


class AssistantAskResponse(BaseModel):
    """Assistant answer payload."""

    answer: str

    provider: str

    question: str

    project: str | None = None
