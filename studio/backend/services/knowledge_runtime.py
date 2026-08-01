"""Runtime knowledge service."""

from __future__ import annotations

from pathlib import Path
from threading import RLock

from aidk.knowledge import (
    KnowledgeGraph,
    KnowledgeQueryService,
    KnowledgeScanner,
    save_snapshot,
    load_snapshot,
    graph_from_snapshot,
)


class KnowledgeRuntime:
    """
    Keeps project knowledge graph
    available for Studio.
    """

    def __init__(self) -> None:

        self._lock = RLock()

        self.graph = KnowledgeGraph()

        self.query = KnowledgeQueryService(
            self.graph
        )

        self.scanner = KnowledgeScanner()

        self.snapshot_path = (
            Path(".aidk")
            / "knowledge"
            / "snapshot.json"
        )

        self._load_snapshot()



    def _load_snapshot(
        self,
    ) -> None:

        if not self.snapshot_path.exists():
            return


        payload = load_snapshot(
            self.snapshot_path
        )


        self.graph = graph_from_snapshot(
            payload
        )


        self.query = (
            KnowledgeQueryService(
                self.graph
            )
        )


    def save_snapshot(
        self,
    ) -> None:

        payload = {

            "entities": [
                entity.to_dict()
                for entity in self.graph.entities()
            ],

            "relations": [
                relation.to_dict()
                for relation in self.graph.relations()
            ],

        }


        save_snapshot(
            self.snapshot_path,
            payload,
        )




    def scan_project(
        self,
        path: str | Path,
    ):

        with self._lock:

            self.graph = (
                self.scanner.scan(
                    Path(path)
                )
            )

            self.query = (
                KnowledgeQueryService(
                    self.graph
                )
            )

        self.save_snapshot()

        return self.graph.statistics()



    def summary(self):

        with self._lock:

            return self.graph.statistics()



knowledge_runtime = KnowledgeRuntime()
