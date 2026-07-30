"""Impact analysis tests."""

from pathlib import Path

from aidk.knowledge import (
    KnowledgeGraph,
    KnowledgeRelation,
    ModuleEntity,
    RelationKind,
    ImpactAnalyzer,
)


def test_import_impact_analysis():

    graph = KnowledgeGraph()


    module_a = ModuleEntity(
        name="a",
        path="a.py",
    )


    module_b = ModuleEntity(
        name="b",
        path="b.py",
    )


    graph.add_entities(
        [
            module_a,
            module_b,
        ]
    )


    graph.add_relation(
        KnowledgeRelation(
            source_id=module_a.id,
            target_id=module_b.id,
            kind=RelationKind.IMPORTS,
        )
    )


    analyzer = ImpactAnalyzer()


    report = analyzer.analyze(
        graph,
        module_b.id,
    )


    assert len(
        report.affected_entities
    ) == 1


    assert report.risk in {
        "LOW",
        "MEDIUM",
        "HIGH",
    }
