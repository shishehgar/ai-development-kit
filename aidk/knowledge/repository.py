"""Persistence layer for AIDK knowledge graph."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from threading import RLock
from typing import Iterable
from uuid import UUID

from aidk.knowledge.entities import (
    KnowledgeEntity,
    KnowledgeRelation,
)


class KnowledgeRepository:
    """
    SQLite persistence for KnowledgeGraph.

    Stores:

    entities
    relations
    """

    def __init__(
        self,
        database: str | Path,
    ) -> None:

        self.database = Path(
            database
        )

        self.database.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._lock = RLock()

        self._initialize()


    def _connect(
        self,
    ) -> sqlite3.Connection:

        connection = sqlite3.connect(
            self.database
        )

        connection.row_factory = (
            sqlite3.Row
        )

        return connection



    def _initialize(
        self,
    ) -> None:

        with self._connect() as db:

            db.executescript(
                """

                CREATE TABLE IF NOT EXISTS
                entities (

                    id TEXT PRIMARY KEY,

                    kind TEXT NOT NULL,

                    name TEXT NOT NULL,

                    qualified_name TEXT,

                    path TEXT,

                    metadata TEXT NOT NULL

                );


                CREATE TABLE IF NOT EXISTS
                relations (

                    id TEXT PRIMARY KEY,

                    source_id TEXT NOT NULL,

                    target_id TEXT NOT NULL,

                    kind TEXT NOT NULL,

                    metadata TEXT NOT NULL

                );

                """
            )


    def save_entity(
        self,
        entity: KnowledgeEntity,
    ) -> None:

        import json

        payload = entity.to_dict()

        with self._lock:

            with self._connect() as db:

                db.execute(
                    """
                    INSERT OR REPLACE INTO entities
                    (
                        id,
                        kind,
                        name,
                        qualified_name,
                        path,
                        metadata
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        payload["id"],
                        payload["kind"],
                        payload["name"],
                        payload["qualified_name"],
                        payload["path"],
                        json.dumps(
                            payload["metadata"]
                        ),
                    ),
                )


    def save_entities(
        self,
        entities: Iterable[
            KnowledgeEntity
        ],
    ) -> None:

        for entity in entities:
            self.save_entity(
                entity
            )



    def save_relation(
        self,
        relation: KnowledgeRelation,
    ) -> None:

        import json

        payload = relation.to_dict()

        with self._lock:

            with self._connect() as db:

                db.execute(
                    """
                    INSERT OR REPLACE INTO relations
                    (
                        id,
                        source_id,
                        target_id,
                        kind,
                        metadata
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        payload["id"],
                        payload["source_id"],
                        payload["target_id"],
                        payload["kind"],
                        json.dumps(
                            payload["metadata"]
                        ),
                    ),
                )



    def save_relations(
        self,
        relations: Iterable[
            KnowledgeRelation
        ],
    ) -> None:

        for relation in relations:
            self.save_relation(
                relation
            )



    def count_entities(
        self,
    ) -> int:

        with self._connect() as db:

            row = db.execute(
                """
                SELECT COUNT(*) AS count
                FROM entities
                """
            ).fetchone()

        return int(
            row["count"]
        )



    def count_relations(
        self,
    ) -> int:

        with self._connect() as db:

            row = db.execute(
                """
                SELECT COUNT(*) AS count
                FROM relations
                """
            ).fetchone()

        return int(
            row["count"]
        )



    def clear(
        self,
    ) -> None:

        with self._connect() as db:

            db.execute(
                "DELETE FROM relations"
            )

            db.execute(
                "DELETE FROM entities"
            )



    def statistics(
        self,
    ) -> dict[str, int]:

        return {

            "entities":
                self.count_entities(),

            "relations":
                self.count_relations(),

        }
