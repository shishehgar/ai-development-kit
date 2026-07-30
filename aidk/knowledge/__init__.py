"""Knowledge-domain primitives for AIDK."""

from aidk.knowledge.entities import (
    KnowledgeEntity,
    KnowledgeRelation,
    ModuleEntity,
    ProjectEntity,
    SourceFileEntity,
    SymbolEntity,
)
from aidk.knowledge.types import (
    EntityKind,
    Language,
    RelationKind,
    Visibility,
)
from aidk.knowledge.graph import (
    KnowledgeGraph,
    KnowledgeGraphError,
    EntityNotFoundError,
)
from aidk.knowledge.repository import (
    KnowledgeRepository,
)
from aidk.knowledge.serializers import (
    save_snapshot,
    load_snapshot,
)
from aidk.knowledge.scanner import (
    KnowledgeScanner,
)
from aidk.knowledge.impact import (
    ImpactAnalyzer,
    ImpactReport,
)
from aidk.knowledge.query import (
    KnowledgeQueryService,
)


__all__ = [
    "EntityKind",
    "KnowledgeEntity",
    "KnowledgeRelation",
    "Language",
    "ModuleEntity",
    "ProjectEntity",
    "RelationKind",
    "SourceFileEntity",
    "SymbolEntity",
    "Visibility",
    "KnowledgeGraph",
    "KnowledgeGraphError",
    "EntityNotFoundError",
    "KnowledgeRepository",
    "save_snapshot",
    "load_snapshot",
    "KnowledgeScanner",
    "ImpactAnalyzer",
    "ImpactReport",
    "KnowledgeQueryService",
]
