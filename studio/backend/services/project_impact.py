"""Project-scoped impact analysis service."""

from __future__ import annotations

from uuid import UUID

from aidk.knowledge.impact import (
    ImpactAnalyzer,
)
from studio.backend.services.project_context import (
    project_context_resolver,
)
from studio.backend.services.project_registry import (
    project_registry,
)


class ProjectNotFoundError(LookupError):
    """Raised when a project is not registered."""


class ImpactEntityNotFoundError(LookupError):
    """Raised when an impact target cannot be found."""


class AmbiguousImpactEntityError(ValueError):
    """Raised when a name resolves to multiple entities."""

    def __init__(
        self,
        name: str,
        candidates: list[dict[str, object]],
    ) -> None:
        self.name = name
        self.candidates = candidates

        super().__init__(
            f"Multiple entities matched {name!r}."
        )


class ProjectImpactService:
    """Execute impact analysis against a project graph."""

    def __init__(self) -> None:
        self.analyzer = ImpactAnalyzer()

    def analyze(
        self,
        project_id: str,
        entity_reference: str,
    ) -> dict[str, object]:
        """Analyze an entity identified by UUID or name."""

        project = project_registry.get(
            project_id
        )

        if project is None:
            raise ProjectNotFoundError(
                f"Unknown project: {project_id}"
            )

        graph = project_context_resolver.resolve(
            project_id
        )

        entity_id = self._resolve_entity_id(
            graph,
            entity_reference,
        )

        report = self.analyzer.analyze(
            graph,
            entity_id,
        )

        result = report.to_dict()

        result["project"] = project_id
        result["graph_statistics"] = (
            graph.statistics()
        )

        return result

    def _resolve_entity_id(
        self,
        graph,
        entity_reference: str,
    ) -> UUID:
        normalized = entity_reference.strip()

        if not normalized:
            raise ImpactEntityNotFoundError(
                "Impact entity reference cannot be empty."
            )

        try:
            entity_id = UUID(
                normalized
            )

            graph.get_entity(
                entity_id
            )

            return entity_id

        except ValueError:
            pass

        except Exception as exc:
            raise ImpactEntityNotFoundError(
                f"Entity not found: {normalized}"
            ) from exc

        matches = graph.find_by_name(
            normalized
        )

        if not matches:
            raise ImpactEntityNotFoundError(
                f"Entity not found: {normalized}"
            )

        if len(matches) > 1:
            raise AmbiguousImpactEntityError(
                normalized,
                [
                    {
                        "id": str(item.id),
                        "name": item.name,
                        "qualified_name": (
                            item.qualified_name
                        ),
                        "kind": item.kind.value,
                        "path": item.path,
                    }
                    for item in matches[:50]
                ],
            )

        return matches[0].id


project_impact_service = (
    ProjectImpactService()
)
