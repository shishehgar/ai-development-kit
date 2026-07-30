"""Core entities for the AIDK knowledge graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from aidk.knowledge.types import (
    EntityKind,
    Language,
    RelationKind,
    Visibility,
)


Metadata = dict[str, Any]


def normalize_path(
    value: str | Path | None,
) -> str | None:
    """Normalize a filesystem path for stable serialization."""

    if value is None:
        return None

    return Path(value).as_posix()


@dataclass(slots=True)
class KnowledgeEntity:
    """Base node stored in the knowledge graph."""

    kind: EntityKind
    name: str
    entity_id: UUID = field(
        default_factory=uuid4
    )
    qualified_name: str | None = None
    path: str | None = None
    metadata: Metadata = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        self.name = self.name.strip()

        if not self.name:
            raise ValueError(
                "Knowledge entity name cannot be empty."
            )

        self.path = normalize_path(
            self.path
        )

        if self.qualified_name is not None:
            self.qualified_name = (
                self.qualified_name.strip()
                or None
            )

    @property
    def id(self) -> UUID:
        """Compatibility alias for entity_id."""

        return self.entity_id

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible representation."""

        return {
            "id": str(self.entity_id),
            "kind": self.kind.value,
            "name": self.name,
            "qualified_name": self.qualified_name,
            "path": self.path,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class ProjectEntity(KnowledgeEntity):
    """Root node representing a software project."""

    root_path: str = "."
    description: str | None = None

    def __init__(
        self,
        *,
        name: str,
        root_path: str | Path,
        description: str | None = None,
        entity_id: UUID | None = None,
        metadata: Metadata | None = None,
    ) -> None:
        normalized_root = (
            normalize_path(root_path)
            or "."
        )

        KnowledgeEntity.__init__(
            self,
            kind=EntityKind.PROJECT,
            name=name,
            entity_id=entity_id or uuid4(),
            qualified_name=name,
            path=normalized_root,
            metadata=metadata or {},
        )

        self.root_path = normalized_root
        self.description = description

    def to_dict(self) -> dict[str, Any]:
        payload = super().to_dict()

        payload.update(
            {
                "root_path": self.root_path,
                "description": self.description,
            }
        )

        return payload


@dataclass(slots=True)
class ModuleEntity(KnowledgeEntity):
    """Node representing a source-code module."""

    language: Language = Language.UNKNOWN

    def __init__(
        self,
        *,
        name: str,
        path: str | Path,
        qualified_name: str | None = None,
        language: Language = Language.UNKNOWN,
        entity_id: UUID | None = None,
        metadata: Metadata | None = None,
    ) -> None:
        KnowledgeEntity.__init__(
            self,
            kind=EntityKind.MODULE,
            name=name,
            entity_id=entity_id or uuid4(),
            qualified_name=qualified_name,
            path=normalize_path(path),
            metadata=metadata or {},
        )

        self.language = language

    def to_dict(self) -> dict[str, Any]:
        payload = super().to_dict()
        payload["language"] = self.language.value
        return payload


@dataclass(slots=True)
class SourceFileEntity(KnowledgeEntity):
    """Node representing a source or configuration file."""

    language: Language = Language.UNKNOWN
    content_hash: str | None = None
    size_bytes: int = 0

    def __init__(
        self,
        *,
        name: str,
        path: str | Path,
        language: Language = Language.UNKNOWN,
        content_hash: str | None = None,
        size_bytes: int = 0,
        entity_id: UUID | None = None,
        metadata: Metadata | None = None,
    ) -> None:
        if size_bytes < 0:
            raise ValueError(
                "size_bytes cannot be negative."
            )

        KnowledgeEntity.__init__(
            self,
            kind=EntityKind.SOURCE_FILE,
            name=name,
            entity_id=entity_id or uuid4(),
            qualified_name=None,
            path=normalize_path(path),
            metadata=metadata or {},
        )

        self.language = language
        self.content_hash = content_hash
        self.size_bytes = size_bytes

    def to_dict(self) -> dict[str, Any]:
        payload = super().to_dict()

        payload.update(
            {
                "language": self.language.value,
                "content_hash": self.content_hash,
                "size_bytes": self.size_bytes,
            }
        )

        return payload


@dataclass(slots=True)
class SymbolEntity(KnowledgeEntity):
    """Node representing a class, function or other symbol."""

    language: Language = Language.UNKNOWN
    visibility: Visibility = Visibility.UNKNOWN
    line_start: int | None = None
    line_end: int | None = None
    signature: str | None = None
    docstring: str | None = None

    def __init__(
        self,
        *,
        kind: EntityKind,
        name: str,
        path: str | Path,
        qualified_name: str | None = None,
        language: Language = Language.UNKNOWN,
        visibility: Visibility = Visibility.UNKNOWN,
        line_start: int | None = None,
        line_end: int | None = None,
        signature: str | None = None,
        docstring: str | None = None,
        entity_id: UUID | None = None,
        metadata: Metadata | None = None,
    ) -> None:
        allowed_kinds = {
            EntityKind.CLASS,
            EntityKind.FUNCTION,
            EntityKind.METHOD,
            EntityKind.PROPERTY,
            EntityKind.VARIABLE,
            EntityKind.CONSTANT,
            EntityKind.ENUM,
            EntityKind.INTERFACE,
            EntityKind.PARAMETER,
            EntityKind.TEST,
            EntityKind.API,
            EntityKind.COMMAND,
            EntityKind.SERVICE,
            EntityKind.ENGINE,
            EntityKind.PLUGIN,
        }

        if kind not in allowed_kinds:
            raise ValueError(
                f"Invalid symbol entity kind: {kind.value}"
            )

        if line_start is not None and line_start < 1:
            raise ValueError(
                "line_start must be greater than zero."
            )

        if line_end is not None and line_end < 1:
            raise ValueError(
                "line_end must be greater than zero."
            )

        if (
            line_start is not None
            and line_end is not None
            and line_end < line_start
        ):
            raise ValueError(
                "line_end cannot be before line_start."
            )

        KnowledgeEntity.__init__(
            self,
            kind=kind,
            name=name,
            entity_id=entity_id or uuid4(),
            qualified_name=qualified_name,
            path=normalize_path(path),
            metadata=metadata or {},
        )

        self.language = language
        self.visibility = visibility
        self.line_start = line_start
        self.line_end = line_end
        self.signature = signature
        self.docstring = docstring

    def to_dict(self) -> dict[str, Any]:
        payload = super().to_dict()

        payload.update(
            {
                "language": self.language.value,
                "visibility": self.visibility.value,
                "line_start": self.line_start,
                "line_end": self.line_end,
                "signature": self.signature,
                "docstring": self.docstring,
            }
        )

        return payload


@dataclass(slots=True)
class KnowledgeRelation:
    """Directed edge between two knowledge entities."""

    source_id: UUID
    target_id: UUID
    kind: RelationKind
    relation_id: UUID = field(
        default_factory=uuid4
    )
    metadata: Metadata = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        if self.source_id == self.target_id:
            self.metadata.setdefault(
                "self_reference",
                True,
            )

    @property
    def id(self) -> UUID:
        return self.relation_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": str(self.relation_id),
            "source_id": str(self.source_id),
            "target_id": str(self.target_id),
            "kind": self.kind.value,
            "metadata": dict(self.metadata),
        }
