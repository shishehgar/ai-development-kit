"""Project-safe incremental knowledge indexing service."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from aidk.knowledge.git_changes import (
    GitChangeDetectionError,
    GitChangeDetector,
    GitChanges,
)
from aidk.knowledge.graph import (
    KnowledgeGraph,
)
from aidk.knowledge.scanner import (
    KnowledgeScanner,
)
from studio.backend.services.project_knowledge import (
    project_knowledge_store,
)
from studio.backend.services.project_registry import (
    project_registry,
)


class ProjectIncrementalError(RuntimeError):
    """Base error for incremental project indexing."""


class IncrementalProjectNotFoundError(
    ProjectIncrementalError
):
    """Raised when a requested project is not registered."""


class ProjectIncrementalService:
    """
    Safely update a project's persistent knowledge graph.

    Strategies:

    no-op:
        No Git changes were detected.

    incremental-add:
        Only new files were detected, so selected files can be
        scanned and merged safely.

    full-refresh:
        Modified, deleted or renamed files were detected. The full
        graph is rebuilt to preserve dependency correctness.
    """

    def __init__(
        self,
        scanner: KnowledgeScanner | None = None,
    ) -> None:
        self.scanner = (
            scanner
            or KnowledgeScanner()
        )

    def reindex(
        self,
        project_id: str,
    ) -> dict[str, Any]:
        """Reindex one registered project."""

        normalized_project_id = (
            project_id.strip()
        )

        if not normalized_project_id:
            raise IncrementalProjectNotFoundError(
                "Project identifier cannot be empty."
            )

        project = project_registry.get(
            normalized_project_id
        )

        if project is None:
            raise IncrementalProjectNotFoundError(
                f"Unknown project: {normalized_project_id}"
            )

        root = Path(
            project.path
        ).resolve()

        if not root.is_dir():
            raise ProjectIncrementalError(
                f"Project path does not exist: {root}"
            )

        try:
            changes = GitChangeDetector(
                root
            ).detect()
        except GitChangeDetectionError as exc:
            raise ProjectIncrementalError(
                f"Git change detection failed: {exc}"
            ) from exc

        if changes.change_count == 0:
            graph = (
                project_knowledge_store
                .get_or_create(
                    normalized_project_id
                )
            )

            return self._build_result(
                project_id=normalized_project_id,
                strategy="no-op",
                reason=(
                    "No Git changes were detected."
                ),
                changes=changes,
                graph=graph,
            )

        if changes.requires_full_refresh:
            graph = self.scanner.scan(
                root
            )

            project_knowledge_store.save(
                normalized_project_id,
                graph,
            )

            return self._build_result(
                project_id=normalized_project_id,
                strategy="full-refresh",
                reason=(
                    "Modified, deleted or renamed files "
                    "require dependency-safe full indexing."
                ),
                changes=changes,
                graph=graph,
            )

        graph = (
            project_knowledge_store
            .get_or_create(
                normalized_project_id
            )
        )

        added_files = [
            path
            for path in changes.added
            if path.is_file()
        ]

        partial_graph = (
            self.scanner.scan_files(
                added_files,
                project=normalized_project_id,
                root=root,
            )
        )

        graph.add_entities(
            partial_graph.entities()
        )

        for relation in (
            partial_graph.relations()
        ):
            graph.add_relation(
                relation
            )

        project_knowledge_store.save(
            normalized_project_id,
            graph,
        )

        return self._build_result(
            project_id=normalized_project_id,
            strategy="incremental-add",
            reason=(
                "Only newly added files were detected; "
                "partial indexing was applied."
            ),
            changes=changes,
            graph=graph,
        )

    @staticmethod
    def _build_result(
        *,
        project_id: str,
        strategy: str,
        reason: str,
        changes: GitChanges,
        graph: KnowledgeGraph,
    ) -> dict[str, Any]:
        """Build a JSON-compatible reindex result."""

        return {
            "project": project_id,
            "strategy": strategy,
            "reason": reason,
            "changed_files": (
                changes.change_count
            ),
            "added_files": len(
                changes.added
            ),
            "modified_files": len(
                changes.modified
            ),
            "deleted_files": len(
                changes.deleted
            ),
            "renamed_files": len(
                changes.renamed
            ),
            "entities": len(
                graph.entities()
            ),
            "relations": len(
                graph.relations()
            ),
        }


project_incremental_service = (
    ProjectIncrementalService()
)

