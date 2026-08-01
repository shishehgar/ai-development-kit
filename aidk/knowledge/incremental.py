"""Incremental knowledge graph indexing."""

from __future__ import annotations


from pathlib import Path


from aidk.knowledge.graph import (
    KnowledgeGraph,
)


from aidk.knowledge.git_changes import (
    GitChangeDetector,
)


from aidk.knowledge.scanner import (
    KnowledgeScanner,
)


from aidk.knowledge.store import (
    KnowledgeGraphStore,
)



class IncrementalIndexer:
    """
    Incrementally update project knowledge.

    Workflow:

        Git Changes
              |
              v
        Scan changed files
              |
              v
        Merge graph
              |
              v
        Persist
    """



    def __init__(
        self,
        root: str | Path,
    ) -> None:


        self.root = Path(root)


        self.scanner = (
            KnowledgeScanner()
        )


        self.git = (
            GitChangeDetector(
                self.root
            )
        )


        self.store = (
            KnowledgeGraphStore()
        )



    def reindex(
        self,
        project: str,
    ) -> dict:


        changes = (
            self.git.detect()
        )


        graph = (
            self.store.load(
                project
            )
        )


        removed = 0


        #
        # Remove deleted files
        #
        for deleted in changes.deleted:

            removed += (
                self._remove_file(
                    graph,
                    deleted,
                )
            )



        #
        # Scan changed files
        #
        changed_files = (
            changes.added
            +
            changes.modified
        )


        updated_graph = (
            self.scanner.scan_files(
                changed_files
            )
        )


        #
        # Merge entities
        #
        for entity in (
            updated_graph.entities()
        ):

            graph.add_entity(
                entity
            )



        #
        # Merge relations
        #
        for relation in (
            updated_graph.relations()
        ):

            graph.add_relation(
                relation
            )



        self.store.save(
            project,
            graph,
        )


        return {

            "project": project,

            "added_files":
                len(changes.added),

            "modified_files":
                len(changes.modified),

            "deleted_files":
                len(changes.deleted),

            "removed_entities":
                removed,

            "entities":
                len(graph.entities()),

            "relations":
                len(graph.relations()),

        }



    def _remove_file(
        self,
        graph: KnowledgeGraph,
        path: Path,
    ) -> int:
        """
        Remove entities belonging to file.
        """

        removed = 0


        for entity in list(
            graph.entities()
        ):

            if entity.path:

                if Path(entity.path) == path:

                    if graph.remove_entity(
                        entity.id
                    ):

                        removed += 1


        return removed
