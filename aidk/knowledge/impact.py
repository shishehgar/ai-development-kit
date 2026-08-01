"""Dependency impact analysis engine."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from uuid import UUID

from aidk.knowledge.entities import (
    KnowledgeEntity,
)
from aidk.knowledge.graph import (
    KnowledgeGraph,
)
from aidk.knowledge.types import (
    EntityKind,
    RelationKind,
)


DEFAULT_IMPACT_RELATIONS: tuple[
    RelationKind,
    ...,
] = (
    RelationKind.IMPORTS,
    RelationKind.DEPENDS_ON,
    RelationKind.USES,
    RelationKind.CALLS,
    RelationKind.REFERENCES,
    RelationKind.INHERITS,
    RelationKind.IMPLEMENTS,
    RelationKind.EXPOSES,
    RelationKind.REGISTERS,
    RelationKind.TESTS,
)


@dataclass(slots=True)
class ImpactedEntity:
    """Entity affected by a target change."""

    entity: KnowledgeEntity
    depth: int
    relation_kinds: set[RelationKind] = field(
        default_factory=set
    )

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible representation."""

        return {
            "id": str(self.entity.id),
            "name": self.entity.name,
            "qualified_name": (
                self.entity.qualified_name
            ),
            "kind": self.entity.kind.value,
            "path": self.entity.path,
            "depth": self.depth,
            "relation_kinds": sorted(
                relation.value
                for relation
                in self.relation_kinds
            ),
        }


@dataclass(slots=True)
class ImpactReport:
    """Result of dependency impact analysis."""

    target_id: UUID
    target_name: str
    target_kind: EntityKind
    target_path: str | None
    affected_entities: list[
        ImpactedEntity
    ] = field(default_factory=list)
    affected_files: int = 0
    affected_modules: int = 0
    affected_tests: int = 0
    maximum_depth: int = 0
    risk_score: int = 0
    risk: str = "LOW"

    def calculate_risk(self) -> None:
        """Calculate a normalized change-risk category."""

        direct_impacts = sum(
            1
            for item in self.affected_entities
            if item.depth == 1
        )

        indirect_impacts = (
            len(self.affected_entities)
            - direct_impacts
        )

        self.risk_score = (
            direct_impacts * 3
            + indirect_impacts
            + self.affected_files * 2
            + self.affected_modules * 2
            + self.affected_tests * 3
            + self.maximum_depth
        )

        if self.risk_score >= 40:
            self.risk = "CRITICAL"
        elif self.risk_score >= 20:
            self.risk = "HIGH"
        elif self.risk_score >= 8:
            self.risk = "MEDIUM"
        else:
            self.risk = "LOW"

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible impact report."""

        return {
            "target": {
                "id": str(self.target_id),
                "name": self.target_name,
                "kind": self.target_kind.value,
                "path": self.target_path,
            },
            "risk": self.risk,
            "risk_score": self.risk_score,
            "affected_count": len(
                self.affected_entities
            ),
            "affected_files": self.affected_files,
            "affected_modules": (
                self.affected_modules
            ),
            "affected_tests": self.affected_tests,
            "maximum_depth": self.maximum_depth,
            "affected_entities": [
                item.to_dict()
                for item in self.affected_entities
            ],
        }


class ImpactAnalyzer:
    """Analyze transitive dependency impact."""

    def __init__(
        self,
        *,
        relation_kinds: tuple[
            RelationKind,
            ...,
        ] = DEFAULT_IMPACT_RELATIONS,
        max_depth: int = 8,
    ) -> None:
        if max_depth < 1:
            raise ValueError(
                "Impact maximum depth must be positive."
            )

        self.relation_kinds = relation_kinds
        self.max_depth = max_depth

    def analyze(
        self,
        graph: KnowledgeGraph,
        entity_id: UUID,
    ) -> ImpactReport:
        """Analyze direct and transitive dependents."""

        target = graph.get_entity(
            entity_id
        )

        report = ImpactReport(
            target_id=target.id,
            target_name=target.name,
            target_kind=target.kind,
            target_path=target.path,
        )

        queue: deque[
            tuple[UUID, int]
        ] = deque(
            [
                (
                    entity_id,
                    0,
                )
            ]
        )

        visited_depth: dict[
            UUID,
            int,
        ] = {
            entity_id: 0,
        }

        impacted: dict[
            UUID,
            ImpactedEntity,
        ] = {}

        while queue:
            current_id, depth = queue.popleft()

            if depth >= self.max_depth:
                continue

            next_depth = depth + 1

            for relation_kind in (
                self.relation_kinds
            ):
                dependents = graph.incoming(
                    current_id,
                    relation_kind,
                )

                for dependent in dependents:
                    if dependent.id == entity_id:
                        continue

                    existing = impacted.get(
                        dependent.id
                    )

                    if existing is None:
                        impacted[
                            dependent.id
                        ] = ImpactedEntity(
                            entity=dependent,
                            depth=next_depth,
                            relation_kinds={
                                relation_kind
                            },
                        )
                    else:
                        existing.relation_kinds.add(
                            relation_kind
                        )

                        if next_depth < existing.depth:
                            existing.depth = next_depth

                    previous_depth = (
                        visited_depth.get(
                            dependent.id
                        )
                    )

                    if (
                        previous_depth is None
                        or next_depth
                        < previous_depth
                    ):
                        visited_depth[
                            dependent.id
                        ] = next_depth

                        queue.append(
                            (
                                dependent.id,
                                next_depth,
                            )
                        )

        report.affected_entities = sorted(
            impacted.values(),
            key=lambda item: (
                item.depth,
                item.entity.kind.value,
                item.entity.qualified_name
                or item.entity.name,
            ),
        )

        report.maximum_depth = max(
            (
                item.depth
                for item
                in report.affected_entities
            ),
            default=0,
        )

        report.affected_files = sum(
            1
            for item in report.affected_entities
            if item.entity.kind
            is EntityKind.SOURCE_FILE
        )

        report.affected_modules = sum(
            1
            for item in report.affected_entities
            if item.entity.kind
            is EntityKind.MODULE
        )

        report.affected_tests = sum(
            1
            for item in report.affected_entities
            if item.entity.kind
            is EntityKind.TEST
        )

        report.calculate_risk()

        return report
