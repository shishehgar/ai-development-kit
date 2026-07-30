"""Tests for knowledge persistence."""

from pathlib import Path

from aidk.knowledge import (
    KnowledgeRepository,
    ProjectEntity,
    ModuleEntity,
    Language,
    KnowledgeRelation,
    RelationKind,
)


def test_repository_save_entity(
    tmp_path: Path,
):

    database = (
        tmp_path /
        "knowledge.db"
    )

    repository = (
        KnowledgeRepository(
            database
        )
    )


    project = ProjectEntity(
        name="AIDK",
        root_path=".",
    )


    repository.save_entity(
        project
    )


    stats = (
        repository.statistics()
    )


    assert stats["entities"] == 1



def test_repository_save_relation(
    tmp_path: Path,
):

    repository = KnowledgeRepository(
        tmp_path /
        "knowledge.db"
    )


    module = ModuleEntity(
        name="app",
        path="aidk/app",
        language=Language.PYTHON,
    )


    project = ProjectEntity(
        name="AIDK",
        root_path=".",
    )


    repository.save_entities(
        [
            project,
            module,
        ]
    )


    relation = KnowledgeRelation(
        source_id=project.id,
        target_id=module.id,
        kind=RelationKind.CONTAINS,
    )


    repository.save_relation(
        relation
    )


    stats = repository.statistics()


    assert stats["entities"] == 2
    assert stats["relations"] == 1
