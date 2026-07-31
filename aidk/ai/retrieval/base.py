"""Common retrieval contracts."""

from __future__ import annotations

from typing import Protocol

from aidk.ai.retrieval.models import RetrievedContext


class ContextRetriever(Protocol):
    """Contract implemented by assistant context retrievers."""

    def retrieve(
        self,
        question: str,
    ) -> RetrievedContext:
        """Retrieve structured context for a user question."""
