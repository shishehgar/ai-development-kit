"""Knowledge query service."""

from __future__ import annotations

from uuid import UUID

from aidk.knowledge.graph import (
    KnowledgeGraph,
)

from aidk.knowledge.impact import (
    ImpactAnalyzer,
)

from aidk.knowledge.types import (
    EntityKind,
)


class KnowledgeQueryService:
    """
    High level query interface.

    Used by:
        API
        Studio
        AI agents
    """

    def __init__(
        self,
        graph: KnowledgeGraph,
    ) -> None:

        self.graph = graph

        self.impact = (
            ImpactAnalyzer()
        )


    def find(
        self,
        name: str,
    ):

        return (
            self.graph.find_by_name(
                name
            )
        )


    def list_kind(
        self,
        kind: EntityKind,
    ):

        return (
            self.graph.find_by_kind(
                kind
            )
        )


    def dependencies(
        self,
        entity_id: UUID,
    ):

        return (
            self.graph.neighbors(
                entity_id
            )
        )


    def dependents(
        self,
        entity_id: UUID,
    ):

        return (
            self.graph.incoming(
                entity_id
            )
        )


    def impact_report(
        self,
        entity_id: UUID,
    ):

        return (
            self.impact.analyze(
                self.graph,
                entity_id,
            )
        )


    def summary(self):

        return (
            self.graph.statistics()
        )
