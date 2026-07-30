"""Tests for knowledge graph domain entities."""

from __future__ import annotations

from pathlib import Path
from uuid import UUID

import pytest

from aidk.knowledge import (
    EntityKind,
    KnowledgeEntity,
    KnowledgeRelation,
    Language,
    ModuleEntity,
    ProjectEntity,
    RelationKind,
    SourceFileEntity,
    SymbolEntity,
    Visibility,
)


def test_base_entity_requires_name() -> None:
    with pytest.raises(
        ValueError,
        match="name cannot be empty",
    ):
        KnowledgeEntity(
            kind=EntityKind.MODULE,
            name="   ",
        )


def test_project_entity_normalizes_path(
    tmp_path: Path,
) -> None:
    project = ProjectEntity(
        name="ai-development-kit",
        root_path=tmp_path,
        description="AI engineering platform",
    )

    assert project.kind is EntityKind.PROJECT
    assert project.path == (
        tmp_path.as_posix()
    )
    assert project.root_path == (
        tmp_path.as_posix()
    )

    UUID(
        project.to_dict()["id"]
    )


def test_module_entity_serialization() -> None:
    module = ModuleEntity(
        name="application",
        path="aidk/application",
        qualified_name="aidk.application",
        language=Language.PYTHON,
    )

    payload = module.to_dict()

    assert payload["kind"] == "module"
    assert payload["language"] == "python"
    assert payload["qualified_name"] == (
        "aidk.application"
    )


def test_source_file_rejects_negative_size() -> None:
    with pytest.raises(
        ValueError,
        match="cannot be negative",
    ):
        SourceFileEntity(
            name="service.py",
            path="aidk/service.py",
            size_bytes=-1,
        )


def test_symbol_validates_line_range() -> None:
    with pytest.raises(
        ValueError,
        match="cannot be before",
    ):
        SymbolEntity(
            kind=EntityKind.CLASS,
            name="WorkspaceService",
            path="aidk/application/workspace_service.py",
            line_start=30,
            line_end=20,
        )


def test_symbol_serialization() -> None:
    symbol = SymbolEntity(
        kind=EntityKind.SERVICE,
        name="WorkspaceService",
        qualified_name=(
            "aidk.application."
            "workspace_service."
            "WorkspaceService"
        ),
        path=(
            "aidk/application/"
            "workspace_service.py"
        ),
        language=Language.PYTHON,
        visibility=Visibility.PUBLIC,
        line_start=12,
        line_end=80,
        signature=(
            "class WorkspaceService"
        ),
    )

    payload = symbol.to_dict()

    assert payload["kind"] == "service"
    assert payload["language"] == "python"
    assert payload["visibility"] == "public"
    assert payload["line_start"] == 12
    assert payload["line_end"] == 80


def test_symbol_rejects_non_symbol_kind() -> None:
    with pytest.raises(
        ValueError,
        match="Invalid symbol entity kind",
    ):
        SymbolEntity(
            kind=EntityKind.PROJECT,
            name="invalid",
            path=".",
        )


def test_relation_serialization() -> None:
    source = ModuleEntity(
        name="context",
        path="aidk/app/context.py",
        language=Language.PYTHON,
    )

    target = SymbolEntity(
        kind=EntityKind.CLASS,
        name="ApplicationContext",
        path="aidk/app/context.py",
        language=Language.PYTHON,
    )

    relation = KnowledgeRelation(
        source_id=source.id,
        target_id=target.id,
        kind=RelationKind.DEFINES,
        metadata={
            "confidence": 1.0,
        },
    )

    payload = relation.to_dict()

    assert payload["source_id"] == str(
        source.id
    )
    assert payload["target_id"] == str(
        target.id
    )
    assert payload["kind"] == "defines"
    assert payload["metadata"] == {
        "confidence": 1.0,
    }
