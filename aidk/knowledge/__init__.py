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
]
