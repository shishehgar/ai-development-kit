"""In-memory knowledge graph engine."""

from __future__ import annotations

from collections import defaultdict
from threading import RLock
from typing import Iterable
from uuid import UUID

from aidk.knowledge.entities import (
    KnowledgeEntity,
    KnowledgeRelation,
)
from aidk.knowledge.types import (
    EntityKind,
    RelationKind,
)


class KnowledgeGraphError(RuntimeError):
    """Base knowledge graph error."""


class EntityNotFoundError(
    KnowledgeGraphError
):
    """Raised when an entity does not exist."""


class KnowledgeGraph:
    """
    In-memory directed knowledge graph.

    Stores:

    Nodes:
        KnowledgeEntity

    Edges:
        KnowledgeRelation
    """

    def __init__(self) -> None:

        self._entities: dict[
            UUID,
            KnowledgeEntity,
        ] = {}

        self._relations: dict[
            UUID,
            KnowledgeRelation,
        ] = {}

        self._outgoing: dict[
            UUID,
            set[UUID],
        ] = defaultdict(set)

        self._incoming: dict[
            UUID,
            set[UUID],
        ] = defaultdict(set)

        self._lock = RLock()


    def add_entity(
        self,
        entity: KnowledgeEntity,
    ) -> KnowledgeEntity:
        """
        Add or replace an entity.
        """

        with self._lock:
            self._entities[
                entity.id
            ] = entity

        return entity


    def add_entities(
        self,
        entities: Iterable[
            KnowledgeEntity
        ],
    ) -> None:
        """
        Add multiple entities.
        """

        for entity in entities:
            self.add_entity(entity)


    def get_entity(
        self,
        entity_id: UUID,
    ) -> KnowledgeEntity:

        with self._lock:

            entity = (
                self._entities.get(
                    entity_id
                )
            )

        if entity is None:
            raise EntityNotFoundError(
                f"Entity not found: {entity_id}"
            )

        return entity


    def remove_entity(
        self,
        entity_id: UUID,
    ) -> bool:
        """
        Remove entity and all relations.
        """

        with self._lock:

            if entity_id not in self._entities:
                return False


            relations = (
                self._outgoing.pop(
                    entity_id,
                    set(),
                )
                |
                self._incoming.pop(
                    entity_id,
                    set(),
                )
            )


            for relation_id in relations:
                self.remove_relation(
                    relation_id
                )


            del self._entities[
                entity_id
            ]


        return True


    def add_relation(
        self,
        relation: KnowledgeRelation,
    ) -> KnowledgeRelation:
        """
        Add graph edge.
        """

        self.get_entity(
            relation.source_id
        )

        self.get_entity(
            relation.target_id
        )


        with self._lock:

            self._relations[
                relation.id
            ] = relation


            self._outgoing[
                relation.source_id
            ].add(
                relation.id
            )


            self._incoming[
                relation.target_id
            ].add(
                relation.id
            )


        return relation



    def remove_relation(
        self,
        relation_id: UUID,
    ) -> bool:

        with self._lock:

            relation = (
                self._relations.pop(
                    relation_id,
                    None,
                )
            )


            if relation is None:
                return False


            self._outgoing[
                relation.source_id
            ].discard(
                relation_id
            )


            self._incoming[
                relation.target_id
            ].discard(
                relation_id
            )


        return True



    def get_relation(
        self,
        relation_id: UUID,
    ) -> KnowledgeRelation:

        with self._lock:

            relation = (
                self._relations.get(
                    relation_id
                )
            )

        if relation is None:
            raise KnowledgeGraphError(
                f"Relation not found: {relation_id}"
            )

        return relation



    def find_by_name(
        self,
        name: str,
    ) -> list[KnowledgeEntity]:

        normalized = name.lower()

        with self._lock:

            return [
                entity
                for entity
                in self._entities.values()
                if entity.name.lower()
                == normalized
            ]



    def find_by_kind(
        self,
        kind: EntityKind,
    ) -> list[KnowledgeEntity]:

        with self._lock:

            return [
                entity
                for entity
                in self._entities.values()
                if entity.kind is kind
            ]



    def neighbors(
        self,
        entity_id: UUID,
        relation_kind: RelationKind | None = None,
    ) -> list[KnowledgeEntity]:
        """
        Return outgoing connected entities.
        """

        with self._lock:

            relation_ids = (
                self._outgoing.get(
                    entity_id,
                    set(),
                )
            )

            result = []

            for relation_id in relation_ids:

                relation = (
                    self._relations[
                        relation_id
                    ]
                )

                if (
                    relation_kind
                    and relation.kind
                    is not relation_kind
                ):
                    continue


                result.append(
                    self._entities[
                        relation.target_id
                    ]
                )


        return result



    def incoming(
        self,
        entity_id: UUID,
        relation_kind: RelationKind | None = None,
    ) -> list[KnowledgeEntity]:

        with self._lock:

            relation_ids = (
                self._incoming.get(
                    entity_id,
                    set(),
                )
            )

            result = []

            for relation_id in relation_ids:

                relation = (
                    self._relations[
                        relation_id
                    ]
                )

                if (
                    relation_kind
                    and relation.kind
                    is not relation_kind
                ):
                    continue


                result.append(
                    self._entities[
                        relation.source_id
                    ]
                )


        return result



    def statistics(
        self,
    ) -> dict[str, int]:

        with self._lock:

            entities = (
                list(
                    self._entities.values()
                )
            )

            relations = (
                list(
                    self._relations.values()
                )
            )


        return {
            "entities": len(
                entities
            ),
            "relations": len(
                relations
            ),
            "projects": sum(
                1
                for item
                in entities
                if item.kind
                is EntityKind.PROJECT
            ),
            "modules": sum(
                1
                for item
                in entities
                if item.kind
                is EntityKind.MODULE
            ),
            "symbols": sum(
                1
                for item
                in entities
                if item.kind
                in {
                    EntityKind.CLASS,
                    EntityKind.FUNCTION,
                    EntityKind.METHOD,
                }
            ),
        }


    def clear(self) -> None:

        with self._lock:
            self._entities.clear()
            self._relations.clear()
            self._outgoing.clear()
            self._incoming.clear()


    def __len__(self) -> int:

        with self._lock:
            return len(
                self._entities
            )


    def entities(
        self,
    ) -> list[KnowledgeEntity]:
        """
        Return all graph entities.

        Public read API.
        """

        with self._lock:

            return list(
                self._entities.values()
            )



    def relations(
        self,
    ) -> list[KnowledgeRelation]:
        """
        Return all graph relations.

        Public read API.
        """

        with self._lock:

            return list(
                self._relations.values()
            )
