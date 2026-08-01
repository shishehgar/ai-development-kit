"""Knowledge graph snapshot restoration."""

from __future__ import annotations

from uuid import UUID

from aidk.knowledge.entities import (
    KnowledgeEntity,
    KnowledgeRelation,
    ProjectEntity,
    ModuleEntity,
    SourceFileEntity,
    SymbolEntity,
)

from aidk.knowledge.graph import (
    KnowledgeGraph,
)

from aidk.knowledge.types import (
    EntityKind,
    Language,
    Visibility,
    RelationKind,
)



def entity_from_dict(
    payload: dict,
) -> KnowledgeEntity:

    kind = EntityKind(
        payload["kind"]
    )

    entity_id = UUID(
        payload["id"]
    )


    common = {

        "entity_id":
            entity_id,

        "metadata":
            payload.get(
                "metadata",
                {},
            ),

    }


    if kind == EntityKind.PROJECT:

        return ProjectEntity(
            name=payload["name"],
            root_path=payload.get(
                "root_path",
                ".",
            ),
            description=payload.get(
                "description"
            ),
            **common,
        )


    if kind == EntityKind.MODULE:

        return ModuleEntity(
            name=payload["name"],
            path=payload.get(
                "path",
                "",
            ),
            qualified_name=payload.get(
                "qualified_name"
            ),
            language=Language(
                payload.get(
                    "language",
                    "unknown",
                )
            ),
            **common,
        )


    if kind == EntityKind.SOURCE_FILE:

        return SourceFileEntity(
            name=payload["name"],
            path=payload.get(
                "path",
                "",
            ),
            language=Language(
                payload.get(
                    "language",
                    "unknown",
                )
            ),
            content_hash=payload.get(
                "content_hash"
            ),
            size_bytes=payload.get(
                "size_bytes",
                0,
            ),
            **common,
        )


    return SymbolEntity(
        kind=kind,
        name=payload["name"],
        path=payload.get(
            "path",
            "",
        ),
        qualified_name=payload.get(
            "qualified_name"
        ),
        language=Language(
            payload.get(
                "language",
                "unknown",
            )
        ),
        visibility=Visibility(
            payload.get(
                "visibility",
                "unknown",
            )
        ),
        line_start=payload.get(
            "line_start"
        ),
        line_end=payload.get(
            "line_end"
        ),
        signature=payload.get(
            "signature"
        ),
        docstring=payload.get(
            "docstring"
        ),
        **common,
    )



def relation_from_dict(
    payload: dict,
) -> KnowledgeRelation:

    return KnowledgeRelation(

        source_id=UUID(
            payload["source_id"]
        ),

        target_id=UUID(
            payload["target_id"]
        ),

        kind=RelationKind(
            payload["kind"]
        ),

        relation_id=UUID(
            payload["id"]
        ),

        metadata=payload.get(
            "metadata",
            {},
        ),
    )



def graph_from_snapshot(
    payload: dict,
) -> KnowledgeGraph:

    graph = KnowledgeGraph()


    for item in payload.get(
        "entities",
        [],
    ):

        graph.add_entity(
            entity_from_dict(
                item
            )
        )


    for item in payload.get(
        "relations",
        [],
    ):

        graph.add_relation(
            relation_from_dict(
                item
            )
        )


    return graph
