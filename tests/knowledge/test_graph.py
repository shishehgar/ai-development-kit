"""Tests for the knowledge graph engine."""

from aidk.knowledge import (
    EntityKind,
    KnowledgeGraph,
    Language,
    ModuleEntity,
    ProjectEntity,
    RelationKind,
    SymbolEntity,
    KnowledgeRelation,
)


def test_add_and_get_entity():

    graph = KnowledgeGraph()

    project = ProjectEntity(
        name="AIDK",
        root_path=".",
    )

    graph.add_entity(project)

    result = graph.get_entity(
        project.id
    )

    assert result is project



def test_add_relation_and_neighbors():

    graph = KnowledgeGraph()

    module = ModuleEntity(
        name="application",
        path="aidk/application",
        language=Language.PYTHON,
    )

    symbol = SymbolEntity(
        kind=EntityKind.CLASS,
        name="Application",
        path="aidk/app/application.py",
    )


    graph.add_entities(
        [
            module,
            symbol,
        ]
    )


    relation = KnowledgeRelation(
        source_id=module.id,
        target_id=symbol.id,
        kind=RelationKind.DEFINES,
    )


    graph.add_relation(
        relation
    )


    neighbors = graph.neighbors(
        module.id
    )

    assert len(neighbors) == 1
    assert neighbors[0].name == (
        "Application"
    )



def test_find_by_name():

    graph = KnowledgeGraph()

    graph.add_entity(
        ModuleEntity(
            name="services",
            path="services",
        )
    )

    result = graph.find_by_name(
        "services"
    )

    assert len(result) == 1



def test_statistics():

    graph = KnowledgeGraph()

    graph.add_entity(
        ProjectEntity(
            name="AIDK",
            root_path=".",
        )
    )

    stats = graph.statistics()

    assert stats["entities"] == 1
    assert stats["projects"] == 1
