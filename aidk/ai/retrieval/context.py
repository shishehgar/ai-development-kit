"""Knowledge-graph context retrieval for the AIDK assistant."""

from __future__ import annotations

import re

from aidk.ai.retrieval.models import RetrievedContext
from aidk.knowledge.graph import KnowledgeGraph


_TOKEN_PATTERN = re.compile(
    r"[A-Za-z_][A-Za-z0-9_.-]*"
)


class GraphContextRetriever:
    """Retrieve relevant entities from a KnowledgeGraph."""

    def __init__(
        self,
        graph: KnowledgeGraph,
    ) -> None:
        self.graph = graph

    def retrieve(
        self,
        question: str,
    ) -> RetrievedContext:
        normalized = question.strip()
        matched_entities: list[dict[str, object]] = []
        seen_entities: set[str] = set()

        for token in self._tokens(normalized):
            for entity in self.graph.find_by_name(token):
                item = entity.to_dict()

                identity = str(
                    item.get("id")
                    or item.get("path")
                    or item.get("name")
                    or repr(item)
                )

                if identity in seen_entities:
                    continue

                seen_entities.add(identity)
                matched_entities.append(item)

        return RetrievedContext(
            question=normalized,
            statistics=self.graph.statistics(),
            matched_entities=matched_entities,
        )

    @staticmethod
    def _tokens(
        question: str,
    ) -> list[str]:
        tokens = _TOKEN_PATTERN.findall(question)

        unique_tokens: list[str] = []
        seen_tokens: set[str] = set()

        for token in tokens:
            key = token.casefold()

            if key in seen_tokens:
                continue

            seen_tokens.add(key)
            unique_tokens.append(token)

        return unique_tokens
