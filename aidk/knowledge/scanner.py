"""Knowledge scanner engine."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from aidk.knowledge.analyzers.files import (
    detect_language,
    iter_source_files,
)
from aidk.knowledge.analyzers.python import (
    PythonAnalyzer,
)
from aidk.knowledge.dependency import (
    DependencyAnalyzer,
)
from aidk.knowledge.entities import (
    ModuleEntity,
)
from aidk.knowledge.graph import (
    KnowledgeGraph,
)
from aidk.knowledge.identity import (
    stable_entity_id,
)
from aidk.knowledge.types import (
    EntityKind,
)


class KnowledgeScanner:
    """
    Build project-aware knowledge graphs.

    Supports:
        - full project scans
        - partial incremental scans
        - stable source, module and symbol identities
    """

    def __init__(self) -> None:
        self.python = PythonAnalyzer()
        self.dependencies = DependencyAnalyzer()

    def scan(
        self,
        root: str | Path,
        *,
        project: str | None = None,
    ) -> KnowledgeGraph:
        """Perform a full project scan."""

        resolved_root = Path(
            root
        ).resolve()

        project_id = (
            project.strip()
            if project and project.strip()
            else resolved_root.name
        )

        return self.scan_files(
            iter_source_files(
                resolved_root
            ),
            project=project_id,
            root=resolved_root,
        )

    def scan_files(
        self,
        files: Iterable[str | Path],
        *,
        project: str = "unknown",
        root: str | Path | None = None,
    ) -> KnowledgeGraph:
        """Scan selected files using stable project-relative identities."""

        project_id = (
            project.strip()
            or "unknown"
        )

        resolved_root = (
            Path(root).resolve()
            if root is not None
            else None
        )

        graph = KnowledgeGraph()

        for item in files:
            file_path = Path(
                item
            ).resolve()

            if (
                not file_path.exists()
                or not file_path.is_file()
            ):
                continue

            identity_path = (
                self._identity_path(
                    file_path,
                    resolved_root,
                )
            )

            language = detect_language(
                file_path
            )

            if language.value == "python":
                file_entity = (
                    self.python.analyze_file(
                        file_path,
                        project=project_id,
                        identity_path=identity_path,
                    )
                )

                graph.add_entity(
                    file_entity
                )

                symbols = (
                    self.python.analyze(
                        file_path,
                        project=project_id,
                        identity_path=identity_path,
                    )
                )

                graph.add_entities(
                    symbols
                )

            module = ModuleEntity(
                entity_id=stable_entity_id(
                    project=project_id,
                    kind=EntityKind.MODULE.value,
                    path=identity_path,
                    qualified_name=(
                        self._module_name(
                            identity_path
                        )
                    ),
                    name=file_path.stem,
                ),
                name=file_path.stem,
                qualified_name=(
                    self._module_name(
                        identity_path
                    )
                ),
                path=file_path,
                language=language,
                metadata={
                    "identity_path":
                        identity_path,
                    "project":
                        project_id,
                },
            )

            graph.add_entity(
                module
            )

        for source_file in list(
            graph.find_by_kind(
                EntityKind.SOURCE_FILE
            )
        ):
            self.dependencies.analyze_file(
                graph,
                source_file,
            )

        return graph

    @staticmethod
    def _identity_path(
        file_path: Path,
        root: Path | None,
    ) -> str:
        """Return a deployment-independent logical file path."""

        if root is not None:
            try:
                return (
                    file_path.relative_to(root)
                    .as_posix()
                )
            except ValueError:
                pass

        return file_path.as_posix()

    @staticmethod
    def _module_name(
        identity_path: str,
    ) -> str:
        """Convert a logical file path to a dotted module name."""

        path = Path(
            identity_path
        )

        without_suffix = path.with_suffix("")

        parts = list(
            without_suffix.parts
        )

        if (
            parts
            and parts[-1] == "__init__"
        ):
            parts.pop()

        return ".".join(parts)
