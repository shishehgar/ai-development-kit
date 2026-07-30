"""Runtime knowledge service."""

from __future__ import annotations

from pathlib import Path
from threading import RLock

from aidk.knowledge import (
    KnowledgeGraph,
    KnowledgeQueryService,
    KnowledgeScanner,
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

        return self.graph.statistics()



    def summary(self):

        with self._lock:

            return self.graph.statistics()



knowledge_runtime = KnowledgeRuntime()
