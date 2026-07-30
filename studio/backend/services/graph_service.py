"""Graph visualization service."""

from __future__ import annotations


from studio.backend.services.knowledge_runtime import (
    knowledge_runtime,
)



def build_graph_response():

    graph = knowledge_runtime.graph


    nodes = []


    edges = []



    for entity in graph.entities():

        nodes.append(
            {
                "id":
                    str(entity.id),

                "name":
                    entity.name,

                "kind":
                    entity.kind.value,

            }
        )



    for relation in graph.relations():

        edges.append(
            {
                "source":
                    str(relation.source_id),

                "target":
                    str(relation.target_id),

                "relation":
                    relation.kind.value,

            }
        )



    return {

        "nodes":
            nodes,

        "edges":
            edges,

    }
