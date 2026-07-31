"""Composable retrieval pipeline for assistant context."""

from __future__ import annotations

from collections.abc import Iterable

from aidk.ai.retrieval.base import ContextRetriever
from aidk.ai.retrieval.models import RetrievedContext


class RetrievalPipeline:
    """Run multiple retrievers and merge their results."""

    def __init__(
        self,
        retrievers: Iterable[ContextRetriever],
    ) -> None:
        self.retrievers = list(retrievers)

    def retrieve(
        self,
        question: str,
    ) -> RetrievedContext:
        merged = RetrievedContext(
            question=question.strip()
        )

        entity_keys: set[str] = set()
        code_keys: set[str] = set()

        for retriever in self.retrievers:
            context = retriever.retrieve(question)

            merged.statistics.update(context.statistics)
            merged.metadata.update(context.metadata)

            for entity in context.matched_entities:
                key = str(
                    entity.get("id")
                    or entity.get("path")
                    or entity.get("name")
                    or repr(entity)
                )

                if key not in entity_keys:
                    entity_keys.add(key)
                    merged.matched_entities.append(entity)

            for match in context.code_matches:
                key = str(match.get("path") or repr(match))

                if key not in code_keys:
                    code_keys.add(key)
                    merged.code_matches.append(match)

        merged.code_matches.sort(
            key=lambda item: int(item.get("score", 0)),
            reverse=True,
        )

        return merged
