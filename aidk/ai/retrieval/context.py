"""Knowledge context retrieval for the AIDK assistant."""

from __future__ import annotations

from dataclasses import dataclass, field

from aidk.knowledge.graph import KnowledgeGraph


@dataclass(slots=True)
class RetrievedContext:
    """Structured project context returned for a user question."""

    question: str
    statistics: dict[str, int]
    matched_entities: list[dict[str, object]] = field(
        default_factory=list
    )


class GraphContextRetriever:
    """Retrieve relevant context from a KnowledgeGraph."""

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

        if normalized:
            for token in normalized.split():
                matches = self.graph.find_by_name(
                    token
                )

                for entity in matches:
                    item = entity.to_dict()

                    if item not in matched_entities:
                        matched_entities.append(item)

        return RetrievedContext(
            question=normalized,
            statistics=self.graph.statistics(),
            matched_entities=matched_entities,
        )
