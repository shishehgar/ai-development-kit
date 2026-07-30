"""Knowledge graph public API tests."""

from aidk.knowledge import (
    KnowledgeGraph,
)


def test_graph_public_collections():

    graph = KnowledgeGraph()


    assert graph.entities() == []

    assert graph.relations() == []
