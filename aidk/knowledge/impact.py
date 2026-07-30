"""Impact analysis engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from aidk.knowledge.graph import (
    KnowledgeGraph,
)

from aidk.knowledge.types import (
    EntityKind,
    RelationKind,
)


@dataclass(slots=True)
class ImpactReport:
    """Result of impact analysis."""

    target_id: UUID

    affected_entities: list = field(
        default_factory=list
    )

    affected_files: int = 0

    affected_modules: int = 0

    affected_tests: int = 0

    risk: str = "LOW"

    def calculate_risk(self) -> None:
        """
        Calculate change risk.
        """

        score = (
            self.affected_files
            +
            self.affected_modules * 2
            +
            self.affected_tests
        )


        if score >= 15:
            self.risk = "HIGH"

        elif score >= 5:
            self.risk = "MEDIUM"

        else:
            self.risk = "LOW"



class ImpactAnalyzer:
    """
    Analyze graph dependency impact.
    """

    def analyze(
        self,
        graph: KnowledgeGraph,
        entity_id: UUID,
    ) -> ImpactReport:


        target = graph.get_entity(
            entity_id
        )


        report = ImpactReport(
            target_id=entity_id
        )


        visited = set()


        def walk(
            current_id: UUID,
        ):

            if current_id in visited:
                return

            visited.add(
                current_id
            )


            parents = graph.incoming(
                current_id,
                RelationKind.IMPORTS,
            )


            for parent in parents:

                report.affected_entities.append(
                    parent
                )

                walk(
                    parent.id
                )


        walk(
            entity_id
        )


        report.affected_files = sum(
            1
            for item
            in report.affected_entities
            if item.kind
            is EntityKind.SOURCE_FILE
        )


        report.affected_modules = sum(
            1
            for item
            in report.affected_entities
            if item.kind
            is EntityKind.MODULE
        )


        report.affected_tests = sum(
            1
            for item
            in report.affected_entities
            if item.kind
            is EntityKind.TEST
        )


        report.calculate_risk()

        return report
